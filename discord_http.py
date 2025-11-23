import requests
import os
import time

class DiscordHttp:
    def __init__(self):
        self.session = requests.Session()

    def _request_with_retries(self, verb, url, **kwargs):
        retries = 3
        delay = 2  # seconds
        for attempt in range(retries):
            try:
                response = self.session.request(verb, url=url, **kwargs)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                if attempt < retries - 1:
                    time.sleep(delay)
                else:
                    raise e

    def post_message(self, content, messageId=None):
        # flags = 4 means it will suppress embeds: https://discord.com/developers/docs/resources/message#message-object-message-flags
        content_payload = {"content": content, "flags": 4}
        target_url = os.getenv('TARGET_URL')
        verb = "POST"
        if messageId is not None:
            target_url = target_url + f"/messages/{messageId}"
            verb = "PATCH"
        response = self._request_with_retries(
            verb, url=target_url, params={"wait": "true"}, json=content_payload
        )
        return response.json()['id']

    def get_message_from_id(self, messageId):
        target_url = os.getenv('TARGET_URL')
        verb = "GET"
        target_url = target_url + f"/messages/{messageId}"
        response = self._request_with_retries(verb, url=target_url)
        return response.json()['content']