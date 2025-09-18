#!/usr/bin/env python3
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from models import db, Restaurant, Pizza, RestaurantPizza
from sqlalchemy.exc import IntegrityError

# ----------------------
# Configuration
# ----------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_URI = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False  # Makes JSON output more readable

# ----------------------
# Initialize Extensions
# ----------------------
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# ----------------------
# Basic Route
# ----------------------
@app.route("/")
def index():
    return "<h1>Pizza Restaurants Code Challenge API</h1>"

# ----------------------
# RESTAURANT ROUTES
# ----------------------

# GET all restaurants (without restaurant_pizzas)
@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([r.to_dict(only=("id", "name", "address")) for r in restaurants])

# GET one restaurant by ID (include restaurant_pizzas)
@app.route("/restaurants/<int:id>", methods=["GET"])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404
    return jsonify(restaurant.to_dict())  # full dict, includes restaurant_pizzas

# DELETE a restaurant by ID
@app.route("/restaurants/<int:id>", methods=["DELETE"])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404
    db.session.delete(restaurant)
    db.session.commit()
    return jsonify({}), 204

# ----------------------
# PIZZA ROUTES
# ----------------------

# GET all pizzas (without restaurant_pizzas)
@app.route("/pizzas", methods=["GET"])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([p.to_dict(only=("id", "name", "ingredients")) for p in pizzas])

# ----------------------
# RESTAURANT_PIZZAS ROUTES
# ----------------------
@app.route("/restaurant_pizzas", methods=["POST"])
def create_restaurant_pizza():
    data = request.get_json()
    price = data.get("price")
    pizza_id = data.get("pizza_id")
    restaurant_id = data.get("restaurant_id")

    pizza = Pizza.query.get(pizza_id)
    restaurant = Restaurant.query.get(restaurant_id)

    if not pizza or not restaurant:
        return jsonify({"errors": ["Pizza or Restaurant not found"]}), 404

    try:
        new_rp = RestaurantPizza(price=price, pizza_id=pizza_id, restaurant_id=restaurant_id)
        db.session.add(new_rp)
        db.session.commit()
        return jsonify(new_rp.to_dict()), 201
    except ValueError:
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"errors": ["Database integrity error"]}), 400

# ----------------------
# Run the App
# ----------------------
if __name__ == "__main__":
    app.run(port=5555, debug=True)
