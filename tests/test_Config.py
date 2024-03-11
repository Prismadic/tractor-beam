import os, shutil
import unittest
from tractor_beam.utils.config import Config, Job, Schema, Settings

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

    def test_load_conf_from_file_invalid(self):
        invalid_config_path = os.path.join(self.script_dir, 'invalid_config.json')
        config = Config(invalid_config_path)
        self.assertIsNone(config.conf)

    # Config can be initialized without any arguments
    def test_initialized_without_arguments(self):
        config = Config()
        assert config.conf is None
        
    # Config cannot load a configuration file that does not exist
    def test_cannot_load_nonexistent_file(self):
        config = Config("nonexistent_file.json")
        assert config.conf is None
        

    # handling valid configuration
    def test_handling_valid_configuration(self):
        # Create a valid configuration dictionary
        valid_config = {
            "role": "admin",
            "settings": {
                "name": "test_config",
                "proj_dir": "/path/to/project",
                "jobs": [
                    {
                        "url": "https://example.com",
                        "types": ["type1", "type2"],
                        "beacon": "beacon1",
                        "delay": 1.5,
                        "custom": [
                            {"key1": "value1"},
                            {"key2": "value2"}
                        ]
                    }
                ]
            }
        }
    
        # Create an instance of Config with the valid configuration dictionary
        config = Config(valid_config)
    
        # Assert that the configuration was loaded successfully
        assert config.conf is not None
    
        # Assert that the loaded configuration matches the expected values
        assert config.conf.role == "admin"
        assert config.conf.settings.name == "test_config"
        assert config.conf.settings.proj_dir == "/path/to/project"
    
        # Assert that the loaded job matches the expected values
        job = config.conf.settings.jobs[0]
        assert job.url == "https://example.com"
        assert job.types == ["type1", "type2"]
        assert job.beacon == "beacon1"
        assert job.delay == 1.5
        assert job.custom == [{"key1": "value1"}, {"key2": "value2"}]

    # creating configuration
    def test_creating_configuration(self):
        # Create a valid configuration dictionary
        config_data = {
            "settings": {
                "name": "test_config",
                "proj_dir": "/path/to/project",
                "jobs": [{"url": ""}]
            },
            "role": "some_role"
        }
    
        # Initialize Config with the configuration dictionary
        config = Config(config_data)
    
        # Assert that the configuration is loaded correctly
        assert config.conf.settings.name == "test_config"
        assert config.conf.settings.proj_dir == "/path/to/project"
        assert isinstance(config.conf.settings.jobs, list)
        assert config.conf.role == "some_role"
        for job in config.conf.settings.jobs:
            assert isinstance(job, Job)

            
    # unboxes configuration to project directory
    def test_unbox_configuration(self):
        # Arrange
        conf = {
            "role": "test",
            "settings": {
                "name": "test_config",
                "proj_dir": self.script_dir,
                "jobs": [
                    {
                        "url": "https://example.com",
                        "types": ["type1", "type2"],
                        "beacon": "beacon1",
                        "delay": 1.5,
                        "custom": [
                            {"key1": "value1"},
                            {"key2": "value2"}
                        ]
                    }
                ]
            }
        }
        config = Config(conf)

        # Act
        result = config.unbox(overwrite=True)

        # Assert
        assert result is not None
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], Schema)
        assert isinstance(result[1], str)
        assert result[0].role == "test"
        assert result[0].settings.name == "test_config"
        assert result[0].settings.proj_dir == self.script_dir
        assert len(result[0].settings.jobs) == 1
        assert result[0].settings.jobs[0].url == "https://example.com"
        assert result[0].settings.jobs[0].types == ["type1", "type2"]
        assert result[0].settings.jobs[0].beacon == "beacon1"
        assert result[0].settings.jobs[0].delay == 1.5
        assert result[0].settings.jobs[0].custom == [{"key1": "value1"}, {"key2": "value2"}]
        assert result[1] == os.path.join(self.script_dir, conf["settings"]["name"], "config.json")
        shutil.rmtree(os.path.join(config.conf.settings.proj_dir, config.conf.settings.name))
        
    # creates project directory and saves configuration
    def test_creates_project_directory_and_saves_configuration(self):
        # Arrange
        conf = {
            "role": "test",
            "settings": {
                "name": "test_config",
                "proj_dir": self.script_dir,
                "jobs": [
                    {
                        "url": "https://example.com",
                        "types": ["type1", "type2"],
                        "beacon": "beacon1",
                        "delay": 1.5,
                        "custom": [
                            {"key1": "value1"},
                            {"key2": "value2"}
                        ]
                    }
                ]
            }
        }
        config = Config(conf)

        # Act
        result = config.unbox(overwrite=True)

        # Assert
        assert result is not None
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert result[0] is not None
        assert isinstance(result[0], Schema)
        assert result[1] == os.path.join(self.script_dir, conf["settings"]["name"], "config.json")
        shutil.rmtree(os.path.join(config.conf.settings.proj_dir, config.conf.settings.name))

    # destroys project directory and configuration
    def test_destroys_project_directory_and_configuration(self):
        # Arrange
        conf = {
            "role": "test",
            "settings": {
                "name": "test_config",
                "proj_dir": self.script_dir,
                "jobs": [
                    {
                        "url": "https://example.com",
                        "types": ["type1", "type2"],
                        "beacon": "beacon1",
                        "delay": 1.5,
                        "custom": [
                            {"key1": "value1"},
                            {"key2": "value2"}
                        ]
                    }
                ]
            }
        }
        config = Config(conf)
        config.unbox()
    
        # Act
        config.destroy(confirm="test_config")
    
        # Assert
        assert not os.path.exists(os.path.join(self.script_dir, conf["settings"]["name"]))

    # Returns None if project directory already exists and overwrite is False
    def test_returns_none_if_project_directory_already_exists_and_overwrite_is_false(self):
        # Create a config instance with the project directory and name

        conf = {
            "role": "test",
            "settings": {
                "name": "test_config",
                "proj_dir": self.script_dir,
                "jobs": [
                    {
                        "url": "https://example.com",
                        "types": ["type1", "type2"],
                        "beacon": "beacon1",
                        "delay": 1.5,
                        "custom": [
                            {"key1": "value1"},
                            {"key2": "value2"}
                        ]
                    }
                ]
            }
        }
        config = Config(conf)
        config.unbox()
        # Call the unbox method with overwrite=False
        result = config.unbox(overwrite=False)

        # Assert that the result is None
        assert result is None

        # Clean up the temporary directories
        shutil.rmtree(os.path.join(config.conf.settings.proj_dir, config.conf.settings.name))
        







    # Define other tests here, using `self.script_dir` to reference any files relative to the script

if __name__ == '__main__':
    unittest.main()
