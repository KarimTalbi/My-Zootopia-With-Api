"""Manages the database"""
import os
import json
import sys

FILE = os.path.join("data", "animals_data.json")
ENCODER = "UTF-8"
AnimalData = list[dict[str, str | list[str] | dict[str, str]]]


class DatabaseFile:
    """Loads Database content"""

    def __init__(self, file_path: str = FILE):
        self.file_path = file_path
        self.data = self.get_data()

    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return len(self.data)

    def get_data(self) -> AnimalData:
        """Returns the data from the database, terminates the program if the database doesn't exist"""
        if not os.path.exists(self.file_path):
            sys.exit(f"File: {self.file_path} could not be loaded. Exiting program...")

        with open(self.file_path, "r", encoding=ENCODER) as f:
            return json.load(f)


class DatabaseInfo:
    """Information from Database"""

    def __init__(self,index: int = 0, file_path: str = FILE):
        self.file = DatabaseFile(file_path)
        self.animal = self.__getitem__(index)

    def __getitem__(self, index):
        return self.file[index]

    @property
    def count(self) -> int:
        return len(self.file)

    @property
    def taxonomy(self):
        return self.animal.get("taxonomy")

    @property
    def characteristics(self):
        return self.animal.get("characteristics")

    @property
    def name(self):
        return self.animal.get("name")

    @property
    def scientific_name(self):
        return self.taxonomy.get("scientific_name")

    @property
    def diet(self):
        return self.characteristics.get("diet")

    @property
    def type(self):
        return self.characteristics.get("type")

    @property
    def color(self):
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
    def skin_type(self):
        return self.characteristics.get("skin_type")

    @property
    def locations(self):
        locations = self.animal.get("locations")
        locations = " and ".join(locations)
        and_count = locations.count(" and ")
        return locations.replace(" and ", ", ", and_count - 1)
