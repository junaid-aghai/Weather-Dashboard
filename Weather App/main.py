from flask import Flask, render_template, request
import requests


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", weather=None)



@app.route("/weather", methods=["POST"])
def get_weather():
    # 1. Get the city name from the HTML form input
    city_name = request.form.get("city")
    
    api_key = "3c8ccc97ec8e27049d7a1b8c94428010"
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'metric'
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if data["cod"] == 200:
            # Prepare data to send to your HTML template
            weather_data = {
                "city": data["name"],
                "temp": round(data["main"]["temp"]),
                "desc": data["weather"][0]["description"].title(),
                "humidity": data["main"]["humidity"],
                "wind": data["wind"]["speed"],
                "visibility": data.get("visibility", 0) / 1000, # Meters to KM
                "pressure": data["main"]["pressure"]
            }
            return render_template("index.html", weather=weather_data)
        else:
            error_msg = data.get("message", "City not found")
            return render_template("index.html", error=error_msg)

    except Exception as e:
        return render_template("index.html", error="Connection error")

if __name__ == "__main__":    
    app.run(debug=True)