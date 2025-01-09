""" Helper functions for the scraper """
from requests import get
from parsel import Selector
import re

# Returns the appropriate function for the handler assignment.
def get_handler(choice):
    if choice == "ops":
        return get_opponents
    if choice == "info":
        return get_info
    if choice == "ops+info":
        return get_ops_with_info

def get_opponents(url):
    response = get(url) # getting the HTML file
    selector = Selector(response.text) # passing the HTML file

    # addressing the rows of the opponent table via xpath
    table = selector.xpath('//table[@class="wikitable"]')[0]
    table_rows = table.xpath('./tbody/tr')

    opponents = []
    for row in table_rows[1:]:
        # obtain certain values
        outcome = row.xpath("./td[1]/text()").get()
        record = row.xpath("./td[2]/text()").get()
        method = row.xpath("./td[4]/text()").get()
        date = row.xpath("./td[6]/span/text()").get()
        if date is None:
            date = opponents[len(opponents) - 1]["date"]

        # obtaining the name, just a tad bit trickier than other fields
        a = row.xpath("./td[3]/a")
        href = a[0].xpath("@href").get() if a else None
        name = a[0].xpath("./text()").get() if a else row.xpath("./td["
               "3]/text()").get()

        # collect data together
        opponent = {
            "name": name.strip('\n'),
            "url": None if not href else "https://en.wikipedia.org" + str(
                href),
            "outcome": outcome.strip("\n"),
            "method": method.strip('\n'),
            "date": date,
            "record": record.replace("\u2013", "-").strip("\n"),
        }
        opponents.append(opponent)

    return opponents

def get_info(url):
    response = get(url)
    selector = Selector(response.text)

    # getting the info table's rows
    table = selector.xpath('//table[@class="infobox vcard"]/tbody')[0]
    table_rows = table.xpath("./tr")

    # obtaining certain values
    name = table.xpath('./tr[1]/th/span/text()').get()
    image = table.xpath('./tr[2]/td/span/a/@href').get()

    info = {
        "name": name,
        "image": "https://en.wikipedia.org" + str(image)
    }

    for row in table_rows[2:]:
        key : str = row.xpath("./th/text()").get()
        value = row.xpath("./td/text()").get()

        if key is None or value is None:
            continue # so that this loop does never crash

        if key.startswith("Nickname"):
            info["nickname"] = value
        elif key.startswith("Nationality"):
            info["nationality"] = value
        elif key.startswith("Height"):
            pattern = "(?P<imperial>\d+.ft.\d+.in).\((?P<metric>[\d.]+.c?m)\)"
            match = re.search(pattern, value.replace("\u00a0", " "))
            if match is None:
                info["height"] = None
                continue
            info["height"] = {
                "metric": match.group("metric"),
                "imperial": match.group("imperial")
            }
        elif key.startswith("Weight"):
            pattern = ("(?P<imperial>\d+.lb).\((?P<metric>\d+.kg);.(?P<eng>["
                       "\d.]+.st.(?:\d+.lb)?)")
            match = re.search(pattern, value.replace("\u00a0", " "))
            if match is None:
                info["weight"] = None
                continue
            info["weight"] = {
                "metric": match.group("metric"),
                "imperial": match.group("imperial"),
                "eng": match.group("eng")
            }
        elif key.startswith("Reach"):
            pattern = "(?P<imperial>\d+.in).\((?P<metric>\d+.c?m)\)"
            match = re.search(pattern, value.replace("\u00a0", " "))
            if match is None:
                info["reach"] = None
                continue
            info["reach"] = {
                "metric": match.group("metric"),
                "imperial": match.group("imperial")
            }
    return info

def get_ops_with_info(url):
    ops = get_opponents(url)
    for op in ops:
        if link := op.get("url"):
            info = get_info(link)
        op["info"] = info
    return ops