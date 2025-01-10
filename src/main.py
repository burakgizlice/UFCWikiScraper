import importlib
import sys

def default():
    module = sys.argv[1]
    try:
        scraper = importlib.import_module(f"{module}.scraper")
        entry_point = getattr(scraper, "run")
        entry_point(sys.argv[2:])
    except ModuleNotFoundError:
        print(f"{module} is not found!")