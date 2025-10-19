from data import json_manager
from web import html_manager

AnimalData = list[dict[str, str | list[str] | dict[str, str]]]
html = html_manager.HtmlFormat()


def animal_info(info):
    output = ""
    for key, value in info.items():
        if key != "Name" and value:
            output += f"\n{' ' * 8}{html.strong(key + ':')} {html.br(value)}"
    return output


def get_animal_data(animals_data: AnimalData) -> str:
    """Filters AnimalData for Name, Diet, Location, Type and returns as a list"""
    animals = []
    output = ""
    for data in animals_data:
        animal_data = {
            "Name": data.get("name", None),
            "Diet": data["characteristics"].get("diet", None),
            "Locations": data.get("locations", [None]),
            "Type": data["characteristics"].get("type", None)
        }

        locations = animal_data.get("Locations", None)
        if locations:
            animal_data["Locations"] = " and ".join(locations)
            and_counter = animal_data["Locations"].count(" and ")

            if and_counter >= 2:
                animal_data["Locations"] = animal_data["Locations"].replace(" and ", ", ", and_counter - 1)

        output += f'{html.li(
            f'\n{" " * 4}{html.div(animal_data.get("Name"))}'
            f'\n{" " * 4}{html.p(animal_info(animal_data) + f"\n{" " * 4}")}\n'
        )}\n\n'

    return output


def main():
    pass
    animals_data = json_manager.DatabaseFile().get_data()
    animals = get_animal_data(animals_data)
    html_manager.HtmlDest().replace_html(animals)


if __name__ == "__main__":
    main()
