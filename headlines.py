#!/usr/bin/env python
# coding=utf-8

import feedparser
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

RSS_FEED = {'hacking': 'https://rss.packetstormsecurity.com/news/tags/hacking',
            'dos': 'https://rss.packetstormsecurity.com/files/tags/denial_of_service/',
            'code_exec': 'https://rss.packetstormsecurity.com/files/tags/code_execution/',
            'encryption': 'https://rss.packetstormsecurity.com/files/tags/encryption/',
            'exploit': 'https://rss.packetstormsecurity.com/files/tags/exploit/'}

@app.route("/", methods=['GET','POST'])
def get_news():
    query = request.form.get("publication")
    if not query or query.lower() not in RSS_FEED:
        publication = "hacking"
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEED[publication])
    return render_template("home.html",articles=feed['entries'])
if __name__ == '__main__':
    app.run(port=5000,debug=True)
