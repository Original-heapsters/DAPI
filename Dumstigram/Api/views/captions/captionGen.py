from flask import current_app


with current_app.app_context():
    api = current_app.config['TWEEPY']


def get_rand_tweet():
    random_tweet = api.search(q='#contentmarketing',
                              count=1,
                              lang='en',
                              since='2017-06-20')
    return random_tweet.text
