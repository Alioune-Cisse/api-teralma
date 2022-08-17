import pandas as pd
import numpy as np
from scipy.optimize import linprog

## Lire données
data_alain = pd.read_csv("data alain.csv")

## Renommer colonne
data_alain.rename(columns={"Unnamed: 1":"Sous catégories dépenses"}, inplace=True)
## Remplacer les nan par la valeur du dessus
data_alain['Catégories dépenses'] = pd.Series(data_alain['Catégories dépenses']).fillna(method='ffill')


def optimiser_depense(budget, services, df=data_alain):
  palier1 = list(df[df['Catégories dépenses'] == "Total dépenses cérémonies"]['Palier Prix 1'])[0]
  palier2 = list(df[df['Catégories dépenses'] == "Total dépenses cérémonies"]['Palier Prix 2'])[0]
  palier3 = list(df[df['Catégories dépenses'] == "Total dépenses cérémonies"]['Palier Prix 3'])[0]
  palier4 = list(df[df['Catégories dépenses'] == "Total dépenses cérémonies"]['Palier Prix 4'])[0]

  palier = (budget <= palier1 and "Palier Prix 1") or (budget <= palier2 and "Palier Prix 2") or (budget <= palier3 and "Palier Prix 3") or "Palier Prix 4"

  dico = create_dict(services, df)
  """A = -1 * np.array(list(dico.values()))
  b = np.array([float(df[df['Sous catégories dépenses']==elt][palier]) for elt in dico.keys()])
  c = -1 * np.array(list(dico.values()))"""

  A,b,c = create_val(services, palier, df, budget)
  #return A, b, c
  print(f'b = {b}\n A = {A}\nc = {c}\n{type(b)}, {type(A)}, {type(c)}')
  res = linprog(c, A_ub=np.array(A), b_ub=np.array(b),bounds=(0, None))
  res.x = [round(elt) for elt in res.x]

  #print('Optimal value:', -1*res.fun, '\nX:', res.x)
  dicto = dict(zip(services, res.x))
  dicto["Autres"] = budget - round(-1*res.fun)
  #print(f"Dépenses Totales : {round(-1*res.fun)} FCFA\n\n____________________________")
  #for i,j in zip(dicto.keys(), dicto.values()):
    #print(f'Dépenses prévues pour {i} = {round(j)}FCFA\n----------------------------')

  return dicto

def create_dict(services, df=data_alain):
  all_services = list(df[~df['Sous catégories dépenses'].isnull()]['Sous catégories dépenses'])
  #all = ['Mouton ', 'Traiteur']
  dico = {}
  for elt in all_services:
    if elt in services:
      dico[elt] = 1
    else:
      dico[elt] = 0

  #print(dico)

  return dico


def create_val(services, palier, df, budget):
  A = [np.ones(len(services))]
  b1 = [budget]
  b2 = [(df[df['Sous catégories dépenses']==elt][palier]).astype(float) for elt in services]

  b = [*b1, *b2]
  c = -1 * np.ones(len(services))

  n = len(b)
  for i in range(n-1):
    val = np.zeros(n-1)
    val[i] = 1
    A.append(val.tolist())

  return A, b, c

def getdata(df=data_alain):
  all_services = list(df[~df['Sous catégories dépenses'].isnull()]['Sous catégories dépenses'])
  return all_services


def repartition(depenses, df=data_alain):
  df = df.dropna()
  gestion_totale = {i:[] for i in list(df['Catégories dépenses'].unique())}

  for i, j in depenses.items():
    try:
      a = list(df[df['Sous catégories dépenses']==i]['Catégories dépenses'])[0]
      gestion_totale[a] = np.append(gestion_totale[a], {i:j})

    except:
      pass
  #val = {k:v for k,v in gestion_totale.items() if v != list()}

  for k, v in gestion_totale.items():
    somme = 0
    for elt in v:
      for i, j in elt.items():
        somme += elt[i]
    gestion_totale[k] = np.append(v, {"Total": somme}).tolist()

  return gestion_totale
