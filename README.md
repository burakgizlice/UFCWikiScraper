# UFCWikiScraper

#### run "pip install -e ." to install the package.

### For CLI:
#### use "scrape wiki_fighters \<type> \<url> \<output_file>"
#### -> "ops" to retrieve opponents, "info" to retrieve info
#### -> "ops+info" to retrieve opponents with their info
#### -> "deep-ops" to retrieve opponents of the opponents (bigger list)
e.g "scrape wiki_fighters ops https://en.wikipedia.org/wiki/Khabib_Nurmagomedov khabib_ops.json"

### For Web Interface:
#### use "flask --app api run"
paste your url to the input field and chose any option to run the api.
