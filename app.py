from flask import Flask
from flask_restful import Resource, Api
import Data
import json
import requests


app = Flask(__name__)
api = Api(app)

api.add_resource(Data.Data, '/data')

@app.route('/')
def hello_world():
	return 'Welcome to ForecastDao. \nPlease enter your predictions through the nostr relay wss://nostr.forecastdao.com'
            
@app.route('/clean')
def clean(): #Get just the values for the data from the nostr relay
    try:
        data = Data.Data.get()
        # data = requests.get(url="http://3.144.27.94:5000/data").text
        data = data.replace("\n", "")
        data = json.loads(data)
        cleaned = []
        for event in data:
            indicator, value, rationale = event[0].split("#")[2:] #extracts and cleans nostr data

            indicator = indicator.replace("\\n", "").replace("'", "").replace('"', "").replace("indicator ", "")
            value = float(value.replace("\\n", "").replace("'", "").replace('"', "").replace(",", "").replace("value ", ""))
            rationale = rationale.replace("\\n", "").replace("rationale ", "") # data is clean
            cleaned.append((indicator, value, rationale))
        return cleaned
    except Exception as e:
         print(f"ERROR in forecastdao-nostr-api.clean: {e}")
         return f"ERROR in forecastdao-nostr-api.clean: {e}" #For testing ONLY

@app.route('/send')
def send(): #sends the data from the nostr relay's default sqlite database to our ComposeDB with only the information and formatting we want
    try:
        data = cleaner()
        for event in data:
            indicator, value, rationale = event
            body = """
            mutation CreateForecast($i:CreateForecastInput!){
                createForecast(input: $i){
                    document{
                        indicator
                        value
                        rationale
                    }
                }
            }
            """
            
            url = "http://3.144.27.94:36593/graphql" #url for graphql editor running in our aws ec2 instance (url only accessible to permissioned ips)
            response = requests.post(url=url, json={"query": body, "variables":  #posts to our composedb
                {
                "i":
                        {"content": {
                            "indicator": indicator,
                            "value": value,
                            "rationale": rationale
                        }
                }
            }})

            print("response status code: ", response.status_code)
            if response.status_code == 200:
                print("response : ",response.content)
            print(response.text)
    except Exception as e:
        print(f"ERROR in forecastdao-nostr-api.send: {e}")


if __name__ == '__main__':
    # send()
    app.run(host='127.0.0.1', port=5000)
