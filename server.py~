from flask import Flask, request, redirect
import requests
import json
import random
import twilio.twiml
import twitter

app = Flask(__name__)

noIntent = [
    "I'm having trouble understanding you, could you rephrase your question?",
    "I didn't catch that, could you rephrase your query?",
    "Sorry, I didn't understand that. Try rephrasing your request."
]

@app.route("/", methods=['GET', 'POST'])
def recieveSMS():
    """Respond to a text with the input (this is a temporary behavior), and decide the appropriate handler"""
    # text_body = request.values.get('Body', None)
    # resp = twilio.twiml.Response()
    # resp.message(text_body)
    wit_response = requests.get(url='https://api.wit.ai/message?v=20150912&q=' + request.values.get('Body', None),headers={'Authorization': 'Bearer I4WKESB35IVVAHPAG4YVYRQ6MB26UAGG'})
    wit_dict = json.loads(wit_response.text)
    print wit_dict
    intent = wit_dict.get('outcomes')[0].get('intent')
    print intent
    confidence = wit_dict.get('outcomes')[0].get('confidence')
    print confidence
    entities = wit_dict.get('outcomes')[0].get('entities')
    print entities

    if confidence < .2:
        noValidIntent()
    elif intent == "lookup":
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
    return 'ok'


#1 Lookup uses the Bing Search API
@app.route("/lookup", methods=['GET', 'POST'])
def lookup(entities):
    return "temp"
#     key = "nAiE8uvJl0LDZE0U0rqvxcIt93KFjmLcyiDF3jpk8ig"
#     url = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/?Query=%27'+entities+'%27&$top=5&$format=json'
#     response_data = requests.get(url)
#     json_result = json.loads(response_data)
#     result_list = json_result['d']['results']
#     print result_list
#     return result_list

#2 Navigate
@app.route("/navigate", methods=['GET', 'POST'])
def navigate(entities):
    key = "GSC5hkB0CEmUyk4nI2MY~HxNEzo1P1bHB1sX8EzDJpA~AmYeCHqvBerEI06DBSKWfo4pgB1w9Krgk7EH6lhGqqf3s5RaJArOzWJ-SL6AYVVw"
    origin = entities.get('origin')[0].get('value');
    destination = entities.get('destination')[0].get('value');
    bingMapsResponse = requests.get(url="http://dev.virtualearth.net/REST/V1/Routes/Driving?wp.0=" + origin + "&wp.1=" + destination + "&avoid=minimizeTolls&key="+key)
    bingMaps_dict = json.loads(bingMapsResponse.text)
    resources = bingMaps_dict.get('resourceSets')[0].get('resources')
    routeLegs = resources[0].get('routeLegs')

    message = ""

    distance = routeLegs[0].get('routeSubLegs')[0].get('travelDistance')
    message += "Total Trip Distance: " + str(distance) + " km\n"
    duration = routeLegs[0].get('routeSubLegs')[0].get('travelDuration')
    message += "Total Trip Duration: " + str(duration/60) + " min \n"
    itineraryItems = routeLegs[0].get('itineraryItems')
    for item in itineraryItems:
        message += item.get('instruction').get('text') + " ("
        message += str(item.get('travelDistance')) + " km, "
        message += str(item.get('travelDuration') / 60 ) + " min)"
        message += "\n"
    resp = twilio.twiml.Response()
    resp.message(message)
    return 'ok'

#3 Translate
@app.route("/translate", methods=['GET', 'POST'])
def translate(entities):
    return -1 #TODO

#4 Weather
@app.route("/weather", methods=['GET', 'POST'])
def weather(entities):
    location = entities.get('location')[0].get('value');
    weather_response = requests.get(url="http://api.openweathermap.org/data/2.5/weather?.q=" + location)
    weather_dict = json.loads(weather_response.text)
    weather = weather_dict.get('list').get('location')[0] #Confirm if this works with Nelson
    
    message = "The weather at " + location + " is " + weather
    resp = twilio.twiml.Response()
    resp.message(message)
    return 'ok'

#5 Twitter Updates
@app.route("/twitter_updates", methods=['GET', 'POST'])
def twitter_updates(entities):
    username = entities.get('username')[0].get('value');
    api = twitter.Api(consumer_key='4m8fjnhaub0s1KGb7jrcGZIKR',consumer_secret='rtohH46EgVGWVIA1BSEImdNpIkNqm7bvREttacwTGK72mxrLZK',access_token_key='2735117372-CEiN7lE00OBfqNmWlVmypzNkblwyVM3cpIGyYdy',access_token_secret='wgADPMZkEWEOqYCa8oZcpWdYJnOuTdtwjeJLC9JbvDew7')
    statuses = api.GetUserTimeline(screen_name=username, count =1)
    latestTweet = [s.text for s in statuses]
    message = "@"+username+": " + latestTweet
    resp = twilio.twiml.Response()
    resp.message(message)
    return 'ok'

#6 Stock Report
@app.route("/stock_report", methods=['GET', 'POST'])
def stock_report(entities):
    company = entities.get('company')[0].get('value')
    yahooFinanceResponse = requests.get(url="http://finance.yahoo.com/webservice/v1/symbols/"+company+"/quote?format=json")
    yahooFinance_dict = json.loads(yahooFinanceResponse.text)
    price = yahooFinance_dict.get('list').get('resources')[0].get('resource').get('fields').get('price')
    message = company+" is currently at " + "$" + price +"."
    resp = twilio.twiml.Response()
    resp.message(message)
    return 'ok'

# No Valid Intent Found
@app.route("/noValidIntent", methods=['GET', 'POST'])
def noValidIntent():
    resp = twilio.twiml.Response()
    message = random.choice(noIntent)
    resp.message(message)

if __name__ == "__main__":
    app.run(debug=True)
