import requests
import base64
import datetime



def getTweeets(p=None):
    consumer_key = 'XXZIKkMETHW6tAdGXs0jXo3SB'
    consumer_secret = 'G9OJGz2MceHf8ZLkXDCyV0U4hQEcMVKiXHxyTReli6Fjxn9KQF'


    client_key = consumer_key
    client_secret = consumer_secret

    key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')

    b64_encoded_key = base64.b64encode(key_secret)
    b64_encoded_key = b64_encoded_key.decode('ascii')

    base_url = 'https://api.twitter.com/'
    auth_url = '{}oauth2/token'.format(base_url)

    auth_headers = {
        'Authorization': 'Basic {}'.format(b64_encoded_key),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }

    auth_data = {
        'grant_type': 'client_credentials'
    }

    auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)

    access_token = auth_resp.json()['access_token']

    search_headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    if p == None:
        pages_list = ['Python Weekly', 'Real Python', 'Full Stack Python']
    else:
        pages_list = [p]

    # real time to check the tweet
    time = datetime.datetime.now()
    real_minute = time.minute
    real_hour = time.hour

    # format the time for the fromdate parameter
    list_str_date = str(time.date()).split("-")
    str_date = ""
    for string in list_str_date:
        str_date += string
    if real_hour == 00:
        str_date += str(23)
    else:
        str_date += str(real_hour - 1)
    str_date += str(real_minute)

    tweets_to_send = set()

    for page in pages_list:
        search_params = {
            'q': page,
            "fromDate": str_date,
            "maxResults": 500,
            'lang': 'en'
        }
        # statuses/user_timeline.json
        search_url = '{}1.1/search/tweets.json'.format(base_url)
        search_resp = requests.get(search_url, headers=search_headers, params=search_params)
        tweet_data = search_resp.json()

        for tweet in tweet_data['statuses']:
            if int(tweet['created_at'].split(' ')[3].split(':')[0]) > real_hour - 1:
                tweets_to_send.add(tweet['text'])

    return tweets_to_send



