# Using GetOldTweets3 library instead of Tweepy because of query limits
import GetOldTweets3 as got
import pandas as pd
from textblob import TextBlob
import re


def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w+:\ / \ / \S+)", " ", tweet).split())


def get_tweet_sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'


def text_query(text_to_query, count, since_date, until_date, location):
    # Creation of query object
    tweet_criteria = got.manager.TweetCriteria().setQuerySearch(text_to_query).\
                                                 setMaxTweets(count).\
                                                 setSince(since_date).\
                                                 setUntil(until_date).\
                                                 setNear(location).\
                                                 setEmoji("unicode")

    # Creation of list that contains all tweets from query
    tweets_data = got.manager.TweetManager.getTweets(tweet_criteria)

    # Creating list of chosen tweet data
    tweets = []

    # Format data before saving
    for tweet in tweets_data:
        date = tweet.date.strftime('%Y-%m-%d')
        time = tweet.date.strftime('%H:%M')

        # Get analysis of tweet
        analysis_result = get_tweet_sentiment(tweet.text)

        tweets.append([tweet.id,
                       tweet.permalink,
                       tweet.username,
                       tweet.text,
                       analysis_result,
                       date, time])

    # Creation of dataframe from tweets
    tweets_df = pd.DataFrame(tweets, columns=['ID', 'Permalink', 'Username', 'Tweet', 'Sentiment Analysis', 'Date', 'Time'])

    # Converting tweets dataframe to csv file
    tweets_df.to_csv('{}-tweets.csv'.format(text_to_query), sep=',')


# Selected query is BBI
# Selected time interval is from June 1 2019 to February 29 2019
text_query("bbi", 2100, "2019-06-01", "2020-02-29", "Nairobi, Kenya")
