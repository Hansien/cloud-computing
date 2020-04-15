from __future__ import unicode_literals

import os
import sys
import redis

from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage, VideoMessage, FileMessage, StickerMessage, StickerSendMessage
)
from linebot.utils import PY3

# set google translate api
from google.cloud import translate_v2 as translate
import six
translate_client = translate.Client()
# translate_client = translate.Client().from_service_account_json(JSON.parse(os.getenv('GOOGLE_CREDENTIALS', None)))

app = Flask(__name__)

# set redis
redis_host = "redis-16080.c13.us-east-1-3.ec2.cloud.redislabs.com"
redis_pwd = "zxe4uRRBxbmQdukb2zR8QSdVItKyQ2uZ"
redis_port = "16080"

redis1 = redis.Redis(host=redis_host, password=redis_pwd, port=redis_port)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

# get google_application_credentials from environment variable
google_application_credentials = os.getenv(
    'GOOGLE_APPLICATION_CREDENTIALS', None)

# obtain the port that heroku assigned to this app.
heroku_port = os.getenv('PORT', None)

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if isinstance(event.message, TextMessage):
            handle_TextMessage(event)
        if isinstance(event.message, ImageMessage):
            handle_ImageMessage(event)
        if isinstance(event.message, VideoMessage):
            handle_VideoMessage(event)
        if isinstance(event.message, FileMessage):
            handle_FileMessage(event)
        if isinstance(event.message, StickerMessage):
            handle_StickerMessage(event)

        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

    return 'OK'

# test_input = {
#     "text": "So let us begin anew--remembering on both sides that civility is not a sign of weakness, and sincerity is always subject to proof. Let us never negotiate out of fear. But let us never fear to negotiate.",
#     "target": "zh"
# }

# if isinstance(test_input, six.binary_type):
#     test_input = test_input.decode('utf-8')

# Text can also be a sequence of strings, in which case this method
# will return a sequence of results for each text.
# result = translate_client.translate(
#     test_input['text'], target_language=test_input['target'])

# print(u'Text: {}'.format(result['input']))
# print(u'Translation: {}'.format(result['translatedText']))
# print(u'Detected source language: {}'.format(
#     result['detectedSourceLanguage']))

# Handler function for Text Message


def handle_TextMessage(event):
    lanFlag = "EN"

    if event.message.text.lower() == "use ch":
        lanFlag = "CH"
    elif event.message.text.lower() == "use en":
        lanFlag = "EN"

    # Case-insensitive full keyword matching
    if redis1.get(event.message.text.lower()) == None:
        msg = 'No Rusult, you can type "help" to get a list of commands!'
    else:
        msg = redis1.get(event.message.text.lower()).decode()

    # translate module
    if lanFlag != "EN":
        text_input = {
            "text": msg,
            "target": lanFlag
        }
        if isinstance(text_input, six.binary_type):
            text_input = text_input.decode('utf-8')
        result = translate_client.translate(
            text_input['text'], target_language=text_input['target'])
        msg = result['translatedText']
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(msg)
    )

# Handler function for Sticker Message


def handle_StickerMessage(event):
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id=event.message.package_id,
            sticker_id=event.message.sticker_id)
    )

# Handler function for Image Message


def handle_ImageMessage(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="Nice image!")
    )

# Handler function for Video Message


def handle_VideoMessage(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="Nice video!")
    )

# Handler function for File Message


def handle_FileMessage(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="Nice file!")
    )


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(host='0.0.0.0', debug=options.debug, port=heroku_port)
