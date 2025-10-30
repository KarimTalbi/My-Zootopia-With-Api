"""requests animal info from the animal api"""
from os import getenv
from dotenv import load_dotenv
from requests import Response, get

load_dotenv()

AnimalData = list[dict[str, str | list[str] | dict[str, str]]]
KEY = getenv('API_NINJAS_KEY')
URL = 'https://api.api-ninjas.com/v1/animals'


class ApiLoad:
    """
    Class for making API requests to retrieve data related to animals.

    This class facilitates the interaction with an API by defining the
    necessary parameters, headers, and the methods to fetch and process
    the response data. It is designed to handle API requests efficiently
    for specific animal-related data.
    """

    def __init__(self, animal: str, url: str = URL, key: str = KEY) -> None:
        self.url: str = url
        self.params: dict[str, str] = {'name': animal}
        self.headers: dict[str, str] = {'X-Api-Key': key}

    @property
    def data(self) -> Response:
        """
        Returns the response object for the given URL with the specified parameters
        and headers by making an HTTP GET request.
        """
        return get(self.url, params=self.params, headers=self.headers)

    @property
    def data_json(self) -> AnimalData:
        """
        Returns the JSON representation of the animal data.

        This property provides the JSON data contained within the instance,
        parsed in the form of an AnimalData object.
        """
        return self.data.json()

    @property
    def has_info(self) -> bool:
        """
        Indicates whether the object contains information based on the presence of
        data in the `data_json` attribute.
        """
        return len(self.data_json) > 0
