""" Main program file for the scraper. """
from .helper_functions import get_handler
import sys
import json

def run():
    args = sys.argv
    if len(args) < 4:
        raise Exception("Missing arguments! 'scrape-fighters type url output'")

    sc_type = args[1]
    sc_url = args[2]
    sc_output = args[3]

    handler = get_handler(sc_type)
    data = handler(sc_url)

    with open(sc_output, "w", encoding="utf-8") as f:
        json_dump = json.dumps(data)
        f.write(json_dump)