from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os, json, requests

def fetch_to_write(state, attachment, headers, attachment_path, file_name, block_size, o=False):
    visited_files = {}
    if os.path.exists(attachment_path) and not o:
        pass
    else:
        response = requests.get(attachment, stream=True, headers=headers)
        response.raise_for_status()
        try:
            if attachment_path not in visited_files:
                writeme(response.iter_content(block_size), attachment_path)
                visited_files[attachment_path] = True  # Add the file path to the hash map
                state.data.append({"file": file_name, "path": attachment_path})
            else:
                _f('warn', f"File exists at {attachment_path}, skipping download.")
        except Exception as e:
            _f('fatal', f"couldn't fetch to write\n{e}"), False

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
    return os.path.exists(path)

def check_headers(data):
    _f('wait','setting header with `.keys()`')
    try:
        h = list(data[0].keys())
        _f('success', f'headers detected as {h} from `.keys()`')
        return h
    except Exception as e:
        _f('fatal', f'{e}')
        return []

def dateme(receipt: dict = None):
    _t = datetime.now()
    receipt['ts']=_t
    return _f('info',f'timestamped - {_t}')

def writeme(content, path: str = None):
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    if isinstance(content, (str, dict)):
        mode = 'w'
    else:
        mode = 'wb'
    
    with open(path, mode) as file:
        if isinstance(content, dict):
            file.write(json.dumps(content))
        elif callable(getattr(content, '__iter__', None)) and not isinstance(content, (str, bytes)):
            for chunk in content:
                file.write(chunk)
        else:
            file.write(content)
    return _f('info',f'written - {path}')

def readthis(path: str = None):
    return open(path,'r')

def files(content: str = None, url: str = None, types: list = None):
    if not types:
        return []  # Return an empty list if no types are specified
    
    soup = BeautifulSoup(content, "html.parser")
    found_urls = []
    for link in soup.find_all("a", href=True):
        if any(link['href'].endswith('.' + filetype) for filetype in types):
            full_url = urljoin(url, link['href'])
            found_urls.append(full_url)
    
    return found_urls

def dir_size(directory: str = None):
    _ = 0
    for path, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(path, file)
            _ += os.path.getsize(filepath)
    return _
    
def all_dir_size(directories: list = None):
    sizes = {}
    for directory in directories:
        if os.path.isdir(directory):
            size_bytes = dir_size(directory)
            size_gb = size_bytes / (1024 ** 3)  # Convert bytes to GB
            sizes[directory] = size_gb
        else:
            _f('warn', f"Directory '{directory}' does not exist.")
    return sizes
