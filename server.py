# server.py
from flask import Flask, render_template, url_for, request
import feedparser


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        RSS_URLs = ["https://www.osaka-u.ac.jp/ja/event_rss", "https://www.osaka-u.ac.jp/ja/misc/ja/event_rss?target=all", "http://www.todainavi.jp/feed/atom/", "https://www.careersupport.adm.u-tokyo.ac.jp/index.php?option=com_jevents&task=modlatest.rss&format=feed&type=rss&modid=139"]
        feed_dics = []
        entry = []
        for RSS_URL in RSS_URLs:
            feed_dic = feedparser.parse(RSS_URL)
            feed_dics.append(feed_dic)
        for feed_dic in feed_dics:
            for entries in feed_dic.entries:
                entry.append(entries)
        return render_template("index.html", entry= entry)
    else:
        return render_template("post.html")
if __name__ == "__main__":
    app.debug = False #本番環境ではFalseにする
    app.run(host="0.0.0.0", port=8888)