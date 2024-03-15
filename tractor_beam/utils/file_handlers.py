import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import PyPDF2, chardet

from tractor_beam.utils.globals import _f

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError

class XMLProcessor:
    def __init__(self, filepath):
        self.filepath = filepath
        self.tree = None
        self.root = None

    def read(self):
        try:
            self.tree = ET.parse(self.filepath)
            self.root = self.tree.getroot()
        except ParseError as e:
            raise e

    def _process_element(self, element, level=0):
        if element is None:
            return ''  # Return an empty string if the element is None
        content = f"{'#' * (level + 2)} {element.tag}\n\n"
        if element.text and element.text.strip():
            content += f"> {element.text.strip()}\n\n"
        for attr, value in element.attrib.items():
            content += f"- **{attr}**: {value}\n"
        for child in element:
            content += self._process_element(child, level + 1)
        return content

    def export_to_markdown(self, output_filepath):
        if self.root is None:
            _f("warn", f"cannot export to Markdown using XML parser")
            return None
        with open(output_filepath, 'w', encoding='utf-8') as md_file:
            content = self._process_element(self.root)
            md_file.write(content)


class PDFProcessor:
    def __init__(self, filepath):
        self.filepath = filepath
        self.pages_text = []  # Initialize pages_text to ensure the attribute always exists

    def read(self):
        with open(self.filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            self.pages_text = [reader.pages[page_num].extract_text() for page_num in range(len(reader.pages))]

    def export_to_markdown(self, output_filepath):
        if not self.pages_text:
            self.read()  # Attempt to read the PDF file again
        
        if self.pages_text is None:
            _f("warn", f"cannot export to Markdown. PDF file {self.filepath} was not successfully parsed.")
            return
        else:
            with open(output_filepath, 'w', encoding='utf-8') as md_file:
                for i, page_text in enumerate(self.pages_text):
                    md_file.write(f"## Page {i + 1}\n\n{page_text}\n\n")

class HTMLProcessor:
    def __init__(self, filepath):
        self.filepath = filepath

    def read(self):
        with open(self.filepath, 'rb') as file:
            result = chardet.detect(file.read())
            encoding = result['encoding']
        with open(self.filepath, 'r', encoding=encoding) as f:
            content = f.read()
            self.soup = BeautifulSoup(content, 'html.parser')

    def _format_link(self, tag):
        return f"[{tag.text.strip()}]({tag.get('href')})"

    def _format_image(self, tag):
        return f"![{tag.get('alt', '').strip()}]({tag.get('src')})\n\n"

    def export_to_markdown(self, output_filepath):
        if not self.soup or not hasattr(self.soup, 'body') or self.soup.body is None:
            _f("warn", f"soup object is None or body tag not found in HTML content for {self.filepath}.")
            return
        with open(output_filepath, 'w', encoding='utf-8') as md_file:
            for tag in self.soup.body.find_all(True):
                if tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    md_file.write(f"{'#' * int(tag.name[1])} {tag.text.strip()}\n\n")
                elif tag.name == 'p':
                    for content in tag.contents:
                        if content.name == 'a':
                            md_file.write(self._format_link(content))
                        else:
                            md_file.write(f"{content}\n\n")
                elif tag.name == 'ul':
                    for li in tag.find_all('li'):
                        md_file.write(f"- {li.text.strip()}\n")
                    md_file.write("\n")
                elif tag.name == 'img':
                    md_file.write(self._format_image(tag))
