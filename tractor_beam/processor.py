import os, csv, socket
from datetime import datetime

from tractor_beam.utils.globals import _f
from tractor_beam.utils.file_handlers import XMLProcessor, PDFProcessor, HTMLProcessor
from tractor_beam.records.visit import VisitState
from tractor_beam.utils.config import Job

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

    def process_visits(self):
        visits_file_path = os.path.join(self.state.conf.settings.proj_dir, self.state.conf.settings.name, 'visit.csv')
        
        updated_rows = []
        field_names = []

        with open(visits_file_path, 'r', encoding='utf-8') as visits_file:
            csv_reader = csv.DictReader(visits_file)
            field_names = csv_reader.fieldnames
            
            if 'converted' not in field_names:
                field_names.append('converted')
            if 'converted_ts' not in field_names:
                field_names.append('converted_ts')
            
            for row in csv_reader:
                file_path = row.get('path', '').strip()
                if not file_path:
                    updated_rows.append(row)
                    continue
                
                converted_file_path = self._process_file(file_path)
                converted_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if converted_file_path:
                    row['converted'] = converted_file_path
                    row['converted_ts'] = converted_ts
                else:
                    row.setdefault('converted', 'conversion_failed')  # Only set if not already present
                    row.setdefault('converted_ts', '')  # Only set if not already present
                
                updated_rows.append(row)
                self.state.data.append({"converted":row, "converted_ts": converted_ts})

        # Write the updated data back to the CSV
        with open(visits_file_path, 'w', newline='', encoding='utf-8') as visits_file:
            csv_writer = csv.DictWriter(visits_file, fieldnames=field_names)
            csv_writer.writeheader()
            csv_writer.writerows(updated_rows)

    def _process_file(self, file_path):
        file_extension = os.path.splitext(file_path)[1].lower()
        output_file_path = f"{os.path.splitext(file_path)[0]}_converted.md"

        # Initialize processor as None for scope reasons
        processor = None

        if file_extension in ['.xml', '.html', '.htm']:
            try:
                if file_extension in ['.xml']:
                    processor = XMLProcessor(file_path)
                    processor.read()
                raise Exception("XML parsing failed.")  # Force failure for XML to HTML conversion.
            except Exception as e:  # Catch XML parsing failure or forced exception.
                _f("warn", f"XML parsing failed for {file_path}, attempting HTML parser.")
                processor = HTMLProcessor(file_path)  # Switch to HTMLProcessor for HTML files or failed XML files.

        elif file_extension in ['.pdf']:
            processor = PDFProcessor(file_path)
        else:
            _f("warn", f"unsupported file type for file {file_path}")
            return None

        # No need to read again for PDF, as it's done in the if-else block above
        if file_extension not in ['.pdf']:
            processor.read()
        try:
            processor.export_to_markdown(output_file_path)
        except Exception as e:
            _f("warn", f"failed to process {file_path} to Markdown: {e}")
            if file_extension in ['.pdf']:
                _f('wait', f"attempting to process {file_path} with `Mothership`")
                self.switch_to_advanced_conversion(file_path)
        _f("success", f"Processed {file_path} to {output_file_path}")
        
        return output_file_path
    
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
