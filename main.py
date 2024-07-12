from flask import Flask, render_template, url_for, request, redirect
from flask_bootstrap import Bootstrap5
import os
import requests
from dotenv import load_dotenv
app = Flask(__name__)
SECRET_KEY = os.urandom(32)
load_dotenv()
api_key = os.getenv('API_KEY')
app.config['SECRET_KEY'] = SECRET_KEY
bootstrap = Bootstrap5(app=app)
API_KEY = api_key

@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        try:
            country = request.form.get('city')
            geocoding_url = f'http://api.openweathermap.org/geo/1.0/direct?q={country}&limit=5&appid={API_KEY}'
            response = requests.get(url=geocoding_url)
            data = response.json()
            lat = data[0]['lat']
            lon = data[0]['lon']
        except IndexError:
            return render_template('notfound.html', country=country)
        print(lat, lon)
        weather_endpoint = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'
        response = requests.get(url=weather_endpoint)
        data = response.json()
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        print(data)
        return redirect(url_for('info', feels_like=feels_like, temp=temp, country=country, humidity=humidity))

    return render_template('index.html')

@app.route('/info')
def info():
    feels_like = request.args.get('feels_like')
    temp = request.args.get('temp')
    country = request.args.get('country')
    humidity = request.args.get('humidity')
    return render_template('info.html', feels_like=feels_like, temp=temp, country=country, humidity=humidity)

if __name__ == '__main__':
    app.run(debug=True)