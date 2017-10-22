from classes import Ranking, parseDecklist
from os import listdir, remove
from os.path import isfile, join
from tqdm import tqdm
from scraper import load_page, parse_deck_page
from optparse import OptionParser


def compute(collective, rankings, deck_size=60):
    if len(collective) < deck_size:
        print "There are not enough cards to make a legal deck. ({} cards passed in, need to end up with {})".format(len(collective), deck_size)
    print "Removing {} cards from pool...".format(len(collective) - deck_size)
    for _ in tqdm(range(len(collective) - deck_size)):
        for cards, rank in rankings.getNext():
            if not all(x in collective for x in cards):
                del rankings.rankings[cards]
                continue
            for card in cards:
                card.updateRank(rank * (1. / (2 ** len(cards))))
        collective = sorted(
            collective, key=lambda x: (
                x.uprank, 100 - x.position))
        collective = collective[1:]
        [x.resetRank() for x in collective]
    names = set(x.name for x in collective)
    namelist = [x.name for x in collective]
    finallist = sorted([(x, namelist.count(x)) for x in names])
    return finallist


def run(n=2, mypath=None, onlyfiles=None):
    if mypath:
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        onlyfiles = ["{}/{}".format(mypath, x) for x in onlyfiles]
    decklists = [parseDecklist(x) for x in onlyfiles]

    ranks = Ranking()
    print "Adding {} decklists...".format(len(decklists))
    for deck in tqdm(decklists):
        ranks.addDeck(deck, n)
    print "Adding sideboards..."
    sbranks = Ranking()
    sideboards = [parseDecklist(x, sideboard=True) for x in onlyfiles]
    for sideboard in tqdm(sideboards):
        sbranks.addDeck(sideboard, n)
    print "Computing final decklist..."
    mainDeck = compute(ranks.getCollective(), ranks, 60)
    print "Computing final sideboard..."
    sideBoard = compute(sbranks.getCollective(), sbranks, 15)
    print "Maindeck:"
    for name, quantity in mainDeck:
        print "\t{} {}".format(quantity, name)
    print "Sideboard:"
    for name, quantity in sideBoard:
        print "\t{} {}".format(quantity, name)


if __name__ == "__main__":
    option_parser = OptionParser()
    option_parser.add_option(
        "-n",
        "--number",
        dest="n",
        default=2,
        action="store",
        type="int",
        help="How many combinations of cards to look at. The higher the number, the longer the program will take to run. Default is 2.")
    option_parser.add_option(
        "-u",
        "--url",
        dest="url",
        action="store",
        type="string",
        help="mtgtop8 url to the archetype that you want to determine the best list for. Either this or -f must be specified. Example: 'http://mtgtop8.com/archetype?a=189&meta=51&f=MO'")
    option_parser.add_option(
        "-f",
        "--folder",
        dest="folder",
        action="store",
        type="string",
        help="Path to folder containing decklists. Either this or -u must be specified.")

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
