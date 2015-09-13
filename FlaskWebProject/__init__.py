from flask import Flask, request, redirect
from microsofttranslator import Translator
import requests
import json
import random
import twilio.twiml
import twitter
import wolframalpha

app = Flask(__name__)
app.debug=True

noIntent = [
    "I'm having trouble understanding you, could you rephrase your question?",
    "I didn't catch that, could you rephrase your query?",
    "Sorry, I didn't understand that. Try rephrasing your request."
]

@app.route("/", methods=['GET', 'POST'])
# Process a received text and decide the appropriate function to call.
def recieveSMS():
    wit_response = requests.get(url='https://api.wit.ai/message?v=20150912&q=' + request.values.get('Body', ''),headers={'Authorization': 'Bearer I4WKESB35IVVAHPAG4YVYRQ6MB26UAGG'})
    return wit_response
    wit_dict = json.loads(wit_response.text)
    print wit_dict

    intent = wit_dict.get('outcomes')[0].get('intent')
    print intent

    confidence = wit_dict.get('outcomes')[0].get('confidence')
    print confidence

    entities = wit_dict.get('outcomes')[0].get('entities')
    print entities

    msg = None

    if confidence < .2:
        msg = noValidIntent()
    elif intent == "wolfram":
        msg = wolfram(entities)
    elif intent == "navigate":
        msg = navigate(entities)
    elif intent == "translate":
        msg = translate(entities)
    elif intent == "weather":
        msg = weather(entities)
    elif intent == "twitter_updates":
        msg = twitter_updates(entities)
    elif intent == "stock_report":
        msg = stock_report(entities)
    elif intent == "activities":
        msg = activities(entities)
    elif intent == "news":
        msg = news(entities)
    else:
        msg = noValidIntent()

    return str(msg)


