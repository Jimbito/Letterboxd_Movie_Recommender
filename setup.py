from ensurepip import version
from unicodedata import name
from urllib.error import URLError
from setuptools import setup
from setuptools import find_packages

setup(
    name='letterboxd_scraper',
    version='0.0.1',
    description='Mock package that allows you to selectively scrape from the Letterboxd website.',
    URL='https://github.com/Jimbito/Letterboxd_Web_Scraper.git',
    author='James Overend',
    license='MIT',
    packages=find_packages(),
    install_requires=['requests','selenium']
)
