import os, requests, re, importlib, time
from tractor_beam.utils.globals import writeme, files, _f, check
from tractor_beam.clone.beacons import *
from youtube_transcript_api import YouTubeTranscriptApi 
from youtube_transcript_api.formatters import TextFormatter

class Abduct:
    def __init__(self, conf: dict = None):
        """
        The function initializes an object with optional parameters and checks if a URL is provided.
    
        :param url: The `url` parameter is used to specify the URL of a webpage that you want to process
        or scrape data from
        :param recurse: The `recurse` parameter is a boolean flag that determines whether the code
        should recursively process the URL. If `recurse` is set to `True`, the code will process the URL
        and all its subpages recursively. If `recurse` is set to `False`, the code will only, defaults
        to False (optional)
        :param custom: The "custom" parameter is a boolean flag that indicates whether the code should
        use custom settings or not. If it is set to True, the code will use custom settings. If it is
        set to False, the code will use default settings, defaults to False (optional)
        :return: If the `url` parameter is `None`, the function will return a call to `_f('fatal', 'no
        url passed')`. Otherwise, it will return `None`.
        """
        self.data = []
        try:
            self.conf = conf.conf
            _f('info', 'Abduct initialized')
        except Exception as e:
            _f('warn', f'no configuration loaded\n{e}')
    def download(self, o: bool=False, f: str=None):
        """
        The `download` function is used to download files from a given URL, with options for specifying
        the download path, headers, and file types.
        
        :param path: The `path` parameter is used to specify the directory where the downloaded file
        will be saved. If no path is provided, a warning message will be displayed
        :param sneaky: The `sneaky` parameter is a boolean flag that determines whether to use sneaky
        headers when making the HTTP request. If `sneaky` is `True`, the request will include headers
        that mimic a common user agent (PostmanRuntime/7.23.3) and accept various, defaults to True
        (optional)
        :param types: The `types` parameter is used to specify the file types that you want to download.
        It is used in conjunction with the `recurse` parameter to recursively download files of the
        specified types from the URL
        :param o: The 'o' parameter is a boolean flag that determines whether to overwrite existing
        files when downloading. If 'o' is set to True, existing files will be overwritten. If 'o' is set
        to False, a warning message will be displayed and the file will not be downloaded if it already
        exists, defaults to False (optional)
        :return: either a tuple containing the downloaded files and a success message, or it returns an
        error message and False.
        """
        proj_path = os.path.join(self.conf["settings"]["proj_dir"],self.conf["settings"]["name"])            
        block_size = 1024
        for job in self.conf['settings']['jobs']:
            print(job)
            headers = {
                "User-Agent": "PostmanRuntime/7.23.3",
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive"
            } if len(job["custom"][0]["headers"]) == 0 \
                else job["custom"][0]["headers"]
            f = f'{proj_path}/{job["url"].split("/")[-1]}'
            if self.conf['role'] == 'watcher':
                module = importlib.import_module("tractor_beam.clone.beacons."+job['beacon'])
                watcher_class = getattr(module, 'Stream')
                watcher = watcher_class(self.conf,job)
                filings = watcher.run()
                for filing in filings:
                    filing_path = os.path.join(proj_path, filing['title'])
                    if job['recurse']:
                        dedupe = [] # temp fix for multiple paths, same name
                        for attachment in filing['attachments']:
                            if attachment.split('/')[-1] not in dedupe:
                                dedupe.append(attachment.split('/')[-1])
                                time.sleep(0.5)
                                file_name = filing['title'].replace("/", "_") + '_' + attachment.split('/')[-1]
                                attachment_path = os.path.join(filing_path, file_name)
                                response = requests.get(attachment, stream=True, headers=headers)
                                response.raise_for_status()
                                try:
                                    writeme(response.iter_content(block_size), attachment_path)
                                    self.data.append({ "file": file_name, "path": attachment_path})
                                except Exception as e:
                                    _f('fatal',e), False
                    else:
                        self.data.append({"file":job["url"], "path":attachment_path})
                        writeme(response.iter_content(block_size), f) if safe else _f('fatal',response.status_code)
                        return self.data
                self._files=filings
                _f('success', f'{len(self._files)} downloaded')
                return self.data
            if job['recurse'] and job['types']:
                response = requests.get(job['url'], stream=True, headers=headers)
                response.raise_for_status()
                safe = response.status_code==200
                _files = files(response.content, job['url'], job['types'])
                for _file in _files:
                    f = f'{proj_path}/{_file.split("/")[-1]}'
                    if o and check(f):
                        self.data.append({"file":_file, "path":f'{os.path.join(proj_path,_file.split("/")[-1])}'})
                        writeme(response.iter_content(block_size), f) if safe else _f('fatal',response.status_code), False
                    elif not check(f):
                        self.data.append({"file":_file, "path":f'{os.path.join(proj_path,_file.split("/")[-1])}'})
                        writeme(response.iter_content(block_size), f) if safe else _f('fatal',response.status_code), False
                    else:
                        _f('warn',f'{_file.split("/")[-1]} already exists - set `o=True` to overwrite when downloading')
                        _files.remove(_file)
                self._files=_files
                _f('success', f'{len(_files)} downloaded')
                return self.data
            else:
                ''' Check if it is a youtube url'''
                isYT = re.search(r"(youtu.be)|(youtube.com)", job["url"])
                if safe and isYT:
                    prefix = re.search("(?s:.*)/",job["url"])
                    YTID = job["url"][prefix.span()[1]:].replace("watch?v=","") if prefix else None
                    _f("INFO",f'{job["url"]} has youtube in it. id: {YTID}')
                    youtubeTranscriptResult = YouTubeTranscriptApi.get_transcript(YTID, languages=['en'])
                    YTID = YTID+".txt"
                    fileLocation = f'{proj_path}/{YTID}'
                    self.data.append({"file":YTID, "path":fileLocation})
                    youtubeScript = TextFormatter().format_transcript(youtubeTranscriptResult)
                    writeme(youtubeScript.encode(), fileLocation) if youtubeScript else _f('fatal',response.status_code)
                    return self.data
                elif safe:
                    self.data.append({"file":job["url"], "path":f'{os.path.join(proj_path,job["url"].split("/")[-1])}'})
                    writeme(response.content, f) if safe else _f('fatal',response.status_code)
                    return self.data


    def destroy(self, confirm: bool = None):
        """
        The `destroy` function deletes files or directories based on a confirmation and a specified
        path.
        
        :param confirm: The `confirm` parameter is used to confirm the destruction of files or
        directories. It should be set to the name of the parent directory that you want to confirm the
        destruction of
        :return: The code is returning a list comprehension that removes files from a directory if the
        confirmation matches the last part of the directory path. If the confirmation does not match, it
        returns a fatal error message.
        """
        if confirm==self.path.split('/')[-1]:
            _f('warn', f'{confirm if not self.recurse else len(self._files)} destroyed from {self.path}') if confirm is not None else None
            return [os.remove(f'{self.path}/{_file.split("/")[-1]}') for _file in self._files] if self.recurse else os.remove(self.path)
        else:
            return _f('fatal','you did not confirm - `SP.destroy(confirm="parent_dir")`')