# @app.route("/wolfram", methods=['GET', 'POST'])
# # Use the wolfram|alpha API to retrieve results to natural language queries.
# # This is a bit unstable, there exists the possibility of the response not having a
# # 'results' pod, which then causes an error. Use with caution.
# def wolfram(entities):
#     question = entities.get('question')[0].get('value');
#     client = wolframalpha.Client('Y9VVR7-5A9P7Y4893')
#     res = client.query(question)
#     message = next(res.results).text
#
#     resp = twilio.twiml.Response()
#     resp.message(message)
#     print message
#     return resp
#
# @app.route("/navigate", methods=['GET', 'POST'])
# # Use the Bing Maps API to generate step by step driving directions from a given
# # start point and end point.
# def navigate(entities):
#     key = "GSC5hkB0CEmUyk4nI2MY~HxNEzo1P1bHB1sX8EzDJpA~AmYeCHqvBerEI06DBSKWfo4pgB1w9Krgk7EH6lhGqqf3s5RaJArOzWJ-SL6AYVVw"
#     origin = entities.get('origin')[0].get('value');
#     destination = entities.get('destination')[0].get('value');
#     bingMapsResponse = requests.get(url="http://dev.virtualearth.net/REST/V1/Routes/Driving?wp.0=" + origin + "&wp.1=" + destination + "&avoid=minimizeTolls&key="+key)
#     bingMaps_dict = json.loads(bingMapsResponse.text)
#     resources = bingMaps_dict.get('resourceSets')[0].get('resources')
#     routeLegs = resources[0].get('routeLegs')
#     message = ""
#     distance = routeLegs[0].get('routeSubLegs')[0].get('travelDistance')
#     message += "Total Trip Distance: " + str(distance) + " km\n"
#     duration = routeLegs[0].get('routeSubLegs')[0].get('travelDuration')
#     message += "Total Trip Duration: " + str(duration/60) + " min \n"
#     itineraryItems = routeLegs[0].get('itineraryItems')
#     count = 1
#     for item in itineraryItems:
#         message += str(count) + ". " + item.get('instruction').get('text') + " ("
#         message += str(item.get('travelDistance')) + " km, "
#         message += str(item.get('travelDuration') / 60 ) + " min)"
#         message += "\n"
#         count +=1
#     resp = twilio.twiml.Response()
#     resp.message(message)
#     print message
#     return resp
#
# @app.route("/translate", methods=['GET', 'POST'])
# # Use the Microsoft Translator API to translate given text from one language
# # to another.
# def translate(entities):
#     phrase_to_translate = entities.get('phrase_to_translate')[0].get('value')
#     message = ""
#     if entities.get('language') == None:
#         message = "Language not supported"
#     else:
#         language = entities.get('language')[0].get('value')
#         language = language.lower()
#         if language == "chinese":
#             language = "zh-CHS"
#         elif language == "dutch":
#             language = "nl"
#         elif language == "english":
#             language = "en"
#         elif language == "french":
#             language = "fr"
#         elif language == "german":
#             language = "de"
#         elif language == "italian":
#             language = "it"
#         elif language == "japanese":
#             language = "ja"
#         elif language == "korean":
#             language = "ko"
#         elif language == "portuguese":
#             language = "pt"
#         elif language == "russian":
#             language = "ru"
#         elif language == "spanish":
#             language = "es"
#         elif language == "swedish":
#             language = "sv"
#         elif language == "thai":
#             language = "th"
#         elif language == "vietnamese":
#             language = "vi"
#         else:
#             message = "Language not supported"
#     if message != "Language not supported":
#         translator = Translator('SMSAssistant', 'fhV+AdYFiK0QfQ4PFys+oQ/T0xiBBVQa32kxxbP55Ks=')
#         message = translator.translate(phrase_to_translate, language)
#     resp = twilio.twiml.Response()
#     print message
#     resp.message(message)
#     return resp
#
# @app.route("/weather", methods=['GET', 'POST'])
# # Use the OpenWeatherMap API to get the weather at a location.
# def weather(entities):
#     location = entities.get('location')[0].get('value');
#     weatherResponse = requests.get(url="http://api.openweathermap.org/data/2.5/weather?q=" + location)
#     weather_dict = json.loads(weatherResponse.text) #Gets all the JSON
#     weatherDescription = weather_dict.get('weather')[0].get('description')
#     temperatureInKelvin = weather_dict.get('main').get('temp')
#
#     temperatureInFarenheit = kelvinToFarenheit(temperatureInKelvin)
#     degree_sign= u'\N{DEGREE SIGN}' #To get degree sign
#
#     print degree_sign
#
#     message = "In " + location + ", the weather forecast is " + weatherDescription + " and the temperature is " + str(temperatureInFarenheit) + " " + degree_sign + "F"
#     resp = twilio.twiml.Response()
#     resp.message(message)
#     print message
#     return resp
#
# def kelvinToFarenheit(tempInK):
#     return (tempInK - 273.15) * 1.8 + 32.0
#
# @app.route("/twitter_updates", methods=['GET', 'POST'])
# # Use the Twitter API to get the most recent tweet of a public user.
# def twitter_updates(entities):
#     username = entities.get('username')[0].get('value');
#     api = twitter.Api(consumer_key='4m8fjnhaub0s1KGb7jrcGZIKR',consumer_secret='rtohH46EgVGWVIA1BSEImdNpIkNqm7bvREttacwTGK72mxrLZK',access_token_key='2735117372-CEiN7lE00OBfqNmWlVmypzNkblwyVM3cpIGyYdy',access_token_secret='wgADPMZkEWEOqYCa8oZcpWdYJnOuTdtwjeJLC9JbvDew7')
#     statuses = api.GetUserTimeline(screen_name=username, count =1)
#     latestTweet = statuses[0].text
#     message = "@"+username+": " + latestTweet
#     print message
#     resp = twilio.twiml.Response()
#     resp.message(message)
#     return resp
#
# @app.route("/stock_report", methods=['GET', 'POST'])
# # Use the Yahoo Finance API to get the most recent stock price of a given symbol.
# def stock_report(entities):
#     company = entities.get('company')[0].get('value')
#     yahooFinanceResponse = requests.get(url="http://finance.yahoo.com/webservice/v1/symbols/"+company+"/quote?format=json")
#     yahooFinance_dict = json.loads(yahooFinanceResponse.text)
#     price = yahooFinance_dict.get('list').get('resources')[0].get('resource').get('fields').get('price')
#     message = company+" is currently at " + "$" + price +"."
#     print message
#     resp = twilio.twiml.Response()
#     resp.message(message)
#     return resp
#
# @app.route("/activities", methods=['GET', 'POST'])
# # Use the Expedia Activities API to get a list of fun activities to do near a location.
# def activities(entities):
#     location = entities.get('location')[0].get('value')
#     print location
#     expediaResponse = requests.get(url="http://terminal2.expedia.com/x/activities/search?location="+location+"&apikey=yYTYKKUxJFqVXrc9fXduouBGThAAWQH5")
#     expedia_dict = json.loads(expediaResponse.text)
#     activities = expedia_dict.get('activities')
#     message = ""
#     count = 1
#     for activity in activities:
#         message += str(count) + ". "
#         message += activity.get('title')
#         message += " (" + str(activity.get('fromPrice'))
#         message += " " + activity.get('fromPriceLabel') + ") \n"
#         count += 1
#     resp = twilio.twiml.Response()
#     resp.message(message)
#     print message
#     return resp
#
# @app.route("/news", methods=['GET', 'POST'])
# # Use the Bing Search News API to get a listing of recent headlines pertaining to a certain topic.
# def news(entities):
#     topic = entities.get('topic')[0].get('value')
#     print topic
#     news_response = requests.get(url='https://api.datamarket.azure.com/Bing/Search/News?$format=json&Query=%27' + topic+"%27", auth=('oeToVPEyRZIASRK2n2byOU1x0EMatLIpd8kCIvwXmMw','oeToVPEyRZIASRK2n2byOU1x0EMatLIpd8kCIvwXmMw'))
#     print news_response
#     news_dict = json.loads(news_response.text)
#     news = news_dict.get('d').get('results')
#     print news
#     message = "Here are the top stories about " + topic + ":\n"
#     if len(news) >= 3:
#         for x in range(0, 2):
#             message += news[x].get('Title') + ",\n"
#         message += news[2].get('Title')
#     else:
#         for item in news:
#             message += item.get('Title') + ",\n"
#         message += item.get('Title')
#     resp = twilio.twiml.Response()
#     resp.message(message)
#     print message
#     return resp
#
# @app.route("/noValidIntent", methods=['GET', 'POST'])
# # No valid intent was found, so an error message will be texted back.
# def noValidIntent():
#     resp = twilio.twiml.Response()
#     message = random.choice(noIntent)
#     resp.message(message)
#     return resp
#
# if __name__ == "__main__":
#     app.run(debug=True)
