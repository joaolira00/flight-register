from typing import List
from passenger import Passenger

class Flights:
    def __init__(self, identifier: int, departure: str, destination: str,
                 schedule_time: str, price: int,
                 seats_avaible: List[str] = None, passenger: List[Passenger] = None):

        self.identifier = identifier
        self.departure = departure
        self.destination = destination
        self.schedule_time = schedule_time
        self.price = price
        self.seats_avaible = seats_avaible or []
        self.passenger = passenger or []

    def to_json_object(self):
        return {
            "id": self.identifier,
            "departure": self.departure,
            "destination": self.destination,
            "schedule_time": self.schedule_time,
            "price": self.price,
            "seats": self.seats_avaible,
            "passengers": [p.json_dump() for p in self.passenger]
        }

    def get_short_info(self):
        return {
            "departure": self.departure,
            "destination": self.destination,
            "price": self.price
        }
