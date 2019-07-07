# server.py
from flask import Flask, render_template, url_for, request
import feedparser


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
		RSS_URLs = ["https://www.osaka-u.ac.jp/ja/news_rss"]	
		entry = []
		feed_dics = []
		if request.method == "GET":
				for RSS_URL in RSS_URLs:
						feed_dic = feedparser.parse(RSS_URL)
						feed_dics.append(feed_dic)
						for feed_dic in feed_dics:
								for entries in feed_dic.entries:
										entry.append(entries)
				return render_template("index.html", entry= entry)
    
		else:
	  #フォームで送信されたRSSのURLをRSS_URLsに付け足す
		#ここDRYにしたいなぁ
				result = request.form
				RSS_URLs.append(result)
				for RSS_URL in RSS_URLs:
						feed_dic = feedparser.parse(RSS_URL)
						feed_dics.append(feed_dic)
						for feed_dic in feed_dics:
								for entries in feed_dic.entries:
										entry.append(entries)
				return render_template("index.html", entry= entry)

if __name__ == "__main__":
    app.debug = False #本番環境ではFalseにする
    app.run(host="0.0.0.0", port=8888)
