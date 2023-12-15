from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import requests
from bs4 import BeautifulSoup
import pandas as pd
import pygsheets

app = Flask(__name__)  

line_bot_api = LineBotApi('U5hlah8NxPTDI61P6+cqf+sVBTJixlenSE/ihCGVYVRf0kbVGUMP57qOBpxxzTIIeXdWvX5dnF6jXdOP/mASdmTKiV/XM5qbRVUHn0DvXckVqNVTBo/A+zT+v+NHTr7li4fjHgwFT8JgvFBDVYZjOAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('1b59f7e2aae7872e0ec20799920c474b')

gc = pygsheets.authorize(service_account_file='./gsheet.json')
sht = gc.open_by_url('https://docs.google.com/spreadsheets/d/1cxvkIggrRHYnZy0oUH-leCFHy3gWdJGEi7XC3i1Hv3c/edit#gid=0')

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
        reply = wks.get_as_df()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply))

@app.route("/")
def home():
    return 'Hello World'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
