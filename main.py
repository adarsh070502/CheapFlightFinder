from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime, timedelta
import requests
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

ORIGIN_CITY_IATA = "HYD"

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()


class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')


class SearchButton(FlaskForm):
    search = SubmitField("Search")


@app.route("/", methods=["POST", "GET"])
def home():
    form = RegisterForm()

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        data_manager.update_users(first_name, last_name, email)
        return render_template("success.html")

    return render_template("index.html", form=form)


@app.route("/searching", methods=["POST", "GET"])
def search():
    form1 = SearchButton()

    if form1.validate_on_submit():

        sheet_data = data_manager.get_destination_data()
        print(sheet_data)

        if sheet_data[0]["iataCode"] == "":
            for row in sheet_data:
                row["iataCode"] = flight_search.get_destination_codes(row["city"])
            data_manager.destination_data = sheet_data
            data_manager.update_destination_codes()

        destinations = {
            data["iataCode"]: {
                "id": data["id"],
                "city": data["city"],
                "price": data["lowestPrice"]
            } for data in sheet_data}

        tomorrow = datetime.now() + timedelta(days=1)
        six_month_from_today = datetime.now() + timedelta(days=6 * 30)

        for destination_code in destinations:
            flight = flight_search.check_flights(
                ORIGIN_CITY_IATA,
                destination_code,
                from_time=tomorrow,
                to_time=six_month_from_today
            )
            if flight is None:
                continue

            if flight.price < destinations[destination_code]["price"]:
                message = f"Low price alert! Only Rupees: {flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."

                ######################
                if flight.stop_overs > 0:
                    message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."
                #######################

                notification_manager.send_sms(message)

                response = requests.get(url="https://api.sheety.co/d4f138debef89be56584e6403593bd0e/users/users")

                print("sending mails")
                for i in range(len(response.json()["users"])):
                    email = response.json()["users"][i]["email"]
                    notification_manager.send_emails(message=message, user_mails=email)
        return render_template("search.html", temp="true")
    return render_template("search.html", form1=form1, temp="false")


if __name__ == '__main__':
    app.run(debug=True)
