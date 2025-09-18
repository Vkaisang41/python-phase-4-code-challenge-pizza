#!/usr/bin/env python3
from models import db, Restaurant, Pizza, RestaurantPizza
from app import app

with app.app_context():
    print("Deleting old data...")
    db.drop_all()
    db.create_all()

    print("Creating restaurants...")
    r1 = Restaurant(name="Karen's Pizza Shack", address="123 Karen Street")
    r2 = Restaurant(name="Sanjay's Pizza", address="456 Sanjay Avenue")
    r3 = Restaurant(name="Kiki's Pizza", address="789 Kiki Boulevard")
    db.session.add_all([r1, r2, r3])

    print("Creating pizzas...")
    p1 = Pizza(name="Emma", ingredients="Dough, Tomato Sauce, Cheese")
    p2 = Pizza(name="Geri", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
    p3 = Pizza(name="Melanie", ingredients="Dough, Sauce, Ricotta, Red peppers, Mustard")
    db.session.add_all([p1, p2, p3])

    print("Creating restaurant pizzas...")
    rp1 = RestaurantPizza(price=5, pizza=p1, restaurant=r1)
    rp2 = RestaurantPizza(price=10, pizza=p2, restaurant=r2)
    rp3 = RestaurantPizza(price=8, pizza=p3, restaurant=r3)
    db.session.add_all([rp1, rp2, rp3])

    db.session.commit()
    print("✅ Seeding done!")
