from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, ImageMessage

import os
import uuid

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

@app.route("/")
def home():
    return "LINE Bot is running!"

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    ext = "jpg"
    file_name = f"{uuid.uuid4()}.{ext}"
    folder = "images"

    if not os.path.exists(folder):
        os.makedirs(folder)

    with open(os.path.join(folder, file_name), "wb") as f:
        for chunk in message_content.iter_content():
            f.write(chunk)

    print(f"Image saved: {file_name}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
