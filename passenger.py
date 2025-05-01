class Passenger:
    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email

    def json_dump(self):
        return {"Username: ": self.username,
                "Email: ": self.email}