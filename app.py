from flask import Flask, render_template, request, jsonify
from basics import optimiser_depense, getdata, repartition
import json
import ast
from flask_cors import CORS

donnees = getdata()

app = Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['JSON_AS_ASCII'] = False

#repartition(optimiser_depense(int(budget), services))

@app.route('/')
def index():
    return "Welcome brother"

"""@app.route('/api/v1', methods=['GET', 'POST'])
def result():
    pass"""
    #return jsonify(repartition(optimiser_depense(int(budget), services)))

@app.route('/api/v1', methods=['GET'])
def my_route():
  budget = request.args["budget"]#.get('budget', default = 1200000, type = int)
  services = request.args["services"]#.get('services', default = ["Traiteur", "Photo"], type = str)
  services = ast.literal_eval(services)
  invites = request.args.get('invites', default=100, type=int)
  print(f'services = {services}\nTypes = {type(services)}')
  repartitions = repartition(optimiser_depense(int(budget),  services))
  print(repartitions)
  #return jsonify(repartitions)
  response = jsonify(repartitions)
  response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
  return response


if __name__ == "__main__":
    app.run(debug=True, port=3000)















