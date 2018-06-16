import requests
import signal
import sys

from google.cloud import language
from google.api_core.exceptions import InvalidArgument

# create a Google Cloud Natural Languague API Python client
client = language.LanguageServiceClient()


graph_api_version = 'v3.0'
access_token = 'EAACEdEose0cBAAVHtR8WdaKGKNL2e0ovbO6kVi1NUrarwQHU9SRSALvcy99bUeEqxTAIH0tv2y2KPSYpL5d54MoQmPzi0z0HiWQwLa8UPozhANnVhkhab8MMiNq4sGsnHzvM1aO9syLTXmPf4FwEXAVqf3cMid20ScqYK4kbJnKlmpw4l9kOZB2cH4QFWoWfdv3lcRwZDZD'

# LHL's Facebook user id
user_id = '125845680811480'

# the id of LHL's response post at https://www.facebook.com/leehsienloong/posts/1505690826160285
post_id = '1900755973320433'

# the graph API endpoint for comments on LHL's post
url = 'https://graph.facebook.com/{}/{}_{}/comments'.format(graph_api_version, user_id, post_id)

comments = []

# set limit to 0 to try to download all comments
limit = 200

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

# a function which takes a block of text and returns its sentiment and magnitude
def detect_sentiment(text):
    """Detects sentiment in the text."""

    document = language.types.Document(
        content=text,
        type=language.enums.Document.Type.PLAIN_TEXT)

    sentiment = client.analyze_sentiment(document).document_sentiment

    return sentiment.score, sentiment.magnitude


# keep track of count of total comments and comments with each sentiment
count = 0
positive_count = 0
neutral_count = 0
negative_count = 0


def print_summary():
    print()
    print('Total comments analysed: {}'.format(count))
    print('Positive : {} ({:.2%})'.format(positive_count, positive_count / count))
    print('Negative : {} ({:.2%})'.format(negative_count, negative_count / count))
    print('Neutral  : {} ({:.2%})'.format(neutral_count, neutral_count / count))
    print('Failed   : {} ({:.2%})'.format(failed, failed / count))


# register a signal handler so that we can exit early
def signal_handler(signal, frame):
    print('KeyboardInterrupt')
    print_summary()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

# read our comments.txt file

for line in comments:
    # use a try-except block since we occasionally get language not supported errors
    try:
        score, mag = detect_sentiment(line)
    except InvalidArgument as e:
        # skip the comment if we get an error
        print('Skipped 1 comment: ', e.message)
        failed += 1
        continue

    # increment the total count
    count += 1

    # depending on whether the sentiment is positve, negative or neutral, increment the corresponding count
    if score > 0:
        positive_count += 1
    elif score < 0:
        negative_count += 1
    else:
        neutral_count += 1

    # calculate the proportion of comments with each sentiment
    positive_proportion = positive_count / count
    neutral_proportion = neutral_count / count
    negative_proportion = negative_count / count

    if count % 50 == 0:
        print("Counted {}".format(count))

##    print(
##        'Count: {}, Positive: {:.3f}, Neutral: {:.3f}, Negative: {:.3f}'.format(
##            count, positive_count, neutral_count, negative_count))

print_summary()
