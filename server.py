# server.py
from flask import Flask, render_template, url_for, request, redirect
import feedparser
import logging

#アプリケーションの起動
app = Flask(__name__)

#表示用のメソッド
def show(rss_urls):
		RSS_URLs = rss_urls
		entry = []
		feed_dics = []
		for RSS_URL in RSS_URLs:
				feed_dic = feedparser.parse(RSS_URL)
				feed_dics.append(feed_dic)
				for feed_dic in feed_dics:
						for entries in feed_dic.entries:
								entry.append(entries)
		return entry

#時系列順に並び替える
def sort_by_time(entry):
	entry = entry
	sorted_entry = []
	for entry in entry:
		sorted_entry.append(entry)
	return sorted(sorted_entry, key=lambda x: x["updated"], reverse=True)

#RSS_URLsを宣言
RSS_URLs = ["https://www.osaka-u.ac.jp/ja/event_rss"]

#トップページのメソッド
@app.route("/", methods=["GET"])
def index():
		entry = show(RSS_URLs)
		sorted_entry = sort_by_time(entry)
		return render_template("index.html", entry= entry, sorted_entry = sorted_entry)

@app.route("/search", methods=["POST"])
def search():
	  #フォームで送信されたRSSのURLをRSS_URLsに付け足す
		result = request.form["text"]
		RSS_URLs.append(result)
		entry = show(RSS_URLs)
		#例外処理
		#try
#		print(entry)
#		except Exception as e:
#				return render_template("index.html", e=e)
		sorted_entry = sort_by_time(entry)
		return render_template("index.html", entry= entry, sorted_entry = sorted_entry)

#存在しないページに対しての処理
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.debug = True #本番環境ではFalseにする
    app.run(host="0.0.0.0", port=8888)
