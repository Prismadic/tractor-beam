import os
import unittest
from tractor_beam.utils.config import Config

class TestConfig(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestConfig, cls).setUpClass()
        # Determine the directory where this test script is located
        cls.script_dir = os.path.dirname(os.path.abspath(__file__))
        # Now, you can use `cls.script_dir` to construct paths to your config files

    def test_load_conf_from_file_valid(self):
        valid_config_path = os.path.join(self.script_dir, 'valid_config.json')
        config = Config(valid_config_path)
        self.assertIsNotNone(config.conf)
        # Add assertions specific to your valid configuration

    def test_load_conf_from_file_invalid(self):
        invalid_config_path = os.path.join(self.script_dir, 'invalid_config.json')
        config = Config(invalid_config_path)
        self.assertIsNone(config.conf)
        # Further assertions for the invalid case

    # Define other tests here, using `self.script_dir` to reference any files relative to the script

if __name__ == '__main__':
    unittest.main()
