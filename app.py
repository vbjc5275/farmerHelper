from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler, exceptions)
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, JoinEvent, LeaveEvent, TextMessage, TextSendMessage
)
from crawl_price import search
app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('ruvd8tZiM9BiKr9rpqgetNJyeCEgEM8l4UbdjMrR7CM+DXQrsMVYAbgAdWZYLHnKPmxbLq5jjESMBhX14eGYMQtSMs5h3xQi8g/4uCxHeUqFxhHF14UVfN//lldsftfPp20IeFERPPlmejHp3lyH1AdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('77ad723a1f785d8445f5e093e7250751')
#my USER ID
myUserID = "Uebe55ea95668d1268b787fdf1d5706ea"


# 監聽所有來自 /callback 的 Post Request
@app.route("/index", methods=['GET'])
def Hello():
    return 'SUCCESS!'

# 監聽所有來自 /callback 的 Post Request
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

@handler.add(JoinEvent,message=TextMessage)
def handle_join(event):
    newcoming_text = "主人好，奴才願意為您肝腦塗地!"

    line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text=newcoming_text)
        )


#訊息傳遞區塊
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):  

    def reply(text):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text)
        )

    def push(id_, text):
        line_bot_api.push_message(id_,TextSendMessage(text))

    ###抓到顧客的資料 ###
    #profile = line_bot_api.get_profile(event.source.user_id)
    #nameid = profile.display_name #使用者名稱
    #uid = profile.user_id #使用者ID

    #群組聊天
    #uid = event.source.group_id
    if hasattr(event.source, 'group_id'):
        uid = event.source.group_id
    elif hasattr(event.source, 'room_id'):
        uid = event.source.room_id
    else:
        uid = event.source.user_id

    userspeak=str(event.message.text).strip() #使用者講的話
   
#####################################系統功能按鈕##############################
    if userspeak == "小琳":
        push(uid, "主子有什麼吩咐?")

    elif userspeak.startswith("查"):
        push(uid, "讓奴才找找...")
        date = userspeak.split(" ")[1]
        product_name = userspeak.split(" ")[2]

        item = ["產品","上價","中價","下價","平均價","跟前一日交易日比較%","交易量(公斤)","跟前一日交易日比較%"]
        content = search(date,market_name="台北一",product_name=product_name)
        
        #content字串表示有誤
        if isinstance(content, str):
            push(uid,content)
            return

        print (item,content)
        if len(item)!=len(content):
            push(uid, "奴才辦事無力，請秉誠主子查查原因!")
            return "ok"

        output = ""
        for i,it in enumerate(item):
            output = output+f'{it}:{content[i]}\n'

        push(uid,output)

    elif userspeak in ["小琳謝謝","小琳謝了"]:
        push(uid,"奴才不敢當")

    elif userspeak in ["小琳退下"]:
        push(uid,"渣")



import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 27017))
    app.run(host='0.0.0.0', port=port)
    #app.run(debug=True,port=5000)





