"""Flask app for Cupcakes"""
from flask import Flask, render_template, request, jsonify
from models import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = 'cluckcluck'

connect_db(app)

@app.route('/')
def index_page():
    cupcakes = Cupcake.query.all()
    return render_template('index.html', cupcakes=cupcakes)


@app.route('/api/cupcakes')
def get_cupcakes():
    # transforms the database data of each cupcake serializing it to be jsonified.
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    # Creates a new Cupcake using json formatted data sent to this route
    # Uses the Cupcake model and adds according values but the whole Cupcake model 
    # isn't jasonified until it is serialized.
    new_cupcake = Cupcake(flavor=request.json["flavor"],
                            size=request.json["size"],
                            rating=request.json["rating"],
                            image=request.json["image"])
    db.session.add(new_cupcake)
    db.session.commit()
    # jsonifies the whole Cupcake model
    response_json = jsonify(cupcake=new_cupcake.serialize())
    return (response_json, 201)

@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)

    # Updates certain attributes of a cupcake and if there's no new value
    # for a certain attribute it defaults to the current value
    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = request.json.get("rating", cupcake.rating)
    cupcake.image = request.json.get("image", cupcake.image)

    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message=f"Deleted")