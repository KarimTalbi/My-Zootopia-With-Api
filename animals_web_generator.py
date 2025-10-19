from data import json_manager
from web import html_manager

AnimalData = list[dict[str, str | list[str] | dict[str, str]]]


def get_animal_data(animals_data: AnimalData) -> str:
    """Filters AnimalData for Name, Diet, Location, Type and returns as a list"""
    animals = []
    output = ""
    for data in animals_data:
        animal_data = {
            "Name": data.get("name", None),
            "Diet": data["characteristics"].get("diet", None),
            "Location": data.get("locations", [None])[0],
            "Type": data["characteristics"].get("type", None)
        }

        animal = [f"{key}: {value}" for key, value in animal_data.items() if value]
        output += (f'<li class="cards__item">\n'
                   f'{"<br/> \n".join(animal)}'
                   f'<br/>\n'
                   f'</li>\n')
    return output


def main():
    pass
    animals_data = json_manager.DatabaseFile().get_data()
    animals = get_animal_data(animals_data)
    html_manager.HtmlDest().replace_html(animals)


if __name__ == "__main__":
    main()
