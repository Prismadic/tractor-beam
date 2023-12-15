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
        , "hygiene-dm"
        , "matplotlib"
    ],
    package_dir = {
        "config": "tractor_beam"
        , "copier": "tractor_beam"
        , "fax": "tractor_beam"
        , "janitor": "tractor_beam"
        , "receipts": "tractor_beam"
        , "supplies": "tractor_beam"
        , "teacher": "tractor_beam"
        , "utils": "tractor_beam"
    },
    url = 'https://github.com/DylanAlloy/tractor-beam'
)