from get_stats import *
from config import *

print(sentiments_output(access_token, graph_api_version, user_id, post_id, limit))

def print_summary(positive_count, neutral_count, negative_count, count):
    print()
    print('Total comments analysed: {}'.format(count))
    print('Positive : {} ({:.2%})'.format(positive_count, positive_count / count))
    print('Negative : {} ({:.2%})'.format(negative_count, negative_count / count))
    print('Neutral  : {} ({:.2%})'.format(neutral_count, neutral_count / count))
    print('Failed   : {} ({:.2%})'.format(failed, failed / count))

