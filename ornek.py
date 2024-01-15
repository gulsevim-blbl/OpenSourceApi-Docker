from flask import Flask, request
from flask_restful import Api, Resource
import pandas as pd
import requests

app = Flask(__name__)
api = Api(app)

class Users(Resource):
    def get(self):
        lang = request.args.get('lang', 'en')  # Default language is set to 'en'
        sayi = request.args.get('sayi', '1')  # Default sayi is set to '1'

        try:
            sayi = int(sayi)
        except ValueError:
            return {'message': 'Invalid value for sayi. It must be an integer.'}, 400

        if sayi > 50:
            return {'message': 'Sayi must be 50 or less.'}, 400

        url = f"https://meowfacts.herokuapp.com/?count={sayi}&lang={lang}"

        response = requests.get(url)
        data = response.json()

        return {'data': data['data']}, 200

    def post(self):
        name = request.args['name']
        age = request.args['age']
        city = request.args['city']

        req_data = pd.DataFrame({
            'name': [name],
            'age': [age],
            'city': [city]
        })

        data = pd.read_csv('kullanici.csv')
        data = data.append(req_data, ignore_index=True)
        data.to_csv('kullanici.csv', index=False)

        return {'message': 'Record successfully added.'}, 201

class Name(Resource):
    def get(self, name):
        data = pd.read_csv('kullanici.csv')
        data = data.to_dict('records')

        for entry in data:
            if entry['name'] == name:
                return {'data': entry}, 200

        return {'message': 'No entry found with this name!'}, 400

api.add_resource(Users, '/users')
api.add_resource(Name, '/isim/<string:name>')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
