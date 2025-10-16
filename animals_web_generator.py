import json
import os
import sys

# --- constants ---
FILE = os.path.abspath("animals_data.json")

# --- Type Aliases for clarity ---
AnimalData = list[dict[str, str | list[str] | dict[str, str]]]

# --- File handling ---
def load_data(file_path: str = FILE) -> AnimalData:
    """Loads a JSON file and returns content if it exists"""
    if not os.path.exists(file_path):
        sys.exit(f"File: {file_path} could not be loaded. Exiting program...")

    with open(file_path, "r", encoding="UTF-8") as handle:
        return json.load(handle)


def get_animal_data(animals_data: AnimalData) -> list[str]:
    """Filters AnimalData for Name, Diet, Location, Type and returns as a list"""
    animals = []
    for data in animals_data:
        animal_data = {
            "Name": data.get("name", None),
            "Diet": data["characteristics"].get("diet", None),
            "Location": data.get("locations", [None])[0],
            "Type": data["characteristics"].get("type", None)
        }

        animal = [f"{key}: {value}" for key, value in animal_data.items() if value]
        animals.append(animal)
    return animals

# --- Helper Functions ---
def print_lines(lines) -> None:
    for sub in lines:
        for line in sub:
            print(line)
        print()


def main():
    animals_data = load_data()
    animal = get_animal_data(animals_data)
    print_lines(animal)


if __name__ == "__main__":
    main()
