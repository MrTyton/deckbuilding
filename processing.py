from classes import Ranking, parseDecklist
from os import listdir, remove
from os.path import isfile, join
from tqdm import tqdm
from scraper import load_page, parse_deck_page
from optparse import OptionParser

       
def compute(collective, rankings):
    print "Removing {} cards from pool...".format(len(collective) - 60)
    for _ in tqdm(range(len(collective) - 60)):
        for cards, rank in rankings.getNext():
            if not all(x in collective for x in cards):
                del rankings.rankings[cards]
                continue
            for card in cards:
                card.updateRank(rank * (1. / (2 ** len(cards))))
        collective = sorted(collective, key=lambda x: (x.uprank, 100-x.position))
        collective = collective[1:]
        [x.resetRank() for x in collective]
    names = set(x.name for x in collective)
    namelist = [x.name for x in collective]
    finallist = sorted([(x, namelist.count(x)) for x in names])
    return finallist
    

def run(n=2, mypath=None, onlyfiles=None):
    if mypath:
        onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
        onlyfiles = ["{}/{}".format(mypath, x) for x in onlyfiles]
    decklists = [parseDecklist(x) for x in onlyfiles]
    
    ranks = Ranking()
    for i, x in enumerate(decklists):
        print "Adding decklist number %d" % (i+1)
        ranks.addDeck(x, n)
    print "Computing final decklist"
    results = compute(ranks.getCollective(), ranks)
    for name, quantity in results:
        print "{} {}".format(quantity, name)
        
if __name__ == "__main__":
    option_parser = OptionParser()
    option_parser.add_option("-n", "--number", dest="n", default=2, action="store", type="int", help="How many combinations of cards to look at. The higher the number, the longer the program will take to run. Default is 2.")
    option_parser.add_option("-u", "--url", dest="url", action="store", type="string", help="mtgtop8 url to the archetype that you want to determine the best list for. Either this or -f must be specified. Example: 'http://mtgtop8.com/archetype?a=189&meta=51&f=MO'")
    option_parser.add_option("-f", "--folder", dest="folder", action="store", type="string", help="Path to folder containing decklists. Either this or -u must be specified.")
    
    options, args = option_parser.parse_args()
    if not options.url and not options.folder:
        print "Need an input. Use -h for more information."
        exit()
    elif options.url and options.folder:
        print "Choose one of the input types."
        exit()
    if options.url:
        options.url = load_page(options.url)
    run(options.n, options.folder, options.url)
    if options.url:
        for cur in options.url:
            remove(cur)
        
        
        