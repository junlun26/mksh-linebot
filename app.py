from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import requests
from bs4 import BeautifulSoup
import pandas as pd
import pygsheets
import json

app = Flask(__name__)  

line_bot_api = LineBotApi('U5hlah8NxPTDI61P6+cqf+sVBTJixlenSE/ihCGVYVRf0kbVGUMP57qOBpxxzTIIeXdWvX5dnF6jXdOP/mASdmTKiV/XM5qbRVUHn0DvXckVqNVTBo/A+zT+v+NHTr7li4fjHgwFT8JgvFBDVYZjOAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('1b59f7e2aae7872e0ec20799920c474b')

gc = pygsheets.authorize(service_account_file='./gsheet.json')
sht = gc.open_by_url('https://docs.google.com/spreadsheets/d/1cxvkIggrRHYnZy0oUH-leCFHy3gWdJGEi7XC3i1Hv3c/edit#gid=0')

flex_message = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "./mkjh icon.jpg",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "spacing": "md",
    "contents": [
      {
        "type": "text",
        "text": "",
        "size": "xl",
        "weight": "bold"
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "button",
        "style": "primary",
        "color": "#905c44",
        "margin": "xxl",
        "action": {
          "type": "uri",
          "label": "前往網站",
          "uri": ""
        }
      }
    ]
  }
}

def creat_columns(working_sheet):
    all_rows = working_sheet.get_all_values(returnas='matrix')
    non_empty_rows = 0
    for row in all_rows:
        if any(cell.strip() for cell in row):
            non_empty_rows += 1

    columns = []
    for i in range(2, non_empty_rows + 2):
        column = CarouselColumn(
            thumbnail_image_url = "https://www.mksh.phc.edu.tw/wp-content/uploads/sites/99/2022/05/%E6%A0%A1%E5%BE%BD.jpg",
            title = working_sheet.get_value("A" + str(i)),
            text = "",
            actions = [
                URIAction(label = "前往網站", uri = working_sheet.get_value("B" + str(i)))
            ]
        )
        columns.append(column)
    return columns
    
@app.route("/callback", methods=['OPTIONS', 'POST'])
def callback():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        return response
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    if text == "本周重要公告":
        wks = sht[0]
        #columns = creat_columns(wks)
        columns = CarouselColumn(
            thumbnail_image_url = "https://www.mksh.phc.edu.tw/wp-content/uploads/sites/99/2022/05/%E6%A0%A1%E5%BE%BD.jpg",
            title = wks.get_value("A2"),
            text = "",
            actions = [
                URIAction(label = "前往網站", uri = wks.get_value("B2"))
            ]
        )
        #flex_message["body"]["contents"][0]["text"] = wks.get_value("A2")
        #flex_message["footer"]["contents"][0]["action"]["uri"] = wks.get_value("B2")
        line_bot_api.reply_message(event.reply_token, TemplateSendMessage(alt_text = "多頁訊息", template = columns))
    elif text == "本月榮譽榜":
        wks = sht[1]
        columns = creat_columns(wks)
        line_bot_api.reply_message(event.reply_token, TemplateSendMessage(alt_text = "多頁訊息", template = columns))
    elif text == "活動、競賽資訊":
        wks = sht[2]
        columns = creat_columns(wks)
        line_bot_api.reply_message(event.reply_token, TemplateSendMessage(alt_text = "多頁訊息", template = columns))

@app.route("/")
def home():
    return 'Hello World'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
