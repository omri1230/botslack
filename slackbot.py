import requests
import json


webhook = "https://hooks.slack.com/services/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"

data = {
    "text": "hi this is a test"
}

requests.post(webhook, json.dumps(data))
