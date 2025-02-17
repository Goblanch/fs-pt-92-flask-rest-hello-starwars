from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    favorites = db.relationship('Favorites', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "is_active": self.is_active
        }
    
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    birth_year = db.Column(db.String(40), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    hair_color = db.Column(db.String(30), nullable=False)
    eye_color = db.Column(db.String(30), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    mass = db.Column(db.Integer, nullable=False)
    skin_color = db.Column(db.String(30), nullable=False)

    favorites = db.relationship('Favorites', backref='people', lazy=True)

    def __repr__(self):
        return '<People %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year, 
            "gender": self.gender,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "height": self.height,
            "mass": self.mass,
            "skin_color": self.skin_color
        }
    
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    climate = db.Column(db.String(40), nullable=False)
    terrain = db.Column(db.String(50), nullable=False)
    gravity = db.Column(db.Integer, nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    orbital_period = db.Column(db.Integer, nullable=False)
    rotation_period = db.Column(db.Integer, nullable=False)
    population = db.Column(db.Integer, nullable=False)
    surface_water = db.Column(db.Boolean(), nullable=False)

    favorites = db.relationship('Favorites', backref='planet', lazy=True)

    def __repr__(self):
        return '<Planet %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "gravity": self.gravity,
            "diameter": self.diameter,
            "orbital_period": self.orbital_period,
            "rotation_period": self.rotation_period,
            "population": self.population,
            "surface_water": self.surface_water
        }

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    manufacter = db.Column(db.String(60), nullable=False)
    passengers = db.Column(db.Integer, nullable=False)
    crew = db.Column(db.Integer, nullable=False)
    cargo_capacity = db.Column(db.Integer, nullable=False)
    consumables = db.Column(db.Integer, nullable=False)
    cost_in_credits = db.Column(db.Integer, nullable=False)
    length = db.Column(db.Integer, nullable=False)
    max_atmosphering_speed = db.Column(db.Integer, nullable=False)

    favorites = db.relationship('Favorites', backref='vehicles', lazy=True)

    def __repr__(self):
        return '<Vehicle %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacter": self.manufacter,
            "passengers": self.passengers,
            "crew": self.crew,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "max_atmosphering_speed": self.max_atmosphering_speed
        }
    
class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    associated_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))

    def serialize(self):
        return {
            "id": self.id,
            "associated_user": self.associated_user,
            "people_id": self.people_id,
            "planet_id": self.planet_id,
            "vehicle_id": self.vehicle_id
        }
    