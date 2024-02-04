from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather_v2.db'
db = SQLAlchemy()
db.init_app(app)

class Weather(db.Model):
    __tablename__ = 'weather'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    temp = db.Column(db.Float, nullable=False)
    feels_like = db.Column(db.Float, nullable=False)
    temp_min = db.Column(db.Float, nullable=False)
    temp_max = db.Column(db.Float, nullable=False)
    pressure = db.Column(db.Integer, nullable=True)
    humidity = db.Column(db.Integer, nullable=True)
    clouds_all = db.Column(db.Integer, nullable=True)
    wind = db.relationship("Wind", back_populates="weather")
    wind_id = db.Column(db.Integer, db.ForeignKey('wind.wind_id'))
    rain = db.relationship("Rain", back_populates="weather")
    rain_id = db.Column(db.Integer, db.ForeignKey('rain.rain_id'))
    snow = db.relationship("Snow", back_populates="weather")
    snow_id = db.Column(db.Integer, db.ForeignKey('snow.snow_id'))
    location = db.relationship("Location", back_populates="weather")
    location_id = db.Column(db.Integer, db.ForeignKey('location.location_id'))
    
    def __init__(self, time, description, temp, feels_like, temp_min, temp_max, pressure, humidity, clouds_all):
        self.time = time
        self.description = description
        self.temp = temp
        self.feels_like = feels_like
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.pressure = pressure
        self.humidity = humidity
        self.clouds_all = clouds_all
        
class Wind(db.Model):
    __tablename__ = 'wind'
    wind_id = db.Column(db.Integer, primary_key=True)
    speed = db.Column(db.Float, nullable=True)
    deg = db.Column(db.Float, nullable=True)
    gust = db.Column(db.Float, nullable=True)
    weather = db.relationship("Weather", back_populates="wind")
    

class Rain(db.Model):
    __table_name__ = 'rain'
    rain_id = db.Column(db.Integer, primary_key=True)
    rain_1hr = db.Column(db.Float, nullable=True)
    rain_3hr = db.Column(db.Float, nullable=True)
    weather = db.relationship("Weather", back_populates="rain")
class Location(db.Model):
    __table_name__ = 'location'
    location_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    weather = db.relationship("Weather", back_populates="location")
class Snow(db.Model):
    __table_name__ = 'rain'
    snow_id = db.Column(db.Integer, primary_key=True)
    snow_1hr = db.Column(db.Float, nullable=True)
    snow_3hr = db.Column(db.Float, nullable=True)
    weather = db.relationship("Weather", back_populates="snow")
    

def update_weather_db(data):
    new_weather = Weather(**data['main'])
    new_weather.location = Location(name=data['location'])
    # update wind
    if 'wind' in data.keys():
        new_weather.wind = Wind(**data['wind'])
    else:
        new_weather.wind_id=1
    # update rain
    if 'rain' in data.keys():
        new_weather.rain = Rain(**data['rain'])
    else:
        new_weather.rain_id=1
    # update snow
    if 'snow' in data.keys():
        new_weather.snow = Snow(**data['snow'])
    else:
        new_weather.snow_id=1
        
    with app.app_context():
        db.session.add(new_weather)
        db.session.commit()

def query_location_table():
    with app.app_context():
        unique_locations = db.session.query(Location.location_id, Location.name).group_by(Location.name).all()
        print(unique_locations)


query_location_table()
if __name__=='__main__':
    with app.app_context():
        db.create_all()
