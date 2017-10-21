from bs4 import BeautifulSoup as BS
from requests import get
from tempfile import NamedTemporaryFile
from tqdm import tqdm

"""
This module scrapes the first page of the linked mtgtop8 page and pulls all of the decklists into temporary files.
Does not yet scrape the second+ pages due to javascript shenanigans.
"""

def load_page(url):
    print "Loading page..."
    resp = get(url)
    if resp.status_code != 200:
        print "Error connecting to website."
        return
    bs = BS(resp.text, "html.parser")
    tables = bs.find_all("table")
    decklist_tables = tables[4] #this should be it always, unless it changes the format of the site
    decks = decklist_tables.find_all("tr", class_="hover_tr")
    urls = ["http://mtgtop8.com/{}".format(x.find("a")['href']) for x in decks]
    print "{} decks to download and process...".format(len(urls))
    decklists = []
    for cur in tqdm(urls):
        decklists.append(parse_deck_page(cur))
    return decklists
    
    
def parse_deck_page(url):
    resp = get(url)
    if resp.status_code != 200:
        print "Error connecting to website."
        return
    bs = BS(resp.text, "html.parser")
    try:
        link = "http://mtgtop8.com/{}".format(bs.find("a", text="MTGO")['href'].encode("utf-8"))
    except:
        print url
    resp = get(link)
    if resp.status_code != 200:
        print "Error connecting to website."
        return
    with NamedTemporaryFile(delete=False) as fp:
        fp.write(resp.text)
        name = fp.name
    return name
    
    
    
    
    