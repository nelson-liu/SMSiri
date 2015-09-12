from flask import Flask, request, redirect
import requests
import json
import random
import twilio.twiml

app = Flask(__name__)

noIntent = [
    "I'm having trouble understanding you, could you rephrase your question?",
    "I didn't catch that, could you rephrase your query?",
    "Sorry, I didn't understand that. Try rephrasing your request."
]

@app.route("/", methods=['GET', 'POST'])
def recieveSMS():
    """Respond to a text with the input (this is a temporary behavior), and decide the appropriate handler"""
    text_body = request.values.get('Body', None)
    # resp = twilio.twiml.Response()
    # resp.message(text_body)
    wit_response = requests.get(url='https://api.wit.ai/message?v=20150912&q=' + request.values.get('Body', None),headers={'Authorization': 'Bearer I4WKESB35IVVAHPAG4YVYRQ6MB26UAGG'})
    wit_dict = json.loads(wit_response.text)
    print wit_dict
    intent = wit_dict.get('outcomes')[0].get('intent')
    print intent
    entities = wit_dict.get('outcomes')[0].get('entities')
    print entities

    if intent == "lookup":
        lookup(entities)
    elif intent == "navigate":
        navigate(entities)
    elif intent == "translate":
        translate(entities)
    elif intent == "weather":
        weather(entities)
    elif intent == "twitter_updates":
        twitter_updates(entities)
    elif intent == "stock_report":
        stock_report(entities)
    else:
        noValidIntent()

#1 Lookup uses the Bing Search API
@app.route("/lookup", methods=['GET', 'POST'])
def lookup(entities):
    key = 'nAiE8uvJl0LDZE0U0rqvxcIt93KFjmLcyiDF3jpk8ig'
    url = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/'+'?Query=%27'+entities+'%27&$top=5&$format=json'
    request = urllib2.Request(url)
    request_opener = urllib2.build_opener()
    response = request_opener.open(request)
    response_data = response.read()
    json_result = json.loads(response_data)
    result_list = json_result['d']['results']
    print result_list
    return result_list

#2 Navigate
@app.route("/navigate", methods=['GET', 'POST'])
def navigate(entities):
    return -1 #TODO

#3 Translate
@app.route("/translate", methods=['GET', 'POST'])
def translate(entities):
    return -1 #TODO

#4 Weather
@app.route("/weather", methods=['GET', 'POST'])
def weather(entities):
    return -1 #TODO

#5 Twitter Updates
@app.route("/twitter_updates", methods=['GET', 'POST'])
def twitter_updates(entities):
    return -1 #TODO

#6 Stock Report
@app.route("/stock_report", methods=['GET', 'POST'])
def stock_report(entities):
    return -1 #TODO

# No Valid Intent Found
@app.route("/noValidIntent", methods=['GET', 'POST'])
def noValidIntent():
    resp = twilio.twiml.Response()
    resp.message(random.choice(noIntent))

if __name__ == "__main__":
    app.run(debug=True)
