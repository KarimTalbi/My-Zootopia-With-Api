import os.path
from data_fetcher import fetch_data, Animal


class CreateHtml:
    """
    Creates an HTML file with a list of animals.
    """
    temp = 'animals_template.html'
    dest = 'animals.html'

    def __init__(self, animals: list[Animal], animal_name: str):
        """
        Initializes the CreateHtml object.
        """
        if not os.path.exists(self.temp):
            raise FileNotFoundError(
                f"Error: The required HTML file was not found at path: {self.temp}"
            )

        self.template = self.load()

        if not animals:
            self.output = f"<h2>The animal \"{animal_name}\" doesn't exist.</h2>"
            self.save()

        else:
            self.animals = animals
            self.animal = None
            self.output = ""
            self.run()

    def run(self) -> None:
        """
        Runs the HTML generation process.
        """
        for animal in self.animals:
            self.animal = animal
            self.top()
            self.middle()
            self.bottom()
        self.save()

    def load(self) -> str:
        """
        Loads the HTML template file.
        """
        with open(self.temp, "r", encoding='UTF-8') as f:
            return f.read()

    def top(self) -> None:
        """
        Adds the top section of an animal's card to the output.
        """
        self.output += (
            f'{" " * 12}<li class="cards__item">\n'
            f'{" " * 16}<div class="card__title">{self.animal.name}</div>\n'
            f'{" " * 16}<div class="card__text">\n'
            f'{" " * 20}<ul class="cards__list">\n'
        )

    def middle(self) -> None:
        """
        Adds the middle section of an animal's card to the output.
        """
        self.output += "".join([
            f'{" " * 24}<li><strong>{key}:</strong> {value}</li>\n'
            for key, value in self.animal if key != "name" and value
        ])

    def bottom(self) -> None:
        """
        Adds the bottom section of an animal's card to the output.
        """
        self.output += (
            f'{" " * 20}</ul>\n'
            f'{" " * 16}</div>\n'
            f'{" " * 12}</li>\n\n'
        )

    def save(self) -> None:
        """
        Saves the generated HTML to a file.
        """
        with open(self.dest, "w", encoding='UTF-8') as f:
            f.write(
                self.template.replace(
                    f"{' ' * 12}__REPLACE_ANIMALS_INFO__", self.output
                )
            )


def main() -> None:
    """
    Gets user input, fetches animal data, and generates an HTML file.
    """
    while True:
        try:
            animal_name = input("Enter animal name: ").strip()

            if not animal_name:
                raise ValueError("can't be empty")

            animals, skin_types = fetch_data(animal_name)

            if not animals:
                CreateHtml(animals, animal_name)
                break

            while True:
                try:
                    print("Skin types:")
                    for i, skin in enumerate(skin_types):
                        print(f"{i + 1}. {skin}")

                    skin_filter = input("Chose filter or leave empty: ").strip()

                    if not skin_filter:
                        break

                    if (
                            not skin_filter.isdigit()
                            or int(skin_filter) >= len(skin_types) + 1
                            or int(skin_filter) < 0
                    ):
                        raise ValueError(
                            f"\n{skin_filter} is not a valid option. Try again."
                        )

                    skin_filter = skin_types[int(skin_filter) - 1]

                    break

                except Exception as e:
                    print(e)

            filtered_animals = []

            for animal in animals:
                if animal.skin_type == skin_filter or not skin_filter:
                    filtered_animals.append(animal)

            CreateHtml(filtered_animals, animal_name)

            break

        except Exception as e:
            print(e)

    print("File saved successfully!")


if __name__ == "__main__":
    main()
