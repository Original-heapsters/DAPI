from flask import current_app
from flask_healthz import HealthError

with current_app.app_context():
    redis = current_app.config['REDIS']
    tweepy_api = current_app.config['TWEEPY']


def liveness():
    if not redis.ping():
        raise HealthError("Can't connect to the redis instance")
    query = 'alive'
    if not tweepy_api.get_recent_tweets_count(query=query, granularity='day'):
        raise HealthError("Can't connect to the tweepy api instance")


def readiness():
    if not redis.ping():
        raise HealthError("Can't connect to the redis instance")

    query = 'ready'
    if not tweepy_api.get_recent_tweets_count(query=query, granularity='day'):
        raise HealthError("Can't connect to the tweepy api instance")
