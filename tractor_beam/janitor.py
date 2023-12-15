import chardet
from .supplies import Broom
from .utils import writeme, _f, check
import os

class Janitor:
    def __init__(self, conf: dict = None):
        """
        The function initializes an object with a path and an output path, and checks for invalid path
        and missing output path.
        
        :param path: The `path` parameter is used to specify a file path. It is an optional parameter,
        meaning it can be set to `None` if not needed
        :param o: The parameter "o" represents the output path. It is used to specify the location where
        the output of the code will be saved or written to
        """
        self.conf = conf.conf
        _f('info', 'Janitor initialized') if conf else _f('warn', f'no configuration loaded')
    def process(self, data: dict=None):
        """
        The function processes a file by reading its contents, detecting the encoding, and performing
        specific actions based on the file type.
        :return: the result of the `writeme` function call, which is not shown in the provided code.
        """
        proj_path = os.path.join(self.conf["settings"]["proj_dir"],self.conf["settings"]["name"])
        if data and check(proj_path):
            for d in data:
                with open(d['path'], 'rb') as f:
                    _ = f.read()
                    enc = chardet.detect(_)['encoding']
                    if enc is None:
                        enc = 'utf-8'
                    try:
                        if d['path'].endswith('.xml'):
                            _t = Broom(copy=_.decode(enc)).sweep(xml=True)
                        else:
                            _t = Broom(copy=_.decode(enc)).sweep()
                        writeme(_t.encode(), os.path.join('/'.join(d['path'].split('/')[:-1]), d['path'].split('/')[-1].split('.')[0]+'_cleaned.txt'))
                    except Exception as e:
                        _f('fatal', f'markup encoding - {e} | {_}')
        else:
            return _f('fatal', 'invalid path')
    def destroy(self, confirm: str = None):
        """
        The function `destroy` removes a file if the confirmation matches the file name.
        
        :param confirm: The `confirm` parameter is used to confirm the destruction of a file. It should
        be set to the name of the file that you want to destroy
        :return: a message indicating whether the file was successfully destroyed or not.
        """
        if not check(self.o):
            return _f('fatal', 'invalid path')
        if confirm==self.o.split('/')[-1]:
            os.remove(self.o), _f('warn', f'{confirm} destroyed from {self.o}')
        else:
            _f('fatal','you did not confirm - `Receipts.destroy(confirm="file_name")`')
        