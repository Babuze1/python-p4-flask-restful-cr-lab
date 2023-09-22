#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Home(Resource):
    def get(text):
        return ("The plants are here!")

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        serialized_plants = [plant.to_dict() for plant in plants]
        return jsonify(serialized_plants)

    def post(self):
        data = request.get_json()
        if 'image' not in data:
            return make_response(jsonify(message="Image is required"), 400)
        new_plant = Plant(name=data['name'], image=data['image'], price=data['price'])
        db.session.add(new_plant)
        db.session.commit()
        return jsonify(new_plant.to_dict())

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get(id)
        if plant is not None:
            return jsonify(plant.to_dict())
        else:
            return make_response(jsonify(message="Plant not found"), 404)
        
api.add_resource(Home, '/')        
api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
