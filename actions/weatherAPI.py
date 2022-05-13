import requests, json

# Enter your API key here
api_key = "b3e485529ed2c733498ae97ba1efbc9b"

base_url = "http://api.openweathermap.org/data/2.5/weather?"


def get_weather(city_name):
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name

    response = requests.get(complete_url)

    x = response.json()
    print(x)

    if x["cod"] != "404":

        y = x["main"]

        # store the value corresponding
        # to the "temp" key of y
        current_temperature = y["temp"]

        # store the value corresponding
        # to the "pressure" key of y
        current_pressure = y["pressure"]

        # store the value corresponding
        # to the "humidity" key of y
        current_humidity = y["humidity"]

        # store the value of "weather"
        # key in variable z
        z = x["weather"]

        # store the value corresponding
        # to the "description" key at
        # the 0th index of z
        weather_description = z[0]["description"]

        # print following values
        # print(" Temperature (in kelvin unit) = " +
        #       str(current_temperature) +
        #       "\n atmospheric pressure (in hPa unit) = " +
        #       str(current_pressure) +
        #       "\n humidity (in percentage) = " +
        #       str(current_humidity) +
        #       "\n description = " +
        #       str(weather_description))
        return weather_description

    else:
        print(" City Not Found ")
        return "sunny"


if __name__ == "__main__":
    get_weather("chennai")