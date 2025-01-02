""" Helper functions for the scraper """
from requests import get
from parsel import Selector

# Returns the appropriate function for the handler assignment.
def get_handler(choice):
    if choice == "ops":
        return get_opponents
    if choice == "info":
        return get_info

def get_opponents(url):
    response = get(url) # getting the HTML file
    selector = Selector(response.text) # passing the HTML file

    # addressing the rows of the table via xpath
    table_rows = selector.xpath('//table[@class="wikitable"]/tbody/tr')

    opponents = []
    for row in table_rows[1:]:
        # obtain certain values
        outcome = row.xpath("./td[1]/text()").get()
        record = row.xpath("./td[2]/text()").get()
        method = row.xpath("./td[4]/text()").get()
        date = row.xpath("./td[6]/span/text()").get()

        # obtaining the name, just a tad bit trickier than other fields
        a = row.xpath("./td[3]/a")
        href = a[0].xpath("@href").get() if a else None
        name = a[0].xpath("./text()").get() if a else row.xpath("./td["
               "3]/text()").get()

        # collect data together
        opponent = {
            "name": name.strip('\n'),
            "url": "https://en.wikipedia.org" + str(href),
            "outcome": outcome.strip("\n"),
            "method": method.strip('\n'),
            "date": date,
            "record": record.replace("\u2013", "-").strip("\n"),
        }
        opponents.append(opponent)

    return opponents

def get_info(url):
    print("GETTING INFORMATION...")
    return {}
