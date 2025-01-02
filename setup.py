from setuptools import setup

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().split('\n')

setup(
    name='ufc_wiki_scraper',
    version='0.0.1',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'scrape-fighters = ufc_wiki_scraper.scraper:run',
        ]
    }
)