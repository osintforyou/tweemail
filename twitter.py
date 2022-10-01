# import tweepy
import tweepy as tw
# import panda
import pandas as pd
# import time
import time
# your Twitter API key and API secret
my_api_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXX"
my_api_secret = "#################################"

# authenticate
auth = tw.OAuthHandler(my_api_key, my_api_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# This is the important part. You have to do your research on Twitter and you will receive the latest tweets from all the users, who will be added to the search_query below.
search_query = "(from:BBCNews OR from:Reuters OR from:cnnbrk OR from:euronews)"

# get tweets from the API
tweets = tw.Cursor(api.search_tweets,
            q=search_query,
            lang="en").items(50) #Depending how often you want to run this program and how many overall tweets the users creating in a certain time, you can decide how much tweets you want to receive in an email.
# store the API responses in a list
tweets_copy = []
for tweet in tweets:
    tweets_copy.append(tweet)
    
print("Total Tweets fetched:", len(tweets_copy))

# intialize the dataframe
tweets_df = pd.DataFrame()
# populate the dataframe
for tweet in tweets_copy:
    hashtags = []
    try:
        for hashtag in tweet.entities["hashtags"]:
            hashtags.append(hashtag["text"])
        text = api.get_status(id=tweet.id, tweet_mode='extended').full_text
    except:
        pass
    tweets_df = tweets_df.append(pd.DataFrame({'user_name': tweet.user.name, 
                                               'user_location': tweet.user.location,\
                                               'user_description': tweet.user.description,
                                               'user_verified': tweet.user.verified,
                                               'date': tweet.created_at,
                                               'text': text, 
                                               'hashtags': [hashtags if hashtags else None],
                                               'source': tweet.source}))
    tweets_df = tweets_df.drop(['user_description', 'hashtags', 'source'], axis=1)
    tweets_df = tweets_df.reset_index(drop=True)
# show the dataframe
tweets_df.head()
timestr = time.strftime("%Y%m%d-%H%M%S")
tweets_df.to_html(f"'{timestr}+.html', index = False")
