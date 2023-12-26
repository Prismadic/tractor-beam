import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as bs
import docx, PyPDF2, re, html
from io import BytesIO
from tractor_beam.utils.globals import _f

class Strip:
    def __init__(self, copy: str = None):
        """
        The function initializes an object with a copy of text data.
        
        :param copy: The `copy` parameter is used to specify the data that should be copied to the `ml`
        attribute of the object being initialized. If `copy` is `None`, it means that no data is being
        copied and a fatal error message is returned. If `copy` is not `None`,
        :return: In this code, if the `copy` parameter is `None`, the function will return a call to
        `_f` function with the arguments `'fatal'` and `'no copy/data set - Strip(copy=text_data)'`. If
        the `copy` parameter is not `None`, the function will set the `ml` attribute of the object to
        the value of `copy`. It does not explicitly
        """
        if copy==None:
            return _f('fatal', 'no copy/data set - `Strip(copy=text_data)`')
        else:
            self.ml=copy
    def sanitize(self, xml: bool = False):
        """
        The `sanitize` function takes in an XML or HTML string and returns a cleaned version of the text
        content, either as plain text or as a formatted string with tag names.
        
        :param xml: The `xml` parameter is a boolean flag that indicates whether the input should be
        treated as XML or not. If `xml` is set to `True`, the function will parse the input as XML using
        the `ElementTree` module and extract the text content of each element. If `xml`, defaults to
        False (optional)
        :return: The code is returning the text content of an XML or HTML document, depending on the
        value of the `xml` parameter. If `xml` is `True`, it returns the text content of the XML
        document. If `xml` is `False`, it returns the text content of the HTML document.
        """
        if xml:
            r = ET.fromstring(self.ml)
            _r = ""
            for e in r.iter():
                if e.text and e.tag:
                    try:
                        _r += f"{e.tag.split('}')[1]}: {e.text}\n"
                    except:
                        _r += f"{e.tag}: {e.text}\n"
            return _r
        else:
            _s = bs(self.ml, 'html.parser')
            _r = _s.get_text(separator=' ')
            _c = html.unescape(_r)
            _c = re.sub(r'<[^>]+>', '', _c)
            c = _c.replace('\n', ' ').replace('\t', ' ')
            return c
    def wash(self):
        """
        The function reads the contents of a PDF or DOCX file and returns the extracted text.
        :return: The code is returning the extracted text from a PDF or DOCX file.
        """
        with open(self.path, 'rb') as f:
            _r = f.read()
            try:
                if self.path.endswith('.pdf'):
                    p = PyPDF2.PdfReader(BytesIO(_r))
                    _t = "\n".join([_p.extract_text() for _p in p.pages])
                elif self.path.endswith('.docx'):
                    _d = docx.Document(BytesIO(_r))
                    _t = ""
                    for paragraph in _d.paragraphs:
                        _t += paragraph.text + '\n'
                # maybe don't need to sanitize?
                # return Strip(copy=text).sanitize()
                return _t
            except Exception as e:
                _f('fatal', f'document: {e} | {self.path}')

class Custom:
    def __init__(self, copy: str = None):
        """
        The function initializes an object with an optional copy parameter.
        
        :param copy: The `copy` parameter is an optional argument that allows you to specify a copy of
        some data. If no copy is provided, it defaults to `None`
        :return: In this code snippet, if the `copy` parameter is `None`, the function will return a
        call to `_f` function with the arguments `'fatal'` and `'no copy/data set -
        Custom(copy=text_data)'`. The return value of the `_f` function is not specified in the code
        snippet, so it is unclear what will be returned.
        """
        if copy==None:
            return _f('fatal', 'no copy/data set - `Custom(copy=text_data)`')