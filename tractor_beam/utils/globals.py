from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm
from jsonschema import validate
from jsonschema.exceptions import ValidationError as ve
import os

def _f(tag: str = None, body: any = None):
    """
    The function `_f` takes a tag and a body of text, and prints the tag with an associated emoji and
    color code, followed by the body of text.
    
    :param tag: The `tag` parameter is a string that represents the tag for the log message. It can be
    one of the following values: "FATAL", "WARN", "INFO", "WAIT", or "SUCCESS"
    :param body: The `body` parameter is a string that represents the message or content that you want
    to display. It will be printed along with the tag and emoji
    """
    tags = [
        ("FATAL", "☠️", "\033[91m"),  # Red color for FATAL
        ("WARN", "🚨", "\033[93m"),   # Yellow color for WARN
        ("INFO", "ℹ️", "\033[94m"),   # Blue color for INFO
        ("WAIT", "☕️", "\033[96m"),    # Cyan color for WAIT
        ("SUCCESS", "🌊", "\033[92m") # Green color for SUCCESS
    ]
    matching_tags = [x for x in tags if x[0] == tag.upper()]
    if matching_tags:
        tag_text = matching_tags[0][0]
        emoji = matching_tags[0][1]
        color_code = matching_tags[0][2]
        print(f'{color_code}{emoji} {tag_text}: {body}\033[0m')  # Reset color after the text
    else:
        print(f'😭 UNKNOWN TAG - `{tag}`')

def check(path):
    """
    The function checks if a file or directory exists at the specified path.
    :return: a boolean value indicating whether the path specified by `self.path` exists or not.
    """
    return os.path.exists(path)

def check_headers(data):
    """
    The function `check_headers` checks if the `receipts` object has a header set and returns it if it
    exists, otherwise it attempts to set the header using the keys of the first data item and returns
    the header if successful, otherwise it returns False.
    
    :param receipts: The `receipts` parameter is expected to be an object or data structure that
    contains information about receipts. It seems to have a `_schema` attribute that is expected to have
    a `header` key. The purpose of the `check_headers` function is to check if the `header` key is
    :return: The function `check_headers` returns either the headers of the receipts if they are already
    set, or it returns `True` if the headers are not set and it successfully detects the headers using
    `.keys()`. If there is an exception during the process, it returns `False`.
    """
    _f('wait','setting header with `.keys()`')
    try:
        h = list(data.keys())
        _f('success', f'headers detected as {h} from `.keys()`')
        return h
    except Exception as e:
        _f('fatal', f'{e}')
        return False

def dateme(receipt: dict = None):
    """
    The `dateme` function adds a timestamp to a receipt dictionary and returns a formatted string with
    the timestamp information.
    
    :param receipt: The `receipt` parameter is a dictionary that represents a receipt. It may contain
    various information related to a transaction, such as the items purchased, the total amount, the
    customer's name, etc
    :return: a formatted string that includes the word "timestamped" followed by the current timestamp.
    """
    _t = datetime.now()
    receipt['ts']=_t
    return _f('info',f'timestamped - {_t}')

def writeme(content: str | dict = None, path: str = None):
    """
    The function `writeme` writes the given content to a file specified by the path and returns a
    message indicating that the file has been written.
    
    :param content: The content parameter is the data that you want to write to the file. It can be a
    string, bytes, or any other data type that can be converted to bytes
    :param path: The `path` parameter is a string that represents the file path where the content will
    be written to
    :return: a string that indicates the status of the write operation. The string is formatted as
    "written - {path}", where {path} is the path parameter passed to the function.
    """
    with open(path, "wb") as _:
        _.write(content)
    return _f('info',f'written - {path}')

def readthis(path: str = None):
    return open(path,'r')

def files(content: str = None, url: str = None, types: list = None):
    """
    The function "files" takes in HTML content, a URL, and a list of file types, and returns a list of
    URLs that match the specified file types.
    
    :param content: The content parameter is the HTML content of a webpage
    :param url: The `url` parameter is the URL of the webpage from which you want to extract the file
    links
    :param types: The "types" parameter is a list of file extensions that you want to filter for. For
    example, if you pass ["pdf", "docx"], the function will only return URLs that end with ".pdf" or
    ".docx"
    :return: a list of URLs that match the specified file types.
    """
    _=[]
    soup = BeautifulSoup(content, "html.parser")
    urls = soup.find_all("a", href=True)
    for _u in tqdm(urls, desc=_f('wait',f'processing {url}')):
        _u = urljoin(url, _u["href"])
        if list(filter(_u.endswith, types)) != []:
            _.append(_u)
            _f('info',f'found - {_u}')
    return _

def dir_size(directory: str = None):
    """
    The `dir_size` function calculates the total size of all files in a given directory and its
    subdirectories.
    
    :param directory: The "directory" parameter is the path to the directory for which you want to
    calculate the total size
    :return: The function `dir_size` returns the total size of all files in the specified directory and
    its subdirectories.
    """
    _ = 0
    for path, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(path, file)
            _ += os.path.getsize(filepath)
    return _
    
def all_dir_size(directories: list = None):
    """
    The function `all_dir_size` calculates the size of all directories in a given list and returns the
    sizes in gigabytes.
    
    :param directories: The `directories` parameter is a list of directory paths
    :return: a dictionary where the keys are the directories and the values are the sizes of those
    directories in gigabytes.
    """
    sizes = {}
    for directory in directories:
        if os.path.isdir(directory):
            size_bytes = dir_size(directory)
            size_gb = size_bytes / (1024 ** 3)  # Convert bytes to GB
            sizes[directory] = size_gb
        else:
            print(f"Directory '{directory}' does not exist.")
    return sizes

def likethis(_j: dict = object):
    """
    The function `likethis` validates a JSON object `_j` against a JSON schema `_s` and returns `True`
    if the validation is successful, otherwise it returns a fatal error message.
    
    :param _j: The parameter `_j` is a dictionary object that represents the data you want to validate
    against a schema
    :type _j: dict
    :param _s: The parameter `_s` is expected to be an object that represents a JSON schema. It is used
    to validate the `_j` parameter, which is expected to be a dictionary (JSON object). The function
    `validate` is called with the `_j` and `_s` parameters to perform the validation
    :type _s: object
    :return: either True or an error message if the validation fails.
    """
    _schema = {
            "type": "object"
            , "properties": {
                "role": { "type": "string" }
                , "settings": {
                    "name": { "type": "string" }
                    , "proj_dir": { "type": "string" }
                    , "jobs": {
                        "type": "object"
                        , "properties": {
                            "url": { "type": "string" }
                            , "files": { "type": "array" }
                            , "recurse": { "type": "boolean" }
                            , "receipts": { "type": "string" }
                            , "janitor": { "type": "boolean" }
                            , "custom": { "type": "array" }
                        }
                    }
                }
            }
        }
    try:
        validate(_j, _schema)
    except ve as e:
        return _f('fatal',f'{e}')
    return True