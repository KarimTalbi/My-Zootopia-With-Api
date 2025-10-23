import os
import sys
from data.json_manager import DataInfo

FILE = os.path.join("web", "animals_template.html")
DEST = os.path.join("web", "animals.html")
ENCODE = "utf-8"


class HtmlLoad:

    def __init__(self, file: str = FILE, dest: str = DEST):
        self.file = file
        self.dest = dest
        self.template = self.load_html

    @property
    def load_html(self) -> str:
        """Returns the content of the HTML, terminates the program if it doesn't exist"""
        if not os.path.exists(self.file):
            sys.exit(f"File: {self.file} could not be loaded. Exiting program...")

        with open(self.file, "r", encoding=ENCODE) as f:
            return f.read()

    @property
    def load_dest(self) -> str:
        """Returns the content of the DEST HTML, terminates the program if it doesn't exist"""
        if not os.path.exists(self.dest):
            sys.exit(f"{self.dest} could not be saved")

        with open(self.dest, "r", encoding=ENCODE) as f:
            return f.read()


class HtmlSave(HtmlLoad):

    def __init__(self, file: str = FILE, dest: str = DEST):
        super().__init__(file)
        self.dest_path = dest

    def save_html(self, content: str) -> None:
        """Saves data to an HTML file, creates a file if it doesn't exist"""
        with open(self.dest_path, "w", encoding=ENCODE) as f:
            f.write(content)


class HtmlForm:
    """Formats strings into HTML Format"""

    def __init__(self, animal: dict[str, str]):
        self.animal = animal

    @property
    def top(self) -> str:
        return (
            f'{" " * 12}<li class="cards__item">\n'
            f'{" " * 16}<div class="card__title">{self.animal["Name"]}</div>\n'
            f'{" " * 16}<div class="card__text">\n'
            f'{" " * 20}<ul class="cards__list">\n'
        )

    @property
    def middle(self) -> str:
        return "".join(
            [f'{" " * 24}<li><strong>{key}:</strong> {value}</li>\n'
             for key, value in self.animal.items() if key != "Name" and value]
        )

    @property
    def bottom(self) -> str:
        return (
            f'{" " * 20}</ul>\n'
            f'{" " * 16}</div>\n'
            f'{" " * 12}</li>\n\n'
        )

    @property
    def serialize(self) -> str:
        return self.top + self.middle + self.bottom


class HtmlData(HtmlSave):

    def __init__(self, file: str = FILE, dest: str = DEST, skin: str = ""):
        super().__init__(file, dest)
        self.form = HtmlForm
        self.info = DataInfo
        self.skin = skin

    @property
    def animal_data(self) -> str:
        """Filters AnimalData for Name, Diet, Location, Type and returns as a list"""
        output = ""
        for i in range(self.info().count):
            animal: dict[str, str] = {
                "Name": self.info(i).name,
                "Scientific Name": self.info(i).scientific_name,
                "Diet": self.info(i).diet,
                "Locations": self.info(i).locations,
                "Type": self.info(i).type,
                "Color": self.info(i).color,
                "Skin Type": self.info(i).skin_type,
            }

            if animal.get("Skin Type") == self.skin or not self.skin:
                output += self.form(animal).serialize
        return output

    @property
    def list_style(self) -> str:
        return self.template.replace("</style>", '''
        .cards__list {
          list-style-type: disc;
          list-style-position: inside;
          margin: 0;
          padding: 20px 0 0 0;
        }
        </style>''')

    @property
    def encoding(self) -> str:
        return self.list_style.replace('<head>', '''<head>
        <meta charset="UTF-8">''')

    @property
    def replacer(self) -> str:
        return self.encoding.replace(f"{" " * 12}__REPLACE_ANIMALS_INFO__", self.animal_data)

    @property
    def web_generator(self) -> bool:
        new_html = self.replacer
        self.save_html(new_html)
        return new_html == self.load_dest
