import os
import matplotlib.pyplot as plt
from .utils import _f

class SP:
    def __init__(self, path: str = None, save: str = None):
        """
        The function initializes an object with a path and save attribute, and displays a warning if no
        data set is provided.
        
        :param path: The `path` parameter is used to specify the path of the data set that you want to
        path. It is an optional parameter and if it is not provided, a warning message will be displayed
        indicating that no data set is specified
        :param save: The `save` parameter is used to specify the location where the data will be saved.
        It is an optional parameter, so if it is not provided, the data will not be saved
        :return: If `path` is `None`, then a warning message is returned. If `path` is not `None`, then
        nothing is returned.
        """
        if path==None:
            return _f('warn', 'no data set')
        else:
            self.path=path
            self.save=save
    def r(self, c: str = None):
        """
        The function calculates the number of unique words and the total number of characters in a given
        string.
        
        :param c: The parameter "c" is a string that represents a sentence or a piece of text
        :return: a tuple containing two values: the number of unique words in the input string `c` and
        the total number of characters in the input string `c`.
        """
        wc, fs = len(set(c.split())), len(c)
        return wc, fs
    def p(self, n: list = None, w: list = None, s: list = None):
        """
        The function `p` plots two bar charts, one for vocabulary size in thousands and another for file
        size in GB, using the given data.
        
        :param n: The parameter `n` represents the x-axis values for the bar plots. It could be a list
        or an array of values that correspond to different categories or labels
        :param w: The parameter `w` represents a list of vocabulary sizes in bytes
        :param s: The parameter `s` represents the file size in bytes
        """
        plt.figure(figsize=(12, 8))
        plt.subplot(2, 1, 1)
        plt.bar(n, [_/1000 for _ in w], color='skyblue')
        plt.ylabel('Vocab Size in thousands')
        plt.title('Vocab Size (K)')
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.subplot(2, 1, 2)
        plt.bar(n, [_/(1024**3) for _ in s], color='lightgreen')
        plt.ylabel('File Size in GB')
        plt.title('File Size (GB)')
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
    def g(self, fp: str = None):
        """
        The function checks if a file exists, reads its content, and returns information about the file.
        
        :param fp: The parameter `fp` stands for "file path". It is a string that represents the path to
        a file
        :return: a list containing a tuple. The tuple contains three elements: the basename of the file
        (obtained using `os.path.basename(fp)`), the word count (`wc`), and the file size (`fs`).
        """
        if os.path.exists(fp):
            with open(fp, 'r') as f:
                content = f.read()
                wc, fs = self.r(content)
                return [(os.path.basename(fp), wc, fs)]
        else:
            return _f('fatal', f"File '{fp}' not found.")
    def generate(self, show: bool = False):
        """
        The function generates a plot based on data from a file and either saves it or displays it
        depending on the value of the "show" parameter.
        
        :param show: The "show" parameter is a boolean value that determines whether or not to display
        the generated plot. If "show" is set to True, the plot will be displayed using the plt.show()
        function. If "show" is set to False, the plot will not be displayed
        """
        fd = self.g(self.path)
        n = [f[0] for f in fd]
        w = [f[1] for f in fd]
        s = [f[2] for f in fd]
        self.p(n, w, s)
        plt.savefig(self.save) if self.save else None
        plt.show() if show else None
    def destroy(self, confirm: str = None):
        """
        The `destroy` function deletes a file if the confirmation matches the file name.
        
        :param confirm: The `confirm` parameter is used to confirm the destruction of a file. It is
        compared with the last part of the `self.save` attribute (which is assumed to be a file path) to
        ensure that the user has entered the correct file name for confirmation. If the `confirm`
        parameter matches
        """
        if confirm==self.save.split('/')[-1]:
            os.remove(self.save), _f('warn', f'{confirm} destroyed from {self.save}') 
        else:
            _f('fatal','you did not confirm - `SP.destroy(confirm="file_name")`')
