from os import getenv
from dotenv import load_dotenv
from requests import Response, get

load_dotenv()

AnimalData = list[dict[str, str | list[str] | dict[str, str]]]
KEY = getenv('API_NINJAS_KEY')
URL = 'https://api.api-ninjas.com/v1/animals'


class ApiLoad:

    def __init__(self, animal: str, url: str = URL, key: str = KEY) -> None:
        self.url: str = url
        self.params: dict[str, str] = {'name': animal}
        self.headers: dict[str, str] = {'X-Api-Key': key}

    @property
    def data(self) -> Response:
        return get(self.url, params=self.params, headers=self.headers)

    @property
    def data_json(self) -> AnimalData:
        return self.data.json()
