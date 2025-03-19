import requests

class OpenverseAPIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openverse.engineering/v1/images"

    def search_images(self, query):
        url = f"{self.base_url}?q={query}"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return None
        except requests.exceptions.RequestException as err:
            print(f"Error occurred: {err}")
            return None

        try:
            data = response.json()
            images = [
                {
                    "url": item["url"],
                    "title": item["title"],
                    "creator": item["creator"]
                }
                for item in data.get("results", [])
            ]
            return images
        except ValueError as json_err:
            print(f"JSON decode error: {json_err}")
            return None