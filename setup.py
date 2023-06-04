from setuptools import setup

with open('./requirements.txt',mode='r') as file:
    requirements = file.read().split('\n')
    print(requirements)

setup(
    name='medium-scrape-pkg',
    version='1.0',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'medium-scraper = medium_scraper:main',
        ]
    }
)