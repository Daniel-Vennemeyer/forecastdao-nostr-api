from flask import Flask
from flask_restful import Resource, Api
import Data


app = Flask(__name__)
api = Api(app)

api.add_resource(Data, '/data')

if __name__ == '__main__':
    app.run()  # run our Flask app
    # app.run(host='127.0.0.1', port=3000, debug=True)
