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

#1 Lookup uses the Bing Search API
@app.route("/lookup", methods=['GET', 'POST'])
def lookup(query):
    #search_type: Web, Image, News, Video
    key = nAiE8uvJl0LDZE0U0rqvxcIt93KFjmLcyiDF3jpk8ig
    # create credential for authentication
    #user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)'
    #credentials = (':%s' % key).encode('base64')[:-1]
    #auth = 'Basic %s' % credentials
    url = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/'+'?Query=%27'+query+'%27&$top=5&$format=json'
    request = urllib2.Request(url)
    #request.add_header('Authorization', auth)
    #request.add_header('User-Agent', user_agent)
    request_opener = urllib2.build_opener()
    response = request_opener.open(request) 
    response_data = response.read()
    json_result = json.loads(response_data)
    result_list = json_result['d']['results']
    print result_list
    return result_list

#2 Navigate
@app.route("/navigate", methods=['GET', 'POST'])
def navigate(x, y):
    key = GSC5hkB0CEmUyk4nI2MY~HxNEzo1P1bHB1sX8EzDJpA~AmYeCHqvBerEI06DBSKWfo4pgB1w9Krgk7EH6lhGqqf3s5RaJArOzWJ-SL6AYVVw
    return -1 #TODO

if __name__ == "__main__":
    app.run(debug=True)
