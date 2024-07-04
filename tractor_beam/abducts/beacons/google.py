from tqdm import tqdm
import requests, os
from datetime import datetime, timedelta
from tractor_beam.utils.globals import _f
from tractor_beam.utils.quantum import AbductState

class Helpers:
    def __init__(self, state):
        self.state = state
    
    def process(self):
        today = datetime.now()
        date = (today - timedelta(days=200)).strftime('%Y-%m-%d')
        filetype_query = "%20OR%20".join([f"filetype:{ext}" for ext in self.state.job.types])
        _affix = f"%20after%3A{date}%20{filetype_query}"
        url = f"https://www.googleapis.com/customsearch/v1?key={self.state.job.custom['auth'][0]}&cx={self.state.job.custom['auth'][1]}&q={self.state.job.custom['query']+_affix}"
        finished = []
        def search(url):
            response = requests.get(url, headers={"User-Agent": "Custom User Agent"}, timeout=10)
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
        progress_bar = tqdm(initial_data["items"], desc="Scanning URLs")
        for item in progress_bar:
            title = item['link'].split("/")[-1]
            updated = datetime.now().strftime('%Y-%m-%d')
            _dict = {
                "url": url,
                "title": title,
                "updated": updated,
                "attachments": [],
                "type": [url.split(".")[-1]],
                "path": title
            }
            try:
                file_response = requests.get(item['link'], headers={"User-Agent": "Your User Agent"}, timeout=10)
            except Exception as e:
                _f("warn", f"BEACON[google].Stream 🏦\n{e}\n{item}")
            if file_response.status_code == 200:
                try:
                    _filename = f"{_dict['title']}_{_dict['updated'].split('T')[0]}.pdf"
                except Exception as e:
                    _f("warn", f"BEACON[google].Stream 🏦\n{e}\n{item}")
                filename = _filename.replace('/', '')
                file_path = os.path.join(self.state.conf.settings.proj_dir, filename)
                _dict['path'] = file_path
                try:
                    with open(file_path, 'wb') as file:
                        file.write(file_response.content)
                    finished.append(_dict)
                except OSError as e:
                    _f("warn", f"BEACON[google].Stream 🏦\n{e}\n{item}")
        return finished

class Stream:
    def __init__(self, state: AbductState):
        self.state = state
        self.helpers = Helpers(self.state)
        _f("success", "loaded BEACON[google].Stream 🔎")
    def fetch(self):
        processed_data = self.helpers.process()
        return processed_data

    async def run(self):
        filings = self.fetch()
        return filings
