from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

app = Flask(__name__)  
line_bot_api = LineBotApi('U5hlah8NxPTDI61P6+cqf+sVBTJixlenSE/ihCGVYVRf0kbVGUMP57qOBpxxzTIIeXdWvX5dnF6jXdOP/mASdmTKiV/XM5qbRVUHn0DvXckVqNVTBo/A+zT+v+NHTr7li4fjHgwFT8JgvFBDVYZjOAdB04t89/1O/w1cDnyilFU=')  
handler = WebhookHandler('1b59f7e2aae7872e0ec20799920c474b')

line_bot_api.push_message('你自己的ID', TextSendMessage(text='你可以開始了'))

@app.route("/callback", methods=['POST']) 
def callback():     
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
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))

if __name__ == "__main__":
    app.run()
