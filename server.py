from flask import Flask, request, redirect
import requests
import json
import twilio.twiml

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def callWit():
    """Respond to a text with the input, and print the wit.ai generated json to console"""

    text_body = request.values.get('Body', None)
    resp = twilio.twiml.Response()
    resp.message(text_body)
    wit_response = requests.get(url='https://api.wit.ai/message?v=20150912&q=' + request.values.get('Body', None),headers={'Authorization': 'Bearer I4WKESB35IVVAHPAG4YVYRQ6MB26UAGG'})
    wit_dict = json.loads(wit_response.text)
    print wit_dict
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
