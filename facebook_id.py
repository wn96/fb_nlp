import requests

def get_id(USER_URL, access_token):
    params= {'id': USER_URL,'access_token': access_token}
    fb_graph = "https://graph.facebook.com/v3.0/"

    r = requests.get(fb_graph, params=params)
    fb_id = r.json().get('id')
    return fb_id if fb_id else 0
