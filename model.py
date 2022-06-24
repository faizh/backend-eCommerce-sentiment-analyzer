import requests
import json

username_lazada     = "LazadaID"
username_bukalapak  = "bukalapak"
username_blibli     = "bliblidotcom"
username_tokopedia  = "tokopedia"

def connect_to_twitter():
    bearer_token = 'AAAAAAAAAAAAAAAAAAAAAHdHdgEAAAAAfeShfQ5b43jfs7zVyTTjTpecq68%3D0rbfMnF974zUZEeYpu72Y7gDSKlEULZx6LMp1KfGbgEvkkajJY'
    return {"Authorization" : "Bearer " + bearer_token}

headers = connect_to_twitter()

def get_tweets_from_id(start_date, end_date, username):
    url         = "https://api.twitter.com/2/tweets/search/recent?"
    max_result  = "max_results=100"
    start_time  = "start_time=" + start_date
    end_time    = "end_time=" + end_date
    query       = "query=from:" + username + " -is:retweet -is:reply"
    params = start_time + "&" + end_time + "&" + max_result + "&" + query
    response_tweet = requests.request("GET", url, params=params, headers=headers).json()
    
    return response_tweet

def get_tweet_to_id():
    url         = "https://api.twitter.com/2/tweets/search/recent?"
    max_result  = "max_results=100"
    start_time  = "start_time=2022-06-23T00:00:00Z" 
    end_time    = "end_time=2022-06-24T00:00:00Z"
    query       = "query=to:IndiHomeCare -is:retweet"
    params = start_time + "&" + end_time + "&" + max_result + "&" + query
    response_tweet = requests.request("GET", url, params=params, headers=headers).json()
    
    return response_tweet

def query_get_conversation_by_tweet_id(tweet_id, start_date, end_date):
    url         = "https://api.twitter.com/2/tweets/search/recent?"
    max_result  = "max_results=25"
    start_time  = "start_time=" + start_date
    end_time    = "end_time=" + end_date
    query_from  = " -from: " + str(username_blibli) + " -from: " + str(username_bukalapak) + " -from: " + str(username_lazada) + " -from: " + str(username_tokopedia)
    query       = "query= -is:retweet conversation_id:" + str(tweet_id) + query_from
    tweet_fields = "tweet.fields=created_at,author_id"
    params = start_time + "&" + end_time + "&" + max_result + "&" + query + "&" + tweet_fields
    response_tweet = requests.request("GET", url, params=params, headers=headers).json()
    
    return response_tweet

def get_tweet_id_from_tweets_created(start_date, end_date, username):
    tweets_created = get_tweets_from_id(start_date, end_date, username)
    tweet_id = []
    for tweet in tweets_created['data']:
        tweet_id.append(tweet['id'])

    return tweet_id

def get_conversation_from_tweet_id(start_date, end_date):
    tweets_id_lazada    = get_tweet_id_from_tweets_created(start_date, end_date, username_lazada)
    tweets_id_blibli    = get_tweet_id_from_tweets_created(start_date, end_date, username_blibli)
    tweets_id_bukalapak = get_tweet_id_from_tweets_created(start_date, end_date, username_bukalapak)
    tweets_id_tokopedia = get_tweet_id_from_tweets_created(start_date, end_date, username_tokopedia)

    tweets_id = []
    tweets_id += tweets_id_lazada
    tweets_id += tweets_id_blibli
    tweets_id += tweets_id_bukalapak
    tweets_id += tweets_id_tokopedia
    
    tweet_details_arr = []
    for tweet_id in tweets_id:
        tweet_details = query_get_conversation_by_tweet_id(tweet_id, start_date, end_date)

        try:
            for tweet_detail in tweet_details['data']:
                tweet_details_arr.append(tweet_detail)
        except:
            continue

    
    return json.dumps(tweet_details_arr)