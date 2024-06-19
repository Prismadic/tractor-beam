from tqdm import tqdm
from time import sleep
from lxml import etree
import io
import html2text

from tractor_beam.utils.globals import _f, check
from tractor_beam.utils.quantum import AbductState

import requests, feedparser, os, yaml
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import pandas as pd

class Helpers:
    def __init__(self, state: AbductState):
        self.state = state
        
    def _update_data(self, data, key, value):
        if key in data:
            if isinstance(data[key], list):
                data[key].append(value)
            else:
                data[key] = [data[key], value]
        else:
            data[key] = value

    def _get_namespaces(self, file_path):
        namespaces = {}
        for event, elem in ET.iterparse(file_path, events=['start-ns']):
            namespaces[elem[0]] = elem[1]
        return namespaces

    def _dataframe_to_yaml(self, df):
        dict_data = df.to_dict(orient='records')
        yaml_data = {}
        h = html2text.HTML2Text()
        h.ignore_links = True
        
        for row in dict_data:
            yaml_key = ''.join(''.join(str(value).split('/')[1:]) for value in row.values() if value is not None)
            if 'Text' in row.keys():
                if row['Text'] not in [None, '', ' ', 'null']:
                    yaml_value = row['Text']
                else:
                    yaml_value=''
            
                
                # Create a file-like object from the string
                markup = io.StringIO(yaml_value)
                
                # Check if the value is HTML
                if bool(BeautifulSoup(markup, "html.parser").find()):
                    # Convert HTML to plain text
                    yaml_value = h.handle(yaml_value)
                
                if yaml_key not in [None, '', ' ', 'null']:
                    yaml_data[yaml_key] = yaml_value
        
        yaml_str = yaml.dump(yaml_data, allow_unicode=True)
        return yaml_str

    def _parse_primary(self, file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()
        data = []

        def add_element_data(elem, path):
            tag = elem.tag.split('}')[-1]  # Remove namespace if present.
            text = elem.text.strip() if elem.text and elem.text.strip() else None
            attributes = dict(elem.attrib) if elem.attrib else None
            data.append([path, tag, text, attributes])

        def traverse_tree(elem, current_path=""):
            tag = elem.tag.split('}')[-1]  # Remove namespace if present.
            new_path = f"{current_path}/{tag}" if current_path else tag
            add_element_data(elem, new_path)
            for child in elem:
                traverse_tree(child, new_path)

        traverse_tree(root)

        # Only attempt to create a DataFrame if there's data collected.
        if data:
            # Create the DataFrame from the list of lists
            df = pd.DataFrame(data, columns=['Path', 'Tag', 'Text', 'Attributes'])
            return df
        else:
            # Handle the case where no data was collected.
            return pd.DataFrame(columns=['Path', 'Tag', 'Text', 'Attributes'])

    def _parse_table(self, file_path):
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

    def _analyze_xml(self, file_path):
        try:
            if 'infoTable' in df['Tag'].values:
                df = self._parse_table(file_path)
            else:
                df = self._parse_primary(file_path)
            try:
                yaml = self._dataframe_to_yaml(df)
                return yaml
            except Exception as e:
                print(f'{e}')
        except Exception as e:
            print(f'{e}')

    def _download_and_process_filing(self, filing):
        response = requests.get(filing["url"], headers={"User-Agent": "Your User Agent"})
        _ = []
        metadata = ['pre.xml', 'def.xml', 'lab.xml', 'cal.xml']
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            links = list({os.path.basename(a['href']): a['href'] for a in soup.find_all('a', href=True)}.values())  # if 'InfoTable' in a['href'] or 'primary_doc' in a['href']
            links = [f"https://www.sec.gov{link}" for link in links]
            for link in links:
                if not any(metadata in link.split("_") for metadata in metadata):
                    if link.endswith('.xml'):
                        __ = {'url': filing['url'], 'title': filing['title'], 'updated': filing['updated'], 'path': ''}
                        file_response = requests.get(link, headers={"User-Agent": "Your User Agent"})
                        if file_response.status_code == 200:
                            _filename = f"{link.split('/')[-1].split('.')[0]}_{link.split('/')[5]}_{filing['title']}_{filing['updated'].split('T')[0]}.xml"
                            filename = _filename.replace('/', '')
                            file_path = os.path.join(self.state.conf.settings.proj_dir, filename)
                            with open(file_path, 'wb') as file:
                                file.write(file_response.content)
                            parsed_filename = filename
                            parsed_filename = parsed_filename.replace('.xml', '.txt')
                            __['path'] = parsed_filename
                            yaml_content = self._analyze_xml(file_path)
                            if (yaml_content == []):
                                _f('warn', f'{parsed_filename} = {yaml_content}?')
                            else:
                                with open(os.path.join(self.state.conf.settings.proj_dir, parsed_filename), 'w') as yfile:
                                    yfile.write(f"{filing['title']} SEC EDGAR filing at the time of {filing['updated']}\n{yaml_content}")
                            _.append(__)
                    elif link.endswith('.pdf'):
                        __ = {'url': filing['url'], 'title': filing['title'], 'updated': filing['updated'], 'path': ''}
                        file_response = requests.get(link, headers={"User-Agent": "Your User Agent"})
                        if file_response.status_code == 200:
                            _filename = f"{link.split('/')[-1].split('.')[0]}_{link.split('/')[5]}_{filing['title']}_{filing['updated'].split('T')[0]}.pdf"
                            filename = _filename.replace('/', '')
                            file_path = os.path.join(self.state.conf.settings.proj_dir, filename)
                            __['path'] = filename
                            with open(file_path, 'wb') as file:
                                file.write(file_response.content)
                            _.append(__)
        return _
    def process(self, filings):
        total = len(filings)
        progress_bar = tqdm(filings, desc=(_f('wait',"BEACON[edgar].Stream 🏦 processing SEC filings")))
        finished = []
        for i, filing in enumerate(progress_bar):
            sleep(0.1) # just throttling
            try:
                response = requests.get(filing["url"], headers=self.state.job.custom['headers'])
                if response.status_code == 200:
                    _ = self._download_and_process_filing(filing)
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
    def fetch(self):
        feed = feedparser.parse(self.state.job.url, request_headers=self.state.job.custom['headers'])
        filings = []
        for entry in feed.entries:
            url = entry.link
            title = entry.title
            updated = entry.updated
            _type = [x.term for x in entry.tags if x.label == 'form type']
            _dict = {
                "url": url,
                "title": title,
                "updated": updated,
                "attachments": [],
                "type": _type
            }
            filings.append(_dict)
        processed = self.helpers.process(filings)
        return [x for x in processed if x is not None]

    async def run(self):
        filings = self.fetch()
        return filings