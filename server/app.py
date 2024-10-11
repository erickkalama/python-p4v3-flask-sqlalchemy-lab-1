# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response,jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake_by_id(id):
    # Query the Earthquake by its ID
    earthquake = db.session.get(Earthquake, id)
    
    if earthquake:
        # If the earthquake is found, return its details as JSON
        return jsonify({
            "id": earthquake.id,
            "location": earthquake.location,
            "magnitude": earthquake.magnitude,
            "year": earthquake.year
        }), 200
    else:
        # If no earthquake is found, return a 404 error
        return jsonify({
            "message": f"Earthquake {id} not found."
        }), 404

@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_minimum_magnitude(magnitude):
    # Query to get all earthquakes with magnitude >= the given magnitude
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
    # Format the list of earthquakes into dictionaries
    quake_list = [{
        "id": quake.id,
        "location": quake.location,
        "magnitude": quake.magnitude,
        "year": quake.year
    } for quake in earthquakes]

    # Return the count and the list of earthquakes
    return jsonify({
        "count": len(earthquakes),
        "quakes": quake_list
    }), 200
if __name__ == '__main__':
    app.run(port=5555, debug=True)



