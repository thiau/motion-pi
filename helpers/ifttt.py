import requests


def trigger_webhook(event_name: str, api_key: str):
    response = requests.get(f"https://maker.ifttt.com/trigger/{event_name}/json/with/key/{api_key}")
    return response
