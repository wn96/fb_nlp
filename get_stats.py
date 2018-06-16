import requests
import signal
import sys
import get_comments

from google.cloud import language
from google.api_core.exceptions import InvalidArgument

def sentiments_output(access_token, graph_api_version, user_id, post_id, limit):
    # create a Google Cloud Natural Languague API Python client
    client = language.LanguageServiceClient()

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
    failed = 0

    # register a signal handler so that we can exit early
    def signal_handler(signal, frame):
        print('KeyboardInterrupt')
        print_summary()
        sys.exit(0)


    signal.signal(signal.SIGINT, signal_handler)

    # read our comments

    for line in get_comments.get_comments(access_token, graph_api_version, user_id, post_id, limit):
        # use a try-except block since we occasionally get language not supported errors
        try:
            score, mag = detect_sentiment(line)
        except InvalidArgument as e:
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
    return (positive_count, neutral_count, negative_count, failed, count)
