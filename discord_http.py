import requests
import os

class DiscordHttp:
    def __init__(self):
        self.session = requests.Session()

    def post_message(self, content, messageId=None):
        # flags = 4 means it will suppress embeds: https://discord.com/developers/docs/resources/message#message-object-message-flags
        content_payload = {"content": content, "flags": 4}
        target_url = os.getenv('TARGET_URL')
        verb = "POST"
        if messageId is not None:
            target_url = target_url + f"/messages/{messageId}"
            verb = "PATCH"
        response = self.session.request(verb, url=target_url, params={"wait": "true"}, json=content_payload)
        return response.json()['id']

    def get_message_from_id(self, messageId):
        target_url = os.getenv('TARGET_URL')
        verb = "GET"
        target_url = target_url + f"/messages/{messageId}"
        response = self.session.request(verb, url=target_url)
        return response.json()['content']