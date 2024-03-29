from tqdm import tqdm
from time import sleep

from tractor_beam.utils.globals import _f, check
from tractor_beam.utils.quantum import AbductState

import requests, feedparser, os, csv, yaml
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import pandas as pd

class Helpers:
    def __init__(self, state: AbductState):
        self.state = state
    async def _dataframe_to_yaml(self, df):
        dict_data = df.to_dict(orient="records")
        yaml_str = yaml.dump(dict_data, allow_unicode=True, default_flow_style=False)
        return yaml_str

    async def _parse_xml_recursive(self, elem, path='', namespaces=None, data=None):
        if namespaces is None:
            namespaces = {}
        if data is None:
            data = {}
        updated_path = f'{path}/{elem.tag.split("}")[-1]}' if path else elem.tag.split("}")[-1]
        if elem.text and elem.text.strip():
            data_key = updated_path
            data[data_key] = elem.text.strip()
        for attr, value in elem.attrib.items():
            data_key = f'{updated_path}/@{attr}'
            data[data_key] = value
        for child in elem:
            await self._parse_xml_recursive(child, updated_path, namespaces, data)
        return data

    async def _parse_primary(self, file_path):
        try:
            tree = ET.parse(file_path)
        except Exception as e:
            return pd.DataFrame([{"error": str(e)}])
        root = tree.getroot()
        namespaces = {'': 'http://www.sec.gov/edgar/thirteenffiler', 'ns1': 'http://www.sec.gov/edgar/common', 'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
        data = await self._parse_xml_recursive(root, namespaces=namespaces)
        return pd.DataFrame([data])

    async def _parse_table(self, file_path):
        try:
            tree = ET.parse(file_path)
        except Exception as e:
            return pd.DataFrame([{"error": str(e)}])
        root = tree.getroot()
        namespace = {'ns': 'http://www.sec.gov/edgar/document/thirteenf/informationtable'}
        data = []
        for info_table in root.findall('.//ns:infoTable', namespace):
            row = {}
            for child in info_table:
                tag = child.tag.split('}')[-1]
                if tag == 'shrsOrPrnAmt':
                    row['sshPrnamt'] = child.find('.//ns:sshPrnamt', namespace).text
                    row['sshPrnamtType'] = child.find('.//ns:sshPrnamtType', namespace).text
                elif tag == 'votingAuthority':
                    row['Sole'] = child.find('.//ns:Sole', namespace).text
                    row['Shared'] = child.find('.//ns:Shared', namespace).text
                    row['None'] = child.find('.//ns:None', namespace).text
                else:
                    row[tag] = child.text
            data.append(row)
        return pd.DataFrame(data)

    async def _analyze_xml(self, file_path):
        if 'primary_doc' in file_path:
            return await self._dataframe_to_yaml(await self._parse_primary(file_path))
        else:
            return await self._dataframe_to_yaml(await self._parse_table(file_path))

    async def _download_and_process_file(self, filing):
        response = requests.get(filing["url"], headers={"User-Agent": "Your User Agent"})
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            links = [a['href'] for a in soup.find_all('a', href=True) if 'InfoTable' in a['href'] or 'primary_doc' in a['href']]
            filing['attachments'] = [f"https://www.sec.gov{link}" for link in links]
            _filings = []
            for link in links:
                file_url = f"https://www.sec.gov{link}"
                file_response = requests.get(file_url, headers={"User-Agent": "Your User Agent"})
                if file_response.status_code == 200:
                    meta = 'primary_doc' if 'primary_doc' in link else 'info_table'
                    _filename = f"{meta}_{link.split('/')[5]}_{filing['updated'].split('T')[0]}.xml"
                    filename = _filename.replace('/', '')
                    file_path = os.path.join(self.state.conf.settings.proj_dir, filename)
                    filing['path'] = file_path
                    with open(file_path, 'wb') as file:
                        file.write(file_response.content)
                    yaml_content = await self._analyze_xml(file_path)
                    parsed_filename = filename.replace('.xml', '.txt')
                    with open(os.path.join(self.state.conf.settings.proj_dir, parsed_filename), 'w') as yfile:
                        yfile.write(f"{filing['title']} filed a {', '.join(filing['type'])} at the time of {filing['updated']}\n{yaml_content}")
                    _filings.append(filing)

        return _filings

    async def process(self, filings):
        total = len(filings)
        progress_bar = tqdm(filings, desc=(_f('wait',"BEACON[edgar].Stream 🏦 processing SEC filings")))
        finished = []
        for i, filing in enumerate(progress_bar):
            sleep(0.1) # just throttling
            try:
                response = requests.get(filing["url"], headers=self.state.job.custom['headers'])
                if response.status_code == 200:
                    _ = await self._download_and_process_file(filing)
                    finished.extend(_)
            except Exception as e:
                _f("warn",f"BEACON[edgar].Stream 🏦\n{e}\n{filing}")
            
            # Update progress bar color based on completion percentage
            progress_percentage = (i + 1) / total * 100
            if progress_percentage <= 30:
                progress_bar.colour = 'red'
            elif progress_percentage <= 60:
                progress_bar.colour = 'yellow'
            elif progress_percentage <= 90:
                progress_bar.colour = 'green'
            else:
                progress_bar.colour = 'magenta'

        return finished

class Stream:
    def __init__(self, state: AbductState):
        self.state = state
        self.helpers = Helpers(self.state)
        _f("success", "loaded BEACON[edgar].Stream 🏦")
    async def fetch(self):
        feed = feedparser.parse(self.state.job.url, request_headers=self.state.job.custom['headers'])
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
        processed = await self.helpers.process(filings)
        return processed

    async def run(self):
        filings = await self.fetch()
        return filings