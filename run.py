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
        threading.Timer(60 * 60, f, [f_stop]).start()


def g(g_stop):
    if not g_stop.is_set():
        client = slack.WebClient(token='xoxb-962732149956-951750678595-5RPg2DDV5bz9zQmglj5Qlhm0')
        tweets = getTweeets(p='omri')
        if tweets:
            response = client.chat_postMessage(
                channel='#content',
                text="python user : \n" + '\n'.join(map(str, tweets)))
        threading.Timer(60*20, g, [g_stop]).start()


f_stop = threading.Event()
f(f_stop)

g_stop = threading.Event()
g(g_stop)


@slack.RTMClient.run_on(event='message')
def say_hello(**payload):
    data = payload['data']
    web_client = payload['web_client']
    rtm_client = payload['rtm_client']
    if 'now' in data.get('text', []):
        channel_id = data['channel']
        user = data['user']
        localtime = time.asctime(time.localtime(time.time()))
        web_client.chat_postMessage(
            channel=channel_id,
            text=f'<@{user}>, the time is :' + localtime
        )
    elif 'new-content' in data.get('text', []):
        if 'new-content' == data.get('text', []):
            channel_id = data['channel']
            tweets = getTweeets()
            web_client.chat_postMessage(
                channel=channel_id,
                text='\n'.join(map(str, tweets))
            )
        else:
            source = data.get('text', [])[12:]
            channel_id = data['channel']
            tweets = getTweeets(source)
            if tweets:
                web_client.chat_postMessage(
                    channel=channel_id,
                    text='\n'.join(map(str, tweets))
                )

slack_token = 'xoxb-962732149956-951750678595-5RPg2DDV5bz9zQmglj5Qlhm0'
rtm_client = slack.RTMClient(token=slack_token)
rtm_client.start()
