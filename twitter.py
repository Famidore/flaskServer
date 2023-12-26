from youtube import obtain_key
import tweepy

client = tweepy.Client(obtain_key("twitter_token.txt"))
