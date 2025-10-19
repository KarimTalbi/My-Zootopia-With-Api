import os
import sys

HTML_TEMPLATE = os.path.join("web", "animals_template.html")
HTML_DEST = os.path.join("web", "animals.html")
REPLACE_STRING = "__REPLACE_ANIMALS_INFO__"
ENCODER = "UTF-8"
HtmlContent = str


class HtmlTemplate:
    """Loads HTML-Template File content"""

    def __init__(self, file_path: str = HTML_TEMPLATE):
        self.file_path = file_path

    def load_html(self) -> HtmlContent:
        """Returns the content of the HTML, terminates the program if the HTML doesn't exist"""
        if not os.path.exists(self.file_path):
            sys.exit(f"File: {self.file_path} could not be loaded. Exiting program...")  # TODO

        with open(self.file_path, "r", encoding=ENCODER) as f:
            return f.read()


class HtmlDest:
    """Saves data to new HTML File"""

    def __init__(self, file_path: str = HTML_TEMPLATE, dest_path: str = HTML_DEST):
        self.template = HtmlTemplate(file_path)
        self.destination = dest_path

    def save_html(self, content: HtmlContent) -> None:
        """Saves data to an HTML file, creates a file if it doesn't exist"""
        with open(self.destination, "w", encoding=ENCODER) as f:
            f.write(content)

    def replace_html(self, replace_by: str, to_replace: str = REPLACE_STRING):
        template = self.template.load_html()
        content = template.replace(to_replace, replace_by)
        self.save_html(content)


class HtmlFormat:
    """Formats strings to HTML Format"""

    def __init__(self):
        self.html = {
            "li": '<li class="cards__item">...</li>',
            "div": '<div class="card__title">...</div>',
            "p": '<p class="card__text">...</p>',
            "strong": '<strong>...</strong>',
            "br": '...<br/>'
        }

    def html_format(self, tag: str, text: str = ""):
        if tag not in self.html:
            return text
        return self.html[tag].replace("...", text)

    def li(self, text: str = ""):
        return self.html_format("li", text)

    def div(self, text: str = ""):
        return self.html_format("div", text)

    def p(self, text: str = ""):
        return self.html_format("p", text)

    def strong(self, text: str = ""):
        return self.html_format("strong", text)

    def br(self, text: str = ""):
        return self.html_format("br", text)
