from tqdm import tqdm
import requests
from datetime import datetime, timedelta
from tractor_beam.utils.globals import _f

class Helpers:
    def __init__(self, job):
        self.job = job
        self.data = []  # To keep track of fetched PDF URLs
    
    def process(self):
        today = datetime.now()
        date = (today - timedelta(days=200)).strftime('%Y-%m-%d')
        filetype_query = "%20OR%20".join([f"filetype:{ext}" for ext in self.job.types])
        _affix = f"%20after%3A{date}%20{filetype_query}"
        url = f"https://www.googleapis.com/customsearch/v1?key={self.job.custom['auth'][0]}&cx={self.job.custom['auth'][1]}&q={self.job.custom['query']+_affix}"

        def search(url):
            response = requests.get(url, headers={"User-Agent": "Custom User Agent"})
            data = response.json()
            return data

        initial_data = search(url)
        if 'queries' not in initial_data:
            _f('warn', f"no data returned\n{initial_data}")
            return []
        while 'queries' in initial_data and len(initial_data['queries'].get('nextPage', [])) > 0:
            next_page_url = url + f"&start={initial_data['queries']['nextPage'][0]['startIndex']}"
            next_page_data = search(next_page_url)
            initial_data['items'] += next_page_data.get('items', [])
            initial_data['queries']['nextPage'] = next_page_data.get('queries', {}).get('nextPage', [])
        progress_bar = tqdm(initial_data["items"], desc="Processing URLs")
        for item in progress_bar:
            title = item['link'].split("/")[-1]
            updated = datetime.now().strftime('%Y-%m-%d')
            _dict = {
                "url": url,
                "title": title,
                "updated": updated,
                "attachments": [],
                "type": [url.split(".")[-1]]
            }
            self.data.append(_dict)
        return self.data

class Stream:
    def __init__(self, conf: str | dict = None, job: str | dict = None):
        self.job = job
        self.conf = conf
        self.helpers = Helpers(self.job)

    def fetch(self):
        processed_data = self.helpers.process()
        return processed_data

    def run(self):
        filings = self.fetch()
        return filings
