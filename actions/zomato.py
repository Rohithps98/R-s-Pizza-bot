from http import HTTPStatus

import requests


base_url = "https://developers.zomato.com/api/v2.1/"


class Zomato:
    def __init__(self):
        self.auth_token = "b7e67856bec959f132532eac43b379b4"

    def get_cities(self, city_name):
        url = base_url + "/cities?q=" + city_name
        try:
            raw_data = requests.get(url, headers={"user-key": self.auth_token, "Accept": "application/json"})
            if raw_data.status_code == HTTPStatus.OK:
                cities = raw_data.json()
                if len(cities.get("location_suggestions", [])) == 0:
                    return None
                else:
                    if cities.get("location_suggestions")[0]["name"].lower() == city_name.lower():
                        return cities.get("location_suggestions")[0]
        except Exception as e:
            print(e)

    def get_cuisines(self, city_id):
        url = base_url + "cuisines?city_id=" + str(city_id)
        try:
            raw_data = requests.get(url, headers={"user-key": self.auth_token, "Accept": "application/json"})
            if raw_data.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
                return None
            if raw_data.status_code == HTTPStatus.OK:
                cuisines = raw_data.json()
                # print(cuisines)
                if not cuisines and len(cuisines['cuisines']) == 0:
                    return None
                return cuisines["cuisines"]
        except Exception as e:
            print(e)

    def get_restaurant_details(self, location_id, cuisine_id):
        url = base_url + "search?entity_id={}&cuisines={}".format(location_id, cuisine_id)
        try:
            raw_data = requests.get(url, headers={"user-key": self.auth_token, "Accept": "application/json"})
            if raw_data.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
                return None
            if raw_data.status_code == HTTPStatus.OK:
                restaurant_details = raw_data.json()
                return restaurant_details
        except Exception as e:
            print(e)



if __name__ == "__main__":
    zom = Zomato()
    print(zom.get_cities("chennai"))
    import json
    print(zom.get_restaurant_details(10883, 82))