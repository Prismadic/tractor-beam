import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import PyPDF2, chardet

from tractor_beam.utils.globals import _f

from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import chardet
import re

class MarkupProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.content = self.read()

    def read(self):
        with open(self.file_path, 'rb') as f:
            raw_data = f.read()
            encoding = chardet.detect(raw_data)['encoding'] or 'utf-8'
            return raw_data.decode(encoding, errors='replace')

    def remove_html_tags(self, text):
        # Remove HTML tags from the text
        soup = BeautifulSoup(text, 'html.parser')
        text_without_tags = soup.get_text(separator=' ')
        return text_without_tags

    def xml_to_string(self, xml_data):
        try:
            root = ET.fromstring(xml_data)
            result = ""
            for element in root.iter():
                if element.text and element.tag:
                    try:
                        result += f"{element.tag.split('}')[1]}: {element.text}\n"
                    except IndexError:
                        result += f"{element.tag}: {element.text}\n"
            return self.remove_html_tags(result)
        except ET.ParseError as e:
            # Handle or log the parse error
            _f('warn', f"Error parsing XML: {e}, attempting to remove tags and return raw data.")
            return self.remove_html_tags(xml_data)

    def process(self):
        if self.file_path.endswith('.xml'):
            processed_text = self.xml_to_string(self.content)
        else:
            processed_text = self.content
        return self.remove_html_tags(processed_text)

    def export_to_markdown(self, output_filepath):
        with open(output_filepath, 'w', encoding='utf-8') as md_file:
            content = self.process()
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