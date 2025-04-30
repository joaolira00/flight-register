class Flights:
    def __init__(self, identifier: int, departure: str, destination: str, schedule_time: int, price: int, seats_avaible: str = []):
        self.identifier = identifier
        self.departure = str(departure)
        self.destination = str(destination)
        self.schedule_time = schedule_time
        self.price = price
        self.seats_avaiable = seats_avaible

    def to_json_object(self):
        return {"Id: ": self.identifier,
                "Departure: ": self.departure,
                "Destination: ": self.destination,
                "Schedule Time: ": self.schedule_time,
                "Price: ": self.price,
                "Seats: ": self.seats_avaiable}