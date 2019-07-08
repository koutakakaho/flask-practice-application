# server.py
from flask import Flask, render_template, url_for, request, redirect
import feedparser
import logging

app = Flask(__name__)

#表示用のメソッド
def show(rss_urls):
		RSS_URLs = rss_urls
		entry = []
		feed_dics = []
		for RSS_URL in RSS_URLs:
				feed_dic = feedparser.parse(RSS_URLs)
				feed_dics.append(feed_dic)
				for feed_dic in feed_dics:
						for entries in feed_dic.entries:
								entry.append(entries)
		print("エントリー{}, {}".format(entry, RSS_URLs))
		
		return entry

#トップページのメソッド
@app.route("/", methods=["GET"])
def index():
		RSS_URLs = ["https://www.osaka-u.ac.jp/ja/event_rss"]
		entry = show(RSS_URLs)
		return render_template("index.html", entry= entry)

@app.route("/search", methods=["POST"])
def search():
	  #フォームで送信されたRSSのURLをRSS_URLsに付け足す
		result = request.form["text"]
		RSS_URLs = [result]
		
		entry = []
		feed_dics = []
		for RSS_URL in RSS_URLs:
				feed_dic = feedparser.parse(RSS_URLs)
				feed_dics.append(feed_dic)
				for feed_dic in feed_dics:
						for entries in feed_dic.entries:
								entry.append(entries)
								
		#例外処理
		#try
#		entry = show(RSS_URLs)
#		print(entry)
#		except Exception as e:
#				return render_template("index.html", e=e)
		return render_template("index.html", entry= entry)

#存在しないページに対しての処理
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.debug = True #本番環境ではFalseにする
    app.run(host="0.0.0.0", port=8888)
