import requests

SHEETY_PRICES_ENDPOINT = "https://api.sheety.co/d4f138debef89be56584e6403593bd0e/users/prices"
SHEETY_USERS_ENDPOINT = "https://api.sheety.co/d4f138debef89be56584e6403593bd0e/users/users"


class DataManager:

    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        print("hi")
        response = requests.get(url=SHEETY_PRICES_ENDPOINT)
        data = response.json()
        self.destination_data = data["prices"]
        print("bye")
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                json=new_data
            )
            print(response.text)

    def update_users(self, first_name, last_name, email):
        data = {
            "user": {
                "firstName": first_name,
                "lastName": last_name,
                "email": email
            }
        }
        response = requests.post(url=SHEETY_USERS_ENDPOINT, json=data)
        print(response.text)
