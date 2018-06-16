import json
import time
import urllib
import requests
from dbhelper import DBHelper
from config import *
import get_stats
from url_json_helper import *
import facebook_id

db = DBHelper()
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_updates(offset=None):
    try:
        url = URL + "getUpdates"
        if offset:
            url += "?offset={}".format(offset)
        js = get_json_from_url(url)
        return js
    except Exception as e:
        print("ERROR HAS OCCURED IN GET_UPDATES", e)

def send_message(text, chat_id, reply_markup=None):
    text = urllib.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)

def check_invalid(url):
    return url[:25] != 'https://www.facebook.com/' or get_post(url) == 0

def get_post(fb_url):
    if fb_url.split('/')[-1].isdigit():
        return fb_url.split('/')[-1]
    elif fb_url.split('/')[-2].isdigit():
        return url.split('/')[-2]
    else:
        return 0

def get_userid(fb_url):
    a = fb_url[25:]
    return a.split('/')[0]

def handle_updates(updates):
    for update in updates["result"]:
        #try:
            if "message" not in update:
                continue
            if "chat" not in update["message"]:
                continue
            if "text" not in update["message"]:
                continue

            chat = update["message"]["chat"]["id"]
            text = update["message"]["text"]
            items = db.get_items(chat)  ##
            if text == "/start":
                send_message("YAY",chat)

            elif text[:6] == "/token":
                input_url = text[7:]
                if text == "/token":
                    send_message("Please add your facebook token.",chat)
                elif False:
                    send_message("You have entered an invalid Token",chat)
                else:
                    #Adding from here
                    items = db.get_items(chat)
                    code = text[7:]

                    if items:
                        db.delete_all(chat)
                        db.add_item(code, chat)
                        send_message("Token has been replaced", chat)

                    else:
                        db.add_item(code, chat)
                        send_message("Token has been added", chat)

            elif text[:2] == "/s":
                input_url = text[3:]
                #Exception Handling
                if text == "/s":
                    send_message("Please type '/s <facebook link>' to check sentiments.",chat)
                elif check_invalid(input_url):
                    send_message("You have entered an invalid facebook URL.\nInput needs to be of form https://www.facebook.com/<username>/posts/<postid>", chat)
                else:
                    token = db.get_items(chat)
                    if token:
                        code = token[0]
                        post_code = get_post(input_url)
                        user_code = facebook_id.get_id(get_userid(input_url), code)
                        result = print_summary(*(get_stats.sentiments_output(code, graph_api_version, user_code, post_code, limit)))
                        send_message(result, chat)
                        #send_message("Your token has expired. If the problem persist, you're fucked.", chat)

            elif text[:4] == '/del':
                db.delete_all(chat)
                send_message("Token has been deleted", chat)

        except Exception as e:
            send_message("An error has occured! Please try again. If the problem persist, please email support at weineng.a@gmail.com!",chat)
            print("ERROR has occured: ", e)
            print(str(update).encode("utf-8", errors='ignore'))
            print()


def main():
    db.setup()
    last_update_id = None
    users_add = list()
    print("Starting Facebook Sentiment Analysis")
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)

def print_summary(positive_count, neutral_count, negative_count, failed, count):
    positive_count = float(positive_count)
    neutral_count = float(neutral_count)
    negative_count = float(negative_count)
    failed = float(failed)
    count = float(count)

    a = ('Total comments analysed: {}\n'.format(count))
    b = ('Positive : {} ({:.0%})\n'.format(positive_count, positive_count / count))
    c = ('Negative : {} ({:.0%})\n'.format(negative_count, negative_count / count))
    d = ('Neutral : {} ({:.0%}))\n'.format(neutral_count, neutral_count / count))
    e = ('Failed : {} ({:.0%}))'.format(failed, failed / count))
    return a + b + c + d + e

if __name__ == '__main__':
    main()
