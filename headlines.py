#!/usr/bin/env python
# coding=utf-8

import feedparser
import json
import urllib
import urllib2
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

RSS_FEEDS = {'hacking': 'https://rss.packetstormsecurity.com/news/tags/hacking',
            'dos': 'https://rss.packetstormsecurity.com/files/tags/denial_of_service/',
            'code_exec': 'https://rss.packetstormsecurity.com/files/tags/code_execution/',
            'encryption': 'https://rss.packetstormsecurity.com/files/tags/encryption/',
            'exploit': 'https://rss.packetstormsecurity.com/files/tags/exploit/'}

DEFAULTS = {'publication':'hacking',
            'city':'Belize City,Belize'}

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=97931e3b253b78925314710b42497ae0"

@app.route("/")
def home():
    # get customized headlines based on user input or default
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)
    # get customized weather based on user input or default
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
    return render_template("home.html", articles=articles, weather=weather)

def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publications']
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']

def get_weather(query):
    query = urllib.quote(query)
    url = WEATHER_URL.format(query)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description":
                   parsed["weather"][0]["description"],
                   "temperature":parsed["main"]["temp"],
                   "city":parsed["name"]
                   }
        return weather

if __name__ == '__main__':
    app.run(port=5000,debug=True)
