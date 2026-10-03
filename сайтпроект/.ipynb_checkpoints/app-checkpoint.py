import requests
from flask import Flask, render_template, request

API_KEY = "eb4aef3a7bc85c912c1ac4c47d61ab7d"

app = Flask(__name__)


def get_weather(city_name):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru"
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
        if r.status_code != 200:
            return {"error": data.get("message", "Неизвестная ошибка")}
        return {
            "city": city_name.capitalize(),
            "temp": round(data["main"]["temp"], 1),
            "feels_like": round(data["main"]["feels_like"], 1),
            "description": data["weather"][0]["description"].capitalize()
        }
    except requests.exceptions.ConnectionError:
        return {"error": "Нет подключения к интернету"}
    except requests.exceptions.Timeout:
        return {"error": "Превышено время ожидания"}
    except Exception as e:
        return {"error": f"Непредвиденная ошибка: {e}"}


@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    if request.method == "POST":
        city = request.form.get("city", "").strip()
        if city:
            weather = get_weather(city)
        else:
            weather = {"error": "Введите название города"}
    return render_template("index.html", weather=weather)


if __name__ == "__main__":
    app.run(debug=True)