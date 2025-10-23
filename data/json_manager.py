"""JSON Database management"""
import os
import json
import sys

FILE = os.path.join("data", "animals_data.json")
ENCODER = "utf-8"

AnimalData = list[dict[str, str | list[str] | dict[str, str]]]
SingleAnimal = dict[str, str | list[str] | dict[str, str]]


class DataLoad:
    """Parent of DataInfo: Loads the Data from the JSON"""

    def __init__(self, file_path: str = FILE) -> None:
        self.file_path = file_path
        self.data = self.get_data

    def __getitem__(self, index: int) -> SingleAnimal:
        return self.data[index]

    def __len__(self) -> int:
        return len(self.data)

    @property
    def get_data(self) -> AnimalData:
        """Returns the data from the database, terminates the program if the database doesn't exist"""
        if not os.path.exists(self.file_path):
            sys.exit(f"File: {self.file_path} could not be loaded. Exiting program...")

        with open(self.file_path, "r", encoding=ENCODER) as f:
            return json.load(f)


class DataInfo(DataLoad):
    """Child of DataLoad: offers multiple getter methods to get specific information from the database"""

    def __init__(self, index: int = 0, file_path: str = FILE) -> None:
        super().__init__(file_path)
        self.animal = self.__getitem__(index)

    @property
    def count(self) -> int:
        """returns the number of different animals"""
        return len(self.data)

    @property
    def skin_types(self) -> list[str]:
        """returns a list of unique Skin Types"""
        types = []
        for animal in self.data:
            types.append(animal["characteristics"]["skin_type"])
        return sorted(list(set(types)))

    @property
    def filter_options(self) -> dict[str, str]:
        """returns a dictionary """
        return {f"{i + 1}": skin for i, skin in enumerate(self.skin_types)}

    @property
    def filter_menu(self) -> str:
        """returns the menu string"""
        return "\n".join([f"{key}. {value}" for key, value in self.filter_options.items()] + [
            f"{len(self.skin_types) + 1}. Exit program"])

    @property
    def taxonomy(self) -> dict[str, str]:
        """returns separate taxonomy child dictionary"""
        return self.animal.get("taxonomy")

    @property
    def characteristics(self) -> dict[str, str]:
        """returns separate characteristics child dictionary"""
        return self.animal.get("characteristics")

    @property
    def name(self) -> str:
        """returns the name of the animal"""
        return self.animal.get("name")

    @property
    def scientific_name(self) -> str:
        """returns the scientific name of the animal"""
        return self.taxonomy.get("scientific_name")

    @property
    def diet(self) -> str:
        """returns the diet of the animal"""
        return self.characteristics.get("diet")

    @property
    def type(self) -> str:
        """returns the type of the animal"""
        return self.characteristics.get("type")

    @property
    def color(self) -> str:
        """returns the color of the animal"""
        color = self.characteristics.get("color")
        form_color = ""
        if color:
            form_color = color[0]
            for char in color[1:]:
                if char.isupper():
                    form_color += " / "
                form_color += char
        return form_color

    @property
    def skin_type(self) -> str:
        """returns the skin type of the animal"""
        return self.characteristics.get("skin_type")

    @property
    def locations(self) -> str:
        """returns the locations of the animal"""
        locations = self.animal.get("locations")
        locations = " and ".join(locations)
        and_count = locations.count(" and ")
        return locations.replace(" and ", ", ", and_count - 1)
