# Using GetOldTweets3 library instead of Tweepy because of query limits
import GetOldTweets3 as got
import pandas as pd


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
        tweets.append([tweet.id,
                       tweet.permalink,
                       tweet.username,
                       tweet.text,
                       date, time,
                       tweet.retweets,
                       tweet.favorites,
                       tweet.hashtags])

    # Creation of dataframe from tweets
    tweets_df = pd.DataFrame(tweets, columns=['ID', 'Permalink', 'Username', 'Tweet', 'Date', 'Time', 'Retweets', 'Favorites', 'Hashtags'])

    # Converting tweets dataframe to csv file
    tweets_df.to_csv('{}-tweets.csv'.format(text_to_query), sep=',')


# Selected hashtag is #IkoKazeKe
# Selected time interval is from January 01 2019 to December 31 2019
text_query("#IkoKaziKe", 5000, "2019-01-01", "2019-12-31", "Nairobi, Kenya")
