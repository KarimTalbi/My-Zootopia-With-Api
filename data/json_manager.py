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

    def get_data(self) -> AnimalData:
        """Returns the data from the database, terminates the program if the database doesn't exist"""
        if not os.path.exists(self.file_path):
            sys.exit(f"File: {self.file_path} could not be loaded. Exiting program...")

        with open(self.file_path, "r", encoding=ENCODER) as f:
            return json.load(f)


class DatabaseInfo:
    """Information from Database"""

    def __init__(self, file_path: str = FILE):
        self.file = DatabaseFile(file_path)
