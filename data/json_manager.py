"""JSON Database management"""
import os
import json
from data.animals_api import ApiLoad

FILE = os.path.join("data", "animals_data.json")
ENCODER = "utf-8"

AnimalData = list[dict[str, str | list[str] | dict[str, str]]]
SingleAnimal = dict[str, str | list[str] | dict[str, str]]


class FileError(Exception):
    """
    Custom exception raised when there is an error while loading
    a file.
    """
    pass


class DataCRUD:
    """
    Handles the foundational task of loading the entire
    animal database from a specified JSON file into memory.
    """

    def __init__(self, file_path: str = FILE, animal: str = 'fox') -> None:
        """
        Initializes the DataLoad class and attempts to load the JSON data.

        :param file_path: The path to the JSON database file. Defaults to FILE.
        """
        self.file_path: str = file_path
        self.animal_name: str = animal
        self._data: AnimalData | None = None

    @property
    def load(self) -> AnimalData:
        """
        Reads the animal data from the JSON file specified by `self.file_path`.

        The data is loaded **lazily**—it's read from the disk only on the first access
        and then cached in `self._data` for all later calls.

        :raises FileError: If the file does not exist, or if the file content is invalid JSON.
        :return: A list of dictionaries representing the animal data.
        """
        if self._data is not None:
            return self._data

        if not os.path.exists(self.file_path):
            raise FileError(f"Error: The required JSON data file was not found at path: {self.file_path}")

        try:
            with open(self.file_path, "r", encoding=ENCODER) as f:
                self._data = json.load(f)
                return self._data

        except json.JSONDecodeError as e:
            raise FileError(f"Error: File '{self.file_path}' is corrupted (not valid JSON): {e}")

    def save(self, data: AnimalData) -> None:
        with open(self.file_path, 'w', encoding=ENCODER) as f:
            json.dump(data, f, indent=4)

        self._data = None

    @property
    def load_api(self):
        return ApiLoad(self.animal_name).data_json

    def save_from_api(self):
        self.save(self.load_api)

    def __getitem__(self, index: int) -> SingleAnimal:
        """
        Allows indexing (e.g., data_load_instance[0]) to get a single animal's data.

        :param index: The index of the animal in the list.
        :return: A dictionary containing the data for a single animal.
        """
        return self.load[index]

    def __len__(self) -> int:
        """
        Returns the total number of animals loaded, enabling use with `len()`.

        :return: The count of animals in the database (integer).
        """
        return len(self.load)


class DataInfo(DataCRUD):
    """
    Provides multiple getter properties to retrieve specific
    and formatted information for a single, indexed animal record.
    """

    def __init__(self, index: int = 0, file_path: str = FILE) -> None:
        """
        Initializes DataInfo, loading the full database via the parent class
        and setting the focus on the animal at the given index.

        :param index: The index of the animal to focus on. Defaults to 0.
        :param file_path: The path to the JSON database file. Defaults to FILE.
        """
        super().__init__(file_path)
        self.animal = self.__getitem__(index)

    @property
    def count(self) -> int:
        """
        Returns the total number of different animals in the loaded database.

        :return: The total count of animals (integer).
        """
        return self.__len__()

    @property
    def skin_types(self) -> list[str]:
        """
        Collects all unique skin types from all animals in the database.

        :return: A sorted list of unique skin type strings.
        """
        types = []
        for animal in self.load:
            skin = animal["characteristics"].get("skin_type")
            if skin:
                types.append(skin)
        return sorted(list(set(types)))

    @property
    def skin_count(self) -> int:
        """
        Returns the total number of different skin types in the loaded database.

        :return: The total count of skin types (integer).
        """
        return len(self.skin_types)

    @property
    def filter_options(self) -> dict[str, str]:
        """
        Generates a dictionary mapping menu numbers (as strings) to unique skin types.

        :return: A dictionary mapping index number strings (starting at "1") to skin type names.
        """
        return {f"{i + 1}": skin for i, skin in enumerate(self.skin_types)}

    @property
    def filter_menu(self) -> str:
        """
        Generates a formatted string representing a command-line filter menu
        based on unique skin types, including an option to exit the program.

        :return: A multi-line string ready for display as a menu.
        """
        return "\n".join([f"{key}. {value}" for key, value in self.filter_options.items()] + [
            f"{self.skin_count + 1}. Exit program"])

    @property
    def taxonomy(self) -> dict[str, str]:
        """
        Returns the taxonomy child dictionary for the current animal.

        :return: A dictionary containing the taxonomy data.
        """
        return self.animal.get("taxonomy")

    @property
    def characteristics(self) -> dict[str, str]:
        """
        Returns the characteristic child dictionary for the current animal.

        :return: A dictionary containing the characteristics' data.
        """
        return self.animal.get("characteristics")

    @property
    def name(self) -> str:
        """
        Returns the common name of the current animal.

        :return: The animal's name (string).
        """
        return self.animal.get("name")

    @property
    def scientific_name(self) -> str:
        """
        Returns the scientific name of the current animal from the taxonomy data.

        :return: The animal's scientific name (string).
        """
        return self.taxonomy.get("scientific_name")

    @property
    def diet(self) -> str:
        """
        Returns the diet type of the current animal from the characteristics' data.

        :return: The animal's diet (string).
        """
        return self.characteristics.get("diet")

    @property
    def type(self) -> str:
        """
        Returns the generic type/group of the current animal (e.g., 'Mammal', 'Hound').

        :return: The animal's type (string).
        """
        return self.characteristics.get("type")

    @property
    def color(self) -> str:
        """
        Returns the animal's colors, formatted with slashes (' / ')
        by splitting the camel-cased color string based on capital letters.

        E.g., "BlackWhiteTan" becomes "Black / White / Tan".

        :return: A formatted string of the animal's colors.
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

    @property
    def skin_type(self) -> str:
        """
        Returns the skin/coat type (e.g., 'Fur', 'Hair', 'Scales') of the current animal.

        :return: The animal's skin type (string).
        """
        return self.characteristics.get("skin_type")

    @property
    def locations(self) -> str:
        """
        Returns a formatted string of the geographical locations where the animal is found.
        It joins the list of locations with commas, using ' and ' before the final item.

        E.g., ['A', 'B', 'C'] becomes "A, B and C".

        :return: A comma-and-separated string of locations.
        """
        locations = self.animal.get("locations")
        locations = " and ".join(locations)
        and_count = locations.count(" and ")
        return locations.replace(" and ", ", ", and_count - 1)
