import twitter
import json


CONSUMER_KEY ='Your Consumer Key'
CONSUMER_SECRET = 'Your Customer Secret'
OAUTH_TOKEN = 'OAUTH TOKEN'
OAUTH_TOKEN_SECRET = 'OAUTH SECRET'



class Twitter:

    def __init__(self):

        auth  = twitter.oauth.OAuth(OAUTH_TOKEN , OAUTH_TOKEN_SECRET, CONSUMER_KEY , CONSUMER_SECRET)

        self.twitter_api = twitter.Twitter(auth = auth)

    def status__search(self , tweet  , max_results = 200, **kw):

        search_results = self.twitter_api.search.tweets(q =  tweet , count = max_results, **kw)
        statuses = search_results["statuses"]



        for _ in range(10):

            try:

                next_results = search_results["search_metadata"]["next_results"]
            except KeyError as e:
                break
            kwargs = dict([kv.split("=") for kv in next_results[1:].split("&")])

            search_results = self.twitter_api.search.tweets(**kwargs)
            statuses += search_results["statuses"]

            if len(statuses) > max_results:
                break


        return statuses

    def tweet_search(self , query, max_results = 1000 ):

        statuses = self.status__search(query , max_results = max_results)
        tweets = []

        for status in statuses:
            if status["text"] not in tweets:
                tweets.append(status["text"])
        return tweets


def main():

    twitter = Twitter()
    tweets = twitter.tweet_search("doctor strange" , max_results = 1000)

    for tweet in tweets:
        print(tweet)

if __name__ == "__main__":
    main()
