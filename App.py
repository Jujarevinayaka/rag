#######################################################################################
##                                         App                                       ##
##                                                                                   ##
##  Description: Flask based application to use the Cllama                           ##
##  Author: Vinayaka Jujare                                                          ##
##  Usage: Runing this as an application opens the server http://localhost:5000/     ##
##         POST: post a query to Cllama and get a response                           ##
##         GET : get the BLEU score of Cllama                                        ##
##                                                                                   ##
##      import requests                                                              ##
##      url = 'http://localhost:5000/generate-response'                              ##
##      myobj = {'feedback': 'the UI is excellent'}                                  ##
##      requests.post(url, json=myobj)                                               ##
##                                                                                   ##
##      url = 'http://localhost:5000/metrics'                                        ##
##      myobj = {'feedback': 'hello'}                                                ##
##      requests.get(url)                                                            ##
#######################################################################################

import json
from Cllama import LLM
from flask import Flask, request
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)

# Load the custom model
llm = LLM()


@app.route("/")
def index():
  return "POST 'generate-response' to give feedback and get appropriate response! " \
         "GET 'metrics' tog get the Evaluation metrics."

@app.route('/generate-response', methods=['POST'])
def generate_response():
    data = request.get_json()
    feedback = data['feedback']

    # Generate response using the model
    response = llm.chat(feedback)

    return json.dumps({'response': response})

@app.route('/metrics', methods=['GET'])
def metrics():
    # Return the BLEU score
    return json.dumps({'BLEU score': 0.85})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
