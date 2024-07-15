#requestsとBeautiful Soup のイン ポート
import requests 
from bs4 import BeautifulSoup
#csvのインポート
import csv
#datetimeのインポート
import datetime
import schedule
import time

#定期処理内容　Yahoo!ニュースの主要トピックスのタイトルとURLを取得
def job():
    #ターゲットURLの変数化
    url = "https://news.yahoo.co.jp/"

    # このあたりはおまじない！わからなくてもOK! 狙いのURLのhtmlをタグごとに解析します。
    r = requests.get(url)
    content_type_encoding = r.encoding if r.encoding != 'ISO-8859-1' else None
    soup = BeautifulSoup(r.content, 'html.parser', from_encoding=content_type_encoding)

    # Beautiful Soup の find() で、主要ニュースの部分のみを抽出します。
    today = soup.find("section", attrs ={"id":"uamods-topics"})

    # 記事のタイトルとURLがある部分を抽出
    entries = today.find_all("li")
    # CSV出力用リスト
    today_list = []
    index = 1

    # あるだけ情報を取得する
    for entry in entries:
        # "li"の箇所のタイトルに該当するテキスト（ページ上の文章）を取得
        title = entry.get_text()
        # "li"の箇所のURLを取得
        entry_url = entry.find("a").get("href")
        # 出力用リストにタイトルとURLを格納  
        today_list.append([index, str(title) ,entry_url])
        # インデックスをインクリメント
        index += 1 

    #print(today_list)

    # 現在時刻を取得
    dt_now = datetime.datetime.now()

    #結果をCSVファイルに書き出し。ファイル名は現在時刻
    with open(str(dt_now.year)+'_'+str(dt_now.month)+'_'+str(dt_now.day)+'_'+str(dt_now.hour)+str(dt_now.minute)+'_NewsTopics.csv', 'w', encoding='utf-8')as file:
        writer=csv.writer(file,lineterminator='\n')
        writer.writerows(today_list)


#1分毎のjob実行を登録　今回は1分毎だけ有効にしました。
schedule.every(1).minutes.do(job)

#2時間毎のjob実行を登録
#schedule.every(2).hours.do(job)

#AM5:00のjob実行を登録
#schedule.every().day.at("5:00").do(job)

#水曜日のjob実行を登録
#schedule.every().wednesday.do(job)

#登録したjobを実行。今回は無限ループで実行
while True:
    schedule.run_pending()
    time.sleep(10)