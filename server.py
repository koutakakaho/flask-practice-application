# server.py
from flask import Flask, render_template, url_for, request, redirect
import feedparser
import logging
from datetime import datetime as dt

#アプリケーションの起動
app = Flask(__name__)


def parseDate(dateData):  
	if dateData == None or dateData == "<":
		return dt(2010,1,1,0,0,0)
	elif dateData == "<":
		return None
	else:
		return dt(  
			dateData.tm_year,  
			dateData.tm_mon,  
			dateData.tm_mday,  
			dateData.tm_hour,  
			dateData.tm_min,  
			dateData.tm_sec  
		)  

#発行者
def in_key(entry, key):
	if key in entry:
		return entry[key]
	else:
		return "unknown"
	
#表示用のメソッド
def show(rss_urls):
	RSS_URLs = rss_urls
	entry = []
	feed_dics = []
	for RSS_URL in RSS_URLs:
		feed_dic = feedparser.parse(RSS_URL)
		for entries in feed_dic.entries:
			entry.append(entries)
	# showメソッドの返り値はリスト
	return entry

#時系列順に並び替える
def sort_by_time(entries):
	entries = [{  
			'title': entry['title'],  
			'link': entry['link'],  
			'date': parseDate(entry['updated_parsed'] or entry['published_parsed']), 
			"publisher": in_key(entry, "publisher")
		} 
			for entry in entries ]
	print([entry["date"] for entry in entries])
	return sorted(entries, key=lambda x: x["date"], reverse=True)

#RSS_URLsを宣言
RSS_URLs = ["https://www.osaka-u.ac.jp/ja/event_rss","http://www.tuat.ac.jp/event/rss.xml","https://www.titech.ac.jp/alumni/event/rss.xml","https://www.tcu.ac.jp/news/all/feed/"]

#トップページのメソッド
@app.route("/", methods=["GET"])
def index():
		entry = show(RSS_URLs)
		sorted_entry = sort_by_time(entry)
		
		#sorted_entryの上位5件のみを取得
		entry_top5 = sorted_entry[:5]
		return render_template("index.html", entry_top5= entry_top5, sorted_entry = sorted_entry)

@app.route("/search", methods=["POST"])
def search():
	  #フォームで送信されたRSSのURLをRSS_URLsに付け足す
		result = request.form["text"]
		RSS_URLs.append(result)
		entry = show(RSS_URLs)
		
		sorted_entry = sort_by_time(entry)
		return render_template("index.html", entry= entry, sorted_entry = sorted_entry)

#存在しないページに対しての処理
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.debug = True #本番環境ではFalseにする
    app.run(host="0.0.0.0", port=8888)
