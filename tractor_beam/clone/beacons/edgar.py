from tqdm import tqdm
from time import sleep
from tractor_beam.utils.globals import _f, files
import requests, feedparser

class Helpers:
    def __init__(self, job):
        self.job = job

    def process(self, filings):
        progress_bar = tqdm(filings, desc=_f('wait',"BEACON[edgar].Stream 🏦 processing SEC filings"))
        for filing in progress_bar:
            sleep(0.25) # just throttling
            try:
                response = requests.get(filing["url"], headers=self.job.custom['headers'])
                if response.status_code == 200:
                    filing_attachments = files(
                        content = response.content
                        , url = filing['url']
                        , types = self.job.types
                    )
                    for a_tag in filing_attachments:
                        if '/Archives/edgar/data/' in a_tag \
                            and a_tag not in filing['attachments']:
                                filing["attachments"].append(a_tag)
            except Exception as e:
                _f('fatal', f"BEACON[edgar].Stream 🏦\n{e}\n{filing}")
            progress_bar.set_postfix({"filing attachments": len(filing["attachments"])})
        return filings

class Stream:
    def __init__(self, conf: str | dict = None, job: str | dict = None):
        self.job = job
        self.conf = conf
        self.helpers = Helpers(self.job)
        _f("success", "loaded BEACON[edgar].Stream 🏦")
    def fetch(self):
        feed = feedparser.parse(self.job.url, request_headers=self.job.custom['headers'])
        filings = []
        for entry in feed.entries:
            url = entry.link
            title = entry.title
            updated = entry.updated
            _dict = {
                "url": url,
                "title": title,
                "updated": updated,
                "attachments": [],
                "type": [x.term for x in entry.tags if x.label == 'form type']
            }
            filings.append(_dict)
        processed = self.helpers.process(filings)
        return processed

    def run(self):
        filings = self.fetch()
        return filings