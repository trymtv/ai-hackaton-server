from crypt import methods
from flask import Flask, Response, request
import json
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import os, time, uuid

endpoint = ""
key = ""
project_id = ""
publish_iteration_name = ""

app = Flask(__name__)

prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": key})
predictor = CustomVisionPredictionClient(endpoint, prediction_credentials)

app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=["GET"])
def greeting(): 
    return 'This es le algae-wiz forwarder.'

@app.route('/', methods=["POST"])
def serve_picture():

    image = request.files["file"]
    print(image)
    results = predictor.classify_image(project_id, publish_iteration_name, image.read())
    predictions = {}
    for prediction in results.predictions:
        predictions[prediction.tag_name] = "{0:.2f}".format(prediction.probability)
    return json.dumps(predictions)
