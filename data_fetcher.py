from os import getenv
from dotenv import load_dotenv
import requests

load_dotenv()


class Animal:
    """
    Represents an animal and its characteristics.
    """

    def __init__(self, animal_data: dict):
        """Initializes the Animal object."""
        self.animal_data = animal_data
        self.name = self.animal_data.get("name")
        self.taxonomy = self.animal_data.get("taxonomy")
        self.characteristics = self.animal_data.get("characteristics")
        self.scientific_name = self.taxonomy.get("scientific_name")
        self.diet = self.characteristics.get("diet")
        self.type = self.characteristics.get("type")
        self.skin_type = self.characteristics.get("skin_type")
        self.color = self.__colors
        self.locations = self.__locations

    def __iter__(self):
        """
        Makes the Animal object iterable.
        """
        yield "name", self.name
        yield "scientific_name", self.scientific_name
        yield "diet", self.diet
        yield "type", self.type
        yield "skin Type", self.skin_type
        yield "color", self.color
        yield "locations", self.locations

    @property
    def __locations(self) -> str:
        """
        Formats the locations of the animal.
        """
        locations = self.animal_data.get("locations")
        locations = " and ".join(locations)
        and_count = locations.count(" and ")
        return locations.replace(" and ", ", ", and_count - 1)

    @property
    def __colors(self) -> str:
        """
        Formats the colors of the animal.
        """
        color = self.characteristics.get("color")
        form_color = ""
        if color:
            form_color = color[0]
            for char in color[1:]:
                if char.isupper():
                    form_color += " / "
                form_color += char
        return form_color


def fetch_data(animal_name: str) -> tuple[list[Animal], list[str]]:
    """
    Fetches animal data from the API.
    """
    response = requests.get(
        url='https://api.api-ninjas.com/v1/animals',
        params={'name': animal_name},
        headers={'X-Api-Key': getenv('API_NINJAS_KEY')}
    )

    if not response.status_code == 200:
        raise requests.exceptions.RequestException

    data = response.json()

    animals = []
    skin_types = []

    for animal in data:
        animal_obj = Animal(animal)
        animals.append(animal_obj)
        skin_types.append(animal_obj.skin_type)

    return animals, list(set(skin_types))
