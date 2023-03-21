import os
import json
import requests


class UrlLabelService:
    def __init__(self):
        self._api_endpoint = os.environ["API_ENDPOINT"] + "/website/predict"

    def add_url(self, input_url):
        """
        Add an url to the database
        :param input_url:
        :return:
        """

        payload = json.dumps([{"url": input_url}])
        headers = {"Content-Type": "application/json"}
        url = self._api_endpoint
        response = requests.request("POST", url, headers=headers, data=payload)
        results = response.json()
        return results
