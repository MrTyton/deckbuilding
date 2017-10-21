from itertools import combinations
from os import listdir
from os.path import isfile, join
from tqdm import tqdm

all_cards = {}

class Card():
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.uprank = 0.
        
    def updateRank(self, num):
        self.uprank += num
        
    def resetRank(self):
        self.uprank = 0
        
    def __gt__(self, other):
        if self.name > other.name: return True
        if self.name == other.name and self.position < other.position: return True
        return False
    
    def __eq__(self, other):
        if self.name == other.name and self.position == other.position: return True
        return False
    
    def __ge__(self, other):
        return self > other or self == other
    
    def __ne__(self, other):
        return not self == other
    
    def __lt__(self, other):
        return not self > other and not self == other
    
    def __le__(self, other):
        return self < other or self == other
    
    def __hash__(self):
        return hash(tuple([self.name, self.position]))
    
    def __repr__(self):
        return "(%s, %d) : %f" % (self.name, self.position, self.uprank)
      
class Ranking():
    def __init__(self):
        self.rankings = {}
        
    def update(self, cards):
        cards = tuple(sorted(cards))
        if cards in self.rankings:
            self.rankings[cards] += 1
        else:
            self.rankings[cards] = 1
            
    def getNext(self):
        for cur in self.rankings.keys():
            yield cur, self.rankings[cur]
            
    def addDeck(self, decklist, n): #decklist is a list of Cards
        for i in range(1, n+1):
            for cur in combinations(decklist, i):
                self.update(sorted(cur))
    
    def getCollective(self):
        return set([x for y in self.rankings.keys() for x in y])            
    

def parseDecklist(file):
    with open(file, "r") as fp:
        lines = fp.readlines()
    decklist = []
    for line in lines:
        if line == "\n": break
        line = line.strip()
        num = int(line[:line.index(" ")])
        name = line[line.index(" ")+1:]
        for i in range(1, num+1):
            insert = Card(name, i)
            if insert not in all_cards:
                all_cards[insert] = insert
            decklist.append(all_cards[insert])
    return decklist
       
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
    

def run(mypath,n):
    onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
    onlyfiles = ["%s%s" % (mypath, x) for x in onlyfiles]
    decklists = [parseDecklist(x) for x in onlyfiles]
    ranks = Ranking()
    for i, x in enumerate(decklists):
        print "Adding decklist number %d" % i+1
        ranks.addDeck(x, n)
    print "Computing final decklist"
    results = compute(ranks.getCollective(), ranks)
    for name, quantity in results:
        print "{} {}".format(quantity, name)