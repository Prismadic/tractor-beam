from bs4 import BeautifulSoup
import chardet
from tractor_beam.utils.globals import _f

from marker.convert import convert_single_pdf
from marker.models import load_all_models
from marker import output

class PDFProcessor:
    def __init__(self, filepath):
        self.filepath = filepath
    
    def load_models(self):
        return load_all_models()

    async def export_to_markdown(self, _dir, output_filepath, model_lst):
        try:
            full_text, doc_images, out_meta = convert_single_pdf(self.filepath, model_lst=model_lst)
            result = output.save_markdown(_dir, output_filepath.split('/')[-1], full_text, doc_images, out_meta)
            return result
        except Exception as e:
            return e

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