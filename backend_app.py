from flask import Flask, jsonify, request
from Components.package_imports import *
from Components.arft04_prediction import arft04_benchmark_prediction_df
from Components.bridge_model_prediction import bridge_model_prediction_df
from Components.benchmark1_prediction import mean_benchmark_prediction_df
from Components.rf_model_prediction import rf_model_prediction_df
from Components.midas_model_prediction import midas_model_prediction_df
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()
import json
from datetime import datetime
import sys, os
sys.path.append(os.path.dirname(__file__)) 


app = Flask(__name__)

@app.route('/mean_model_prediction', methods = ["POST", "GET"])
def mean_model_prediction():
    data = request.get_json(silent = True)
    selected_month = data["month"]
    selected_year = data["year"]
    selected_date = datetime.strptime(f"{selected_year}-{selected_month}-01", "%Y-%b-%d").strftime("%Y-%m-%d")
    output = mean_benchmark_prediction_df(selected_date)
    output = output.to_json()
    return app.response_class(response = output, status = 200, mimetype= "application/json")

@app.route('/arft04_model_prediction', methods = ["POST", "GET"])
def arft04_model_prediction():
    data = request.get_json(silent = True)
    selected_month = data["month"]
    selected_year = data["year"]
    selected_date = datetime.strptime(f"{selected_year}-{selected_month}-01", "%Y-%b-%d").strftime("%Y-%m-%d")
    output = arft04_benchmark_prediction_df(selected_date)
    output = output.to_json()
    return app.response_class(response = output, status = 200, mimetype = "application/json")

@app.route('/midas_model_prediction', methods = ["POST", "GET"])
def midas_model_prediction():
    data = request.get_json(silent = True)
    selected_month = data["month"]
    selected_year = data["year"]
    selected_date = datetime.strptime(f"{selected_year}-{selected_month}-01", "%Y-%b-%d").strftime("%Y-%m-%d")
    output = midas_model_prediction_df(selected_date)
    output = output.to_json()
    return app.response_class(response = output, status = 200, mimetype = "application/json")

@app.route('/bridge_model_prediction', methods = ["POST", "GET"])
def bridge_model_prediction():
    data = request.get_json(silent = True)
    selected_month = data["month"]
    selected_year = data["year"]
    selected_date = datetime.strptime(f"{selected_year}-{selected_month}-01", "%Y-%b-%d").strftime("%Y-%m-%d")
    output = bridge_model_prediction_df(selected_date)
    output = output.to_json()
    return app.response_class(response = output, status = 200, mimetype = "application/json")

@app.route('/rf_model_prediction', methods = ["POST", "GET"])
def rf_model_prediction():
    data = request.get_json(silent = True)
    selected_month = data["month"]
    selected_year = data["year"]
    selected_date = datetime.strptime(f"{selected_year}-{selected_month}-01", "%Y-%b-%d").strftime("%Y-%m-%d")
    output = rf_model_prediction_df(selected_date)
    output = output.to_json()
    return app.response_class(response = output, status = 200, mimetype = "application/json")

if __name__ == "__main__":
    app.run(debug = True)