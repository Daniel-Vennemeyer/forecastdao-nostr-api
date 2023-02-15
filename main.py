from flask import Flask
from flask_restful import Resource, Api, reqparse
import Data

app = Flask(__name__)
api = Api(app)

api.add_resource(Data, '/data')

if __name__ == '__main__':
    app.run()  # run our Flask app
