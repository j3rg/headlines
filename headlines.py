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

RSS_FEED = {'hacking': 'https://rss.packetstormsecurity.com/news/tags/hacking',
            'dos': 'https://rss.packetstormsecurity.com/files/tags/denial_of_service/',
            'code_exec': 'https://rss.packetstormsecurity.com/files/tags/code_execution/',
            'encryption': 'https://rss.packetstormsecurity.com/files/tags/encryption/',
            'exploit': 'https://rss.packetstormsecurity.com/files/tags/exploit/'}

def get_weather(query):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=97931e3b253b78925314710b42497ae0"
    query = urllib.quote(query)
    url = api_url.format(query)
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

@app.route("/", methods=['GET','POST'])
def get_news():
    query = request.form.get("publication")
    if not query or query.lower() not in RSS_FEED:
        publication = "hacking"
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEED[publication])
    weather = get_weather("Belize City,Belize")
    return render_template("home.html",articles=feed['entries'],weather=weather)
if __name__ == '__main__':
    app.run(port=5000,debug=True)
