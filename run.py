import os
import slack
import time
import threading
from tweets import getTweeets


def f(f_stop):
    if not f_stop.is_set():
        client = slack.WebClient(token='xoxb-962732149956-951750678595-5RPg2DDV5bz9zQmglj5Qlhm0')
        localtime = time.asctime(time.localtime(time.time()))
        response = client.chat_postMessage(
            channel='#content',
            text="Local current time :" + localtime)
        threading.Timer(60*60, f, [f_stop]).start()

f_stop = threading.Event()
# start calling f now and every hour thereafter
f(f_stop)



@slack.RTMClient.run_on(event='message')
def say_hello(**payload):
    data = payload['data']
    web_client = payload['web_client']
    rtm_client = payload['rtm_client']
    if 'now' in data.get('text', []):
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']
        localtime = time.asctime(time.localtime(time.time()))
        web_client.chat_postMessage(
            channel=channel_id,
            text=f'<@{user}>, the time is :' + localtime
            #thread_ts=thread_ts
        )
    elif 'new-content' in data.get('text', []):
        channel_id = data['channel']

        user = data['user']
        tweets = getTweeets()
        web_client.chat_postMessage(
            channel=channel_id,
            text=f'<@{user}>, here is the new content: \n' + '\n'.join(map(str, tweets))
        )

slack_token = 'xoxb-962732149956-951750678595-5RPg2DDV5bz9zQmglj5Qlhm0'
rtm_client = slack.RTMClient(token=slack_token)
rtm_client.start()
