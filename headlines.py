#!/usr/bin/env python
# coding=utf-8

import feedparser
from flask import Flask

app = Flask(__name__)

PS_FEED = {'hacking': 'https://rss.packetstormsecurity.com/news/tags/hacking',
           'dos': 'https://rss.packetstormsecurity.com/files/tags/denial_of_service/',
           'code_exec': 'https://rss.packetstormsecurity.com/files/tags/code_execution/',
           'encryption':'https://rss.packetstormsecurity.com/files/tags/encryption/',
           'exploit':'https://rss.packetstormsecurity.com/files/tags/exploit/'}

@app.route("/")
@app.route("/<publication>")
def get_news(publication="hacking"):
    feed = feedparser.parse(PS_FEED[publication])
    first_article = feed['entries'][0]
    return """<html>
        <body>
            <h1> Packet Storm Headlines </h1>
            <b>{0}</b> <br/>
            <i>{1}</i> <br/>
            <p>{2}</p> <br/>
        </body>
    </html>""".format(first_article.get("title"), first_article.get("published"), first_article.get("summary"))

if __name__ == '__main__':
    app.run(port=5000,debug=True)
