import json
import os
import sys

# --- constants ---
FILE_DATA = os.path.abspath("animals_data.json")
FILE_HTML_TEMPLATE = os.path.abspath("animals_template.html")
FILE_HTML = os.path.abspath("animals.html")
REPLACE_STRING = "__REPLACE_ANIMALS_INFO__"

# --- Type Aliases for clarity ---
AnimalData = list[dict[str, str | list[str] | dict[str, str]]]

# --- File handling ---
def load_data(file_path: str = FILE_DATA) -> AnimalData:
    """Loads a JSON file and returns content if it exists"""
    if not os.path.exists(file_path):
        sys.exit(f"File: {file_path} could not be loaded. Exiting program...")

    with open(file_path, "r", encoding="UTF-8") as handle:
        return json.load(handle)


def load_html(file_path: str = FILE_HTML_TEMPLATE) -> str:
    """Loads an HTML file and returns content if it exists"""
    if not os.path.exists(file_path):
        sys.exit(f"File: {file_path} could not be loaded. Exiting program...")

    with open(file_path, "r", encoding="UTF-8") as handle:
        return handle.read()


def save_html(content: str, file_path: str = FILE_HTML) -> None:
    """Saves data to an HTML file, creates a file if it doesn't exist"""
    with open(file_path, "w", encoding="UTF-8") as handle:
        handle.write(content)


def replace_data(replace_with: str, to_replace: str = REPLACE_STRING, content: str = load_html()) -> str:
    """replaces a specified part of the content with new content"""
    return content.replace(to_replace, replace_with)


def get_animal_data(animals_data: AnimalData) -> str:
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
        animals.append("\n".join(animal) + "\n")
    return "\n".join(animals)


def main():
    animals_data = load_data()
    animals = get_animal_data(animals_data)
    animal_html_new = replace_data(animals)
    save_html(animal_html_new)


if __name__ == "__main__":
    main()
