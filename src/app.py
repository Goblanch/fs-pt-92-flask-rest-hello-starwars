"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
from models import People, Planet, Vehicle, Favorites

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def get_all_people():
    try:
        people = People.query.all()

        result = [person.serialize() for person in people]

        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/people/<int:people_id>', methods=['GET'])
def get_person_by_id(people_id):
    try:
        person = People.query.get(people_id)

        if not person:
            return jsonify({"error": "Person not found"}), 404
        
        return jsonify(person.serialize()), 200
    
    except Exception as e:
        return jsonify({"error", str(e)}), 500
    
@app.route('/planets', methods=['GET'])
def get_all_planets():
    try:
        planets = Planet.query.all()

        result = [planet.serialize() for planet in planets]

        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):
    try:
        planet = Planet.query.get(planet_id)

        if not planet:
            return jsonify({"error": "Planet not found"}), 404
        
        return jsonify(planet.serialize()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/vehicles', methods=['GET'])
def get_all_vehicles():
    try:
        vehicles = Vehicle.query.all()

        result = [vehicle.serialize() for vehicle in vehicles]

        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle_by_id(vehicle_id):
    try:
        vehicle = Vehicle.query.get(vehicle_id)

        if not vehicle:
            return jsonify({"error": "Vehicle not found"}), 404
        
        return jsonify(vehicle.serialize()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = User.query.all()

        result = [user.serialize() for user in users]

        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    try:
        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404
        
        favorites = Favorites.query.filter_by(associated_user=user.id)

        if not favorites:
            return jsonify({"error": "Favorites not found"}), 404
        
        result = [favorite.serialize() for favorite in favorites]

        if not result:
            return jsonify({"details": "user has no favorites"})

        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/favorite/<int:user_id>/people/<int:person_id>', methods=['POST'])
def add_person_to_favorites(user_id, person_id):
    try:
        user = User.query.get(user_id)

        if user is None:
            return jsonify({"error": "User not found"}), 404

        person = People.query.get(person_id)

        if person is None:
            return jsonify({"error": "Person not found"}), 404
        
        existing_favorite = Favorites.query.filter_by(associated_user=user_id, people_id=person_id).first()
        if existing_favorite:
            return jsonify({"details": "This person is already in favorites"}), 200
        
        new_favorite = Favorites(associated_user=user_id, people_id=person_id)
        db.session.add(new_favorite)
        db.session.commit()

        return jsonify({"details": "Person added to favorites"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/favorite/<int:user_id>/people/<int:person_id>', methods=['DELETE'])
def delete_person_from_favorites(user_id, person_id):
    try:

        user = User.query.get(user_id)

        if user is None:
            return jsonify({"error": "User not found"}), 404

        favorite = Favorites.query.filter_by(associated_user=user_id, people_id=person_id).first()

        if not favorite:
            return jsonify({"error": "Favorite not found"}), 404

        db.session.delete(favorite)
        db.session.commit()

        return jsonify({"details": "Person removed from favorites successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/favorite/<int:user_id>/planet/<int:planet_id>', methods=['POST'])
def add_planet_to_favorites(user_id, planet_id):
    try:
        user = User.query.get(user_id)

        if user is None:
            return jsonify({"error": "User not found"}), 404

        planet = Planet.query.get(planet_id)

        if planet is None:
            return jsonify({"error": "Planet not found"}), 404
        
        existing_favorite = Favorites.query.filter_by(associated_user=user_id, planet_id=planet_id).first()
        if existing_favorite:
            return jsonify({"details": "This planet is already in favorites"}), 200
        
        new_favorite = Favorites(associated_user=user_id, planet_id=planet_id)
        db.session.add(new_favorite)
        db.session.commit()

        return jsonify({"details": "Planet added to favorites"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/favorite/<int:user_id>/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet_from_favorites(user_id, planet_id):
    try:

        user = User.query.get(user_id)

        if user is None:
            return jsonify({"error": "User not found"}), 404

        favorite = Favorites.query.filter_by(associated_user=user_id, planet_id=planet_id).first()

        if not favorite:
            return jsonify({"error": "Favorite not found"}), 404

        db.session.delete(favorite)
        db.session.commit()

        return jsonify({"details": "Planet removed from favorites successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/favorite/<int:user_id>/vehicle/<int:vehicle_id>', methods=['POST'])
def add_vehicle_to_favorites(user_id, vehicle_id):
    try:
        user = User.query.get(user_id)

        if user is None:
            return jsonify({"error": "User not found"}), 404

        vehicle = Vehicle.query.get(vehicle_id)

        if vehicle is None:
            return jsonify({"error": "Vehicle not found"}), 404
        
        existing_favorite = Favorites.query.filter_by(associated_user=user_id, vehicle_id=vehicle_id).first()
        if existing_favorite:
            return jsonify({"details": "This vehicle is already in favorites"}), 200
        
        new_favorite = Favorites(associated_user=user_id, vehicle_id=vehicle_id)
        db.session.add(new_favorite)
        db.session.commit()

        return jsonify({"details": "Vehicle added to favorites"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/favorite/<int:user_id>/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle_from_favorites(user_id, vehicle_id):
    try:

        user = User.query.get(user_id)

        if user is None:
            return jsonify({"error": "User not found"}), 404

        favorite = Favorites.query.filter_by(associated_user=user_id, vehicle_id=vehicle_id).first()

        if not favorite:
            return jsonify({"error": "Favorite not found"}), 404

        db.session.delete(favorite)
        db.session.commit()

        return jsonify({"details": "Vehicle removed from favorites successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
