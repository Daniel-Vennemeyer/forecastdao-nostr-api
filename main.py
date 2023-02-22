from flask import Flask
from flask_restful import Resource, Api
import Data

app = Flask(__name__)
api = Api(app)

api.add_resource(Data.Data, '/data')

@app.route('/')
def hello_world():
	return 'Hello World!'

if __name__ == '__main__':
    # app.run()  # run our Flask app
    app.run(host='127.0.0.1', port=5000)
