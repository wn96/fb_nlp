import requests
import signal
import sys

def get_comments(access_token, graph_api_version, user_id, post_id, limit=0):
    comments = []

    url = 'https://graph.facebook.com/{}/{}_{}/comments'.format(graph_api_version, user_id, post_id)

    # register a signal handler so that we can exit early
    def signal_handler(signal, frame):
        print('KeyboardInterrupt')
        sys.exit(0)


    signal.signal(signal.SIGINT, signal_handler)

    r = requests.get(url, params={'access_token': access_token})
    while True:
        data = r.json()

        # catch errors returned by the Graph API
        if 'error' in data:
            raise Exception(data['error']['message'])

        # append the text of each comment into the comments list
        for comment in data['data']:
            # remove line breaks in each comment
            text = comment['message'].replace('\n', ' ')
            comments.append(text)

        print('Got {} comments, total: {}'.format(len(data['data']), len(comments)))

        # check if we have enough comments
        if 0 < limit <= len(comments):
            break

        # check if there are more comments
        if 'paging' in data and 'next' in data['paging']:
            r = requests.get(data['paging']['next'])
        else:
            break
    return comments
