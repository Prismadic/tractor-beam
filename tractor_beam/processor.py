import os, csv, socket, glob
from datetime import datetime

from tractor_beam.utils.globals import _f
from tractor_beam.utils.file_handlers import PDFProcessor
from tractor_beam.visits.visit import VisitState
from tractor_beam.utils.config import Job

from marker.models import load_all_models
from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class ProcessState:
    conf: Optional[dict] = None
    job: Optional[dict] = None
    data: List[Dict[str, str]] = field(default_factory=list)

class VisitsProcessor:
    def __init__(self, conf: VisitState, job: Job = None, cb=None):
        try:
            self.state = VisitState(conf=conf.conf, job=job)
            self.cb = cb
            return _f('info', f'Processor initialized\n{self.state}')
        except Exception as e:
            return _f('warn', f'no configuration loaded\n{e}')

    async def process_visits(self):
        model_lst = load_all_models()
        visits_file_path = os.path.join(self.state.conf.settings.proj_dir, self.state.conf.settings.name, 'visit.csv')
        field_names = []
        processed_files = set()
        last_processed_index = -1

        # Read existing data and find the last processed row
        with open(visits_file_path, 'r', encoding='utf-8') as visits_file:
            csv_reader = csv.DictReader(visits_file)
            field_names = csv_reader.fieldnames
            rows = list(csv_reader)
            
            for i, row in enumerate(rows):
                if row.get('converted_path') and row.get('converted_ts'):
                    processed_files.add(row['path'].strip())
                    last_processed_index = i

        # Add new fields if they don't exist
        for field in ['converted_path', 'converted_ts']:
            if field not in field_names:
                field_names.append(field)

        # Process unprocessed rows
        for i in range(last_processed_index + 1, len(rows)):
            row = rows[i]
            file_path = row.get('path', '').strip()
            
            if not file_path or file_path in processed_files:
                continue

            _path = os.path.join(file_path)
            converted_file_path = await self._process_file(_path, model_lst)
            converted_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if converted_file_path:
                row['converted_path'] = converted_file_path
                row['converted_ts'] = converted_ts
            else:
                row['converted_path'] = 'conversion_failed'
                row['converted_ts'] = ''

            processed_files.add(file_path)
            self.state.data.append({"converted": row})

            # Write the updated row immediately
            with open(visits_file_path, 'a', newline='', encoding='utf-8') as visits_file:
                csv_writer = csv.DictWriter(visits_file, fieldnames=field_names)
                if visits_file.tell() == 0:  # If file is empty, write header
                    csv_writer.writeheader()
                csv_writer.writerow(row)

    async def _process_file(self, file_path, model_lst):
        file_extension = os.path.splitext(file_path)[1].lower()
        output_file_path = f"{os.path.splitext(file_path)[0]}_converted.md"

        if os.path.exists(output_file_path):
            return output_file_path

        # Initialize processor as None for scope reasons
        processor = None
        if file_extension in ['.xml', '.html', '.htm', '.txt']:
            try:
                processor.read()
            except Exception as e:
                _f("warn", f"HTML parsing failed for {file_path}\n{e}")
            if processor:
                export_path = processor.export_to_markdown(self.state.conf.settings.proj_dir, output_file_path)
                _f("success", f"Processed {file_path} to {output_file_path}")
        elif file_extension in ['.pdf']:
            try:
                processor = PDFProcessor(file_path)
                _f("wait", f"processing {file_path}...")
            except Exception as e:
                _f("warn", f"PDF parsing failed for {file_path}\n{e}")
                _f('wait', f"attempting to process {file_path} with `Mothership`")
                self.switch_to_advanced_conversion(file_path)
            if processor:
                export_path = await processor.export_to_markdown(self.state.conf.settings.proj_dir, output_file_path, model_lst)
                _f("success", f"Processed {file_path} to {export_path}")
        
        return export_path

        
    def switch_to_advanced_conversion(self, file_path):
        advanced_converter = Mothership()
        advanced_converter.contact()
        advanced_converter.repulse(file_path)
        advanced_converter.close()

class Mothership:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.socket = None

    def contact(self):
        if self.socket is not None:
            _f("warn", "already in contact with `Mothership`")

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        _f("success", f"contacted {self.host}:{self.port}")

    def repulse(self, file_path):
        if self.socket is None:
            raise RuntimeError("no contact with `Mothership`")

        _f("wait", f"sending {file_path} to `Mothership`...")
        with open(file_path, 'rb') as file:
            while chunk := file.read(4096):
                self.socket.sendall(chunk)

        _f("success", "file has been repulsed successfully.")

    def close(self):
        if self.socket:
            self.socket.close()
            self.socket = None
            _f("warn", "closed contact with `Mothership`")
