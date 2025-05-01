from flask import Flask, jsonify, request, abort
from flights import Flights
from passenger import Passenger
from flasgger import Swagger

app = Flask(__name__)

swagger = Swagger(app, template_file='swagger.yaml')


flights_registered = [
    Flights(1, "Belem", "Maldivas", "19:00", 2000,
        ["10A", "25B", "17D"],
        [Passenger("Gabriel", "gabriel@gmail.com"),
         Passenger("Luan", "luan@gmail.com"),
         Passenger("Ronald", "ronald@gmail.com"),],
    ),
    Flights(2, "Belem", "Maldivas", "08:00",3000,
        [],
        [Passenger("Hugo", "hugo@gmail.com"),
         Passenger("Fabio", "fabio@gmail.com"),
         Passenger("Lih", "lih@gmail.com"),],
    ),
]


@app.route("/flights/get-flight/<int:identifier>", methods=["GET"])
def get_flight(identifier):
    for flight in flights_registered:
        if flight.identifier == identifier:
            return jsonify(flight.to_json_object()), 200

    return jsonify({"error": "Not found"}), 404


@app.route("/flights/search-flights/<departure>/<destination>", methods=["GET"])
def search_flights(departure, destination):
    available = [
        f for f in flights_registered
        if f.departure.casefold() == departure.casefold()
        and f.destination.casefold() == destination.casefold()
    ]

    if not available:
        return jsonify({"error": "No flights available for this trip."}), 404

    return jsonify([f.get_short_info() for f in available]), 200


@app.route("/flights/book-flight/<int:identifier>/<seat>", methods=["POST"])
def book_flight(identifier, seat):
    data = request.get_json() or {}
    username = data.get("username")
    email = data.get("email")

    if not username or not email:
        return jsonify({"error": "username and email required"}), 400

    for flight in flights_registered:
        if flight.identifier != identifier:
            continue

        if len(flight.seats_avaible) < 1:
            return jsonify({"error": "No seats available"}), 400

        if seat not in flight.seats_avaible:
            return jsonify({"error": "Seat not available"}), 400

        flight.seats_avaible.remove(seat)
        flight.passenger.append(Passenger(username, email))
        return jsonify({"message": "Flight booked successfully"}), 201

    return jsonify({"error": "Flight not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)  
