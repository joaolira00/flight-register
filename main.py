from flask import Flask, jsonify
from flights import Flights

app = Flask(__name__)

flights_registered = [
    Flights(1, "Belem", "Maldivas", 19, 2000, ["10A", "25B", "17D"]),
    Flights(2, "Belem", "Maldivas", 8, 3000, ["15A", "25F", "12D"])
]


@app.route('/flights/get-flight/<identifier>', methods=['GET'])
def get_flight(identifier):
    identifier = int(identifier)

    for flight in flights_registered:
        if flight.identifier == identifier:
            return jsonify(flight.to_json_object())
        
    return {"error: ": 404, "message: ": "Not found."}

@app.route('/flights/search-flights/<departure>/<destination>', methods=['GET'])
def search_flights(departure, destination):
    avaiable_flights = []

    for flight in flights_registered:
        if flight.departure == departure and flight.destination == destination:
            avaiable_flights.append(flight)

    return jsonify([flight.to_json_object() for flight in avaiable_flights])


if __name__ == '__main__':
    app.run(debug=True)