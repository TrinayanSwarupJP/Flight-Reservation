from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Flight:
    def __init__(self, flight_from, flight_to, departure_date):
        self.flight_from = flight_from
        self.flight_to = flight_to
        self.departure_date = departure_date

    def __str__(self):
        return f"Flight from {self.flight_from} to {self.flight_to}, departing on {self.departure_date}"

class Passenger(db.Model):
    __tablename__ = 'passenger'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    passport = Column(String)
    passenger_type = Column(String)

    def __init__(self, name, email, passport, passenger_type):
        self.name = name
        self.email = email
        self.passport = passport
        self.passenger_type = passenger_type

    def calculate_ticket_price(self):
        if self.passenger_type == "Economy":
            return 80
        elif self.passenger_type == "Premium Economy":
            return 100
        elif self.passenger_type == "Business Class":
            return 180
        elif self.passenger_type == "First Class":
            return 280
        else:
            return 0

class EconomyPassenger(Passenger):
    def __init__(self, name, email, passport):
        super().__init__(name, email, passport, "Economy")

class PremiumEconomyPassenger(Passenger):
    def __init__(self, name, email, passport):
        super().__init__(name, email, passport, "Premium Economy")

class BusinessClassPassenger(Passenger):
    def __init__(self, name, email, passport):
        super().__init__(name, email, passport, "Business Class")

class FirstClassPassenger(Passenger):
    def __init__(self, name, email, passport):
        super().__init__(name, email, passport, "First Class")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/flight_details', methods=['POST'])
def flight_details():
    flight_from = request.form.get('flight_from')
    flight_to = request.form.get('flight_to')
    departure_date = request.form.get('departure_date')
    flights = [
        {"name": "Flight 1", "departure": flight_from, "departure_time": "10:10 am", "destination": flight_to, "destination_time": "11:00 am", "date": departure_date},
        {"name": "Flight 2", "departure": flight_from, "departure_time": "4:00 pm", "destination": flight_to, "destination_time": "4:50 pm", "date": departure_date}
    ]
    return render_template('flight_details.html', flights=flights)

@app.route('/flight_reservation', methods=['GET', 'POST'])
def flight_reservation():
    if request.method == 'POST':
        return render_template('flight_reservation.html')

@app.route('/booking_confirmation', methods=['POST'])
def booking_confirmation():
    passenger_name = request.form.get('passenger_name')
    passenger_email = request.form.get('passenger_email')
    passenger_passport = request.form.get('passenger_passport')
    passenger_type = request.form.get('passenger_type')
    
    passenger = Passenger(name=passenger_name, email=passenger_email, passport=passenger_passport, passenger_type=passenger_type)

    
    return render_template('booking_confirmation.html', passenger=passenger)



@app.route('/passenger_details', methods=['POST'])
def passenger_details():
    return render_template('passenger_details.html')


@app.route('/process_payment', methods=['POST'])
def process_payment():
    return render_template('process_payment.html')



if __name__ == "__main__":
    app.run(debug=True)
