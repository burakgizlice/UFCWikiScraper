""" Main program file for the scraper. """
from .helper_functions import get_handler
import sys
import json

def run(args):
    if len(args) < 2:
        raise Exception("Missing arguments! 'wiki_fighters type url output'")

    sc_type = args[0]
    sc_url = args[1]
    sc_output = args[2] if len(args) >= 3 else None

    handler = get_handler(sc_type)
    data = handler(sc_url)

    if sc_output is None:
        return data
    else:
        with open(sc_output, "w", encoding="utf-8") as f:
            json_dump = json.dumps(data)
            f.write(json_dump)
