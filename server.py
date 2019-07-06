# server.py
from flask import Flask, render_template
import feedparser


app = Flask(__name__)

@app.route("/")
def hello_name():
    RSS_URLs = ["https://www.osaka-u.ac.jp/ja/event_rss", "https://www.osaka-u.ac.jp/ja/misc/ja/event_rss?target=all", "http://www.todainavi.jp/feed/atom/", "https://www.careersupport.adm.u-tokyo.ac.jp/index.php?option=com_jevents&task=modlatest.rss&format=feed&type=rss&modid=139"]
    feed_dics = []
    for RSS_URL in RSS_URLs:
        feed_dic = feedparser.parse(RSS_URL)
        feed_dics.append(feed_dic)
    return render_template("index.html", feed_dics= feed_dics)
    
if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=8888)