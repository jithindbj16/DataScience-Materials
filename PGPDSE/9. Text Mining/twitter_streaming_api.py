from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import glob
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

senti = SentimentIntensityAnalyzer()

consumer_key = "mxTTBeZ3GyqBmfi76RcjpOA0D"
consumer_secret = "yF5Fi5YTNlosNKrP73TGb6KLT6xxVHaeKOYGQYjtj45BAO5pRI"

access_token = "775582536516849664-wOokh3u1KmZMndQiS9F2AQhBQ5Mvc3k"
access_token_secret = "gwpsKLfyIIQk6GyaeNUbDAFvhpWQNjl0vlpO06i5HXqAh"

def get_sentiment(text):
    score=senti.polarity_scores(text)['compound']
    if score>0.05:
           return 'Positive'
    elif score < -0.05:
           return 'Negative'
    else:
           return 'Neutral'


class StdOutListener(StreamListener):

    def on_data(self, data):
        data = json.loads(data)
        print('---------Someone Tweeted with #AnilAmbani-----------')
        text=data['text']
        curr_tweet={
        'text':[data['text']],
        'created_at':[data['created_at']],
        'source':[data['source']],
        'geo':[data['geo']],
        'profile_location':[data['user']['location']],
        'profile_name':[data['user']['name']],
        'profile_description':[data['user']['description']],
         'sentiment':[get_sentiment(data['text'])]
        }
        df_tweet=pd.DataFrame(curr_tweet)
        csv_file='tweets.csv'
        try:
            if csv_file in glob.glob('*.csv'):
                # Append results
                with open(csv_file,'a') as f:
                    df_tweet.to_csv(f,header=False,index=False)
            else:
                # Create one and add data
                df_tweet.to_csv(csv_file,index=False)
        except:
            pass
        
        return True

    def on_error(self, status):
        print (status)


if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(track=['#AnilAmbani'])