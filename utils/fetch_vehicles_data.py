import json
from typing import List

import requests


def search_vehicles() -> List[dict]:
    """API request to get a list real vehicles.

    Returns:
        List[dict]: Dict list content a brand and car model
    """
    url = "https://parseapi.back4app.com/classes/Car_Model_List?keys=Make,Model"
    headers = {
        "X-Parse-Application-Id": "hlhoNKjOvEhqzcVAJ1lxjicJLZNVv36GdbboZj3Z",
        "X-Parse-Master-Key": "SNMJJF0CZZhTPhLDIqGhTlUNV9r60M2Z5spyWfXW",
    }

    response = requests.get(url, headers=headers)
    return json.loads(response.content.decode("utf-8"))["results"]
