import requests
import json
from bs4 import BeautifulSoup

#Yahoo! から天気情報を取得
yahoo_url = 'https://weather.yahoo.co.jp/weather/jp/21/5210.html'
response = requests.get(yahoo_url)
soup = BeautifulSoup(response.text, 'html.parser')
rs = soup.find(class_='forecastCity')
rs = [i.strip() for i in rs.text.splitlines()]
rs = [i for i in rs if i != ""]

furo_guid = ""
emoji_dict = {'晴れ': '🌞', '雨': '☔', '曇り': '☁', '晴時々曇': '🌤', '晴時々雨': '🌦️', '曇時々晴': '🌥', '曇時々雨': '🌧️', '雨時々曇': '🌧️', '晴のち曇': '🌞→☁', '晴のち雨': '🌞→☔', '曇のち晴': '☁→🌞', '曇のち雨': '☁→☔', '雨のち晴': '☔→🌞', '雨のち曇': '☔→☁'}

if rs[19] in emoji_dict:
  emoji_tomorrow = emoji_dict[f'{rs[19]}']
else:
  emoji_tomorrow = ''
 
if rs[19] in "晴れ" or rs[19] in "晴時々曇":
  furo_guid = "昼間にエコキュートの沸増しをするのがいいでしょう"
else:
  furo_guid = "夜中にエコキュートの沸増しをするのがいいでしょう"
  
tomorrow_weather = f"明日{rs[18]}の天気は {rs[19]}{emoji_tomorrow}\n最高気温は{rs[20]}\n最低気温は{rs[21]}です。\n{furo_guid} "

# 定数の定義
BROADCAST_URL = 'https://api.line.me/v2/bot/message/broadcast'
LINE_API_TOKEN = 'QoQxfASEg/BgE9c4az1crFJ/RAOPDKyg9FCdYpMgoKrpAYO6ywhgfJLWKB1wj6hiSQZ6RLBTNIifJhjo0+DzKATZ5S96ZAG8RpU5bY3ocuLgYppgO9Bbs2cO28MaBsnrKqyCEr7jmRd1cVE6MDOoFwdB04t89/1O/w1cDnyilFU='
# 送信準備
headers = {'Content-Type': 'application/json',
           'Authorization': f'Bearer {LINE_API_TOKEN}'}

payload_tomorrow = {'messages':[{'type': 'text',
			         'text': f'{tomorrow_weather}'
			      }
			    ]
	                  }
			  
# Line 送信
requests.post(BROADCAST_URL, headers=headers, data=json.dumps(payload_tomorrow))
