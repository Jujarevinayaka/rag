#######################################################################################
##                                         App                                       ##
##                                                                                   ##
##  Description: Flask based application to use the Cllama                           ##
##  Author: Vinayaka Jujare                                                          ##
##  Usage: Runing this as an application opens the server http://localhost:5000/     ##
##         POST: post a query to Cllama and get a response                           ##
##         GET : get the evaluation metrics                                          ##
##                                                                                   ##
##      import requests                                                              ##
##      url = 'http://localhost:5000/generate-response'                              ##
##      myobj = {'feedback': 'the UI is excellent'}                                  ##
##      requests.post(url, json=myobj)                                               ##
##                                                                                   ##
##      url = 'http://localhost:5000/metrics'                                        ##
##      requests.get(url)                                                            ##
#######################################################################################

import json
from Cllama import LLM
from flask import Flask, request, Response
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
    if type(data) is not dict:
        return Response(
            "Invalid POST request, should be in the format of {'feedback': 'some feedback'}",
            status=400,
        )

    if 'feedback' not in data.keys():
        return Response(
            "Invalid POST request, should be in the format of {'feedback': 'some feedback'}",
            status=400,
        )

    feedback = data['feedback']
    reference_response = data.get('reference_response')

    # Generate response using the model
    response, BLEU_score = llm.chat(prompt=feedback, reference_response=reference_response)

    return json.dumps({'response': response})

@app.route('/metrics', methods=['GET'])
def metrics():
    # Return the BLEU score
    score = LLM().get_overall_bleu_score()
    return json.dumps({'BLEU score': score})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
