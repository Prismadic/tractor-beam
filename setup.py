from setuptools import setup

setup(
    name='llm_tractor_beam',
    version='0.0.1',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        "chardet"
        , "docx"
        , "beautifulsoup4"
        , "llm-hygiene"
        , "matplotlib"
        , "tqdm"
        , "jsonschema"
    ],
    package_dir = {
    },
    url = 'https://github.com/DylanAlloy/tractor-beam'
)