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
            return
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
        self.soup = None

    def read(self):
        with open(self.filepath, 'rb') as file:
            result = chardet.detect(file.read(1024))  # Read a sample for encoding detection
            encoding = result.get('encoding', 'utf-8')  # Default to utf-8 if chardet is unsure

        try:
            with open(self.filepath, 'r', encoding=encoding, errors='replace') as f:
                content = f.read()
                self.soup = BeautifulSoup(content, 'html.parser')
        except UnicodeDecodeError as e:
            _f('warn', e)
    def _format_link(self, tag):
        return f"[{tag.text.strip()}]({tag.get('href')})"

    def _format_image(self, tag):
        return f"![{tag.get('alt', '').strip()}]({tag.get('src')})\n\n"

    def _process_contents(self, contents):
        output = ""
        for content in contents:
            if content.name == 'a':
                output += self._format_link(content)
            elif content.name == 'img':
                output += self._format_image(content)
            else:
                output += f"{content}\n\n"
        return output

    def export_to_markdown(self, output_filepath):
        if not self.soup or not hasattr(self.soup, 'body') or self.soup.body is None:
            print(f"Warning: soup object is None or body tag not found in HTML content for {self.filepath}.")
            return
        with open(output_filepath, 'w', encoding='utf-8') as md_file:
            for tag in self.soup.body.find_all(True):
                if tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    md_file.write(f"{'#' * int(tag.name[1])} {tag.text.strip()}\n\n")
                elif tag.name == 'p' or tag.name == 'li':
                    md_file.write(self._process_contents(tag.contents))
                elif tag.name == 'ul':
                    for li in tag.find_all('li'):
                        md_file.write(f"- {self._process_contents(li.contents)}")
                    md_file.write("\n")
                elif tag.name == 'img':
                    md_file.write(self._format_image(tag))