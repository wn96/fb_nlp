import requests

USER_URL = 'https://www.facebook.com/weineng.a/' # your link
ACCESS_TOKEN = 'EAACEdEose0cBAAVHtR8WdaKGKNL2e0ovbO6kVi1NUrarwQHU9SRSALvcy99bUeEqxTAIH0tv2y2KPSYpL5d54MoQmPzi0z0HiWQwLa8UPozhANnVhkhab8MMiNq4sGsnHzvM1aO9syLTXmPf4FwEXAVqf3cMid20ScqYK4kbJnKlmpw4l9kOZB2cH4QFWoWfdv3lcRwZDZD'


def get_id(USER_URL):
    params= {'id': USER_URL,'access_token': ACCESS_TOKEN}
    fb_graph = "https://graph.facebook.com/v3.0/"

    r = requests.get(fb_graph, params=params)
    fb_id = r.json().get('id')
    if type(fb_id) != int:
        return "0"
    return fb_id
