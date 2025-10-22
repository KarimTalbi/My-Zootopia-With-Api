from data import json_manager
from web import html_manager

AnimalData = list[dict[str, str | list[str] | dict[str, str]]]
html = html_manager.HtmlFormat()
info = json_manager.DatabaseInfo


def serialization_helper(obj_data: dict[str, str]) -> str:
    """Helper function for animal_serialization"""
    output = ""
    for key, value in obj_data.items():
        if key != "Name" and value:
            output += f"\n{' ' * 8}{html.strong(key + ':')} {html.br(value)}"
    return output


def animal_serialization(animal_obj: dict[str, str]) -> str:
    """Formats Data for a single Animal Object"""
    output = ""
    output += f'{html.li(
            f'\n{" " * 4}{html.div(animal_obj.get("Name"))}'
            f'\n{" " * 4}{html.p(serialization_helper(animal_obj) + f"\n{" " * 4}")}\n'
        )}\n\n'
    return output


def get_animal_data() -> str:
    """Filters AnimalData for Name, Diet, Location, Type and returns as a list"""
    output = ""
    for i in range(info().count):
        animal: dict[str, str] = {
            "Name": info(i).name,
            "Scientific Name": info(i).scientific_name,
            "Diet": info(i).diet,
            "Locations": info(i).locations,
            "Type": info(i).type,
            "Color": info(i).color,
            "Skin Type": info(i).skin_type,
        }

        output += animal_serialization(animal)
    return output


def main() -> None:
    replace_with = get_animal_data()
    html_manager.HtmlDest().replace_html(replace_with)


if __name__ == "__main__":
    main()
