import requests
import base64
import datetime

consumer_key = 'XXZIKkMETHW6tAdGXs0jXo3SB'
consumer_secret = 'G9OJGz2MceHf8ZLkXDCyV0U4hQEcMVKiXHxyTReli6Fjxn9KQF'
resource_owner_key = '1214904876427288576-8XoWHXKYQvCRJvmRfL4Hz9ENNzcfjw'
resource_owner_secret = 'imbtd4xK0sTYUqpH270zzBzc3d9QF2sXgRuR7BGPan7ZX'

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
pages_list = ['Python Weekly', 'Real Python', 'Full Stack Python']

# real time to check the tweet
time = datetime.datetime.now()
real_minute = time.minute
real_hour = time.hour

# format the time for the fromdate parmetr
list_str_date = str(time.date()).split("-")
str_date = ""
for string in list_str_date:
    str_date += string
str_date += str(real_hour - 1)
str_date += str(real_minute)

tweets_to_send = []
for page in pages_list:
    search_params = {
        'q': page,
        "fromDate": "str_date",
        "maxResults": 500,
        'lang': 'en'
    }
    search_url = '{}1.1/search/tweets.json'.format(base_url)
    search_resp = requests.get(search_url, headers=search_headers, params=search_params)
    tweet_data = search_resp.json()

    for tweet in tweet_data['statuses']:
        if tweet['id'] not in tweets_to_send:
            tweets_to_send.append((tweet['created_at'], tweet['text']))

for tweet in tweets_to_send:
    print(tweet)