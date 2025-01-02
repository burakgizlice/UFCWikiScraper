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

        # obtaining the name, just a tad bit trickier than other fields
        a = row.xpath("./td[3]/a")
        href = a[0].xpath("@href").get() if a else None
        name = a[0].xpath("./text()").get() if a else row.xpath("./td["
               "3]/text()").get()
        print(name)

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

    for row in table_rows[2:12]:
        th = row.xpath("./th/text()").get().lower()
        td = row.xpath("./td//text()").getall()
        info[th] = ''.join(td).strip().replace('\u00a0', ' ').replace(
            '\u2013', '-')

    # collecting the data together
    return info
