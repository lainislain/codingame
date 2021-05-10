import sys
import math

class Cell:
    def __init__(self, richness, neighbors):
        self.richness = richness
        self.neighbors = neighbors

class Tree():
    growcost = -1
    seedtargets = -1
    def __init__(self, index, size, dormant, bonus):
        self.index = index
        self.size = size
        self.dormant = dormant
        self.bonus = bonus

class Game:
    def __init__(self):
        self.day = 0
        self.nutrients = 0
        self.sundirection = 0
        self.my_sun = 0
        self.my_score = 0
        self.opponents_sun = 0
        self.opponent_score = 0
        self.opponent_is_waiting = 0
        self.cells = []
        self.mytrees = []
        self.optrees = []
        self.alltreesindex = []

def CountTrees(s,trees):
    i = 0
    for tree in trees:
        if tree.size == s:
            i += 1
    return i

def SortBySize(tree):
    return tree.size

def FindBestSeedByRichness(i,mytrees):
    m = -1
    res = -1
    for j in mytrees[i].seedtargets:
        if game.cells[j].richness > m:
            m = game.cells[j].richness
            res = j
    return res

def AddSeedTargets(i,mytrees,trees):
    targets = set()
    targets.add(mytrees[i].index)  
    for a in range(mytrees[i].size):
        newtargets = set()
        for j in targets:
            for k in game.cells[j].neighbors:
                if k >= 0:
                    newtargets.add(k)
        targets.update(newtargets)
    targets.remove(mytrees[i].index)
    toremove = []
    for target in targets:
        if game.cells[target].richness == 0 or target in trees:
            toremove += [target]
    for j in toremove:
        targets.remove(j)
    return targets

def FindBestSeed(mytrees):
    pass


game = Game()
previousday = 0
number_of_cells = int(input())
for i in range(number_of_cells):
    index, richness, neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5 = [int(j) for j in input().split()]
    neigh = [neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5]
    game.cells += [Cell(richness,neigh)]
    #print(index, richness, file=sys.stderr, flush=True)

while True:
    day = int(input()) 
    game.day = day
    if day > previousday:
        game.sundirection += 1
        game.sundirection %= 6
    previousday = day
    nutrients = int(input()) 
    game.nutrients = nutrients
    check = 1
    sun, score = [int(i) for i in input().split()]
    game.my_sun = sun
    game.my_score = score
    inputs = input().split()
    opp_sun = int(inputs[0])
    opp_score = int(inputs[1])
    opp_is_waiting = inputs[2] != "0"  
    game.opponent_sun = opp_sun
    game.opponent_score = opp_score
    game.opponent_is_waiting = opp_is_waiting
    game.mytrees.clear()
    game.optrees.clear()
    game.alltreesindex.clear()
    #print(game.day, game.sundirection,file=sys.stderr, flush=True)
    number_of_trees = int(input()) 
    for i in range(number_of_trees):
        inputs = input().split()
        cell_index = int(inputs[0])  
        size = int(inputs[1]) 
        is_mine = inputs[2] != "0"
        is_dormant = inputs[3] != "0"
        game.alltreesindex += [cell_index]
        if is_mine:
            game.mytrees += [Tree(cell_index,size,is_dormant,2**(game.cells[cell_index].richness - 1))]
        else:
            game.optrees += [Tree(cell_index,size,is_dormant,2**(game.cells[cell_index].richness - 1))]
    number_of_possible_moves = int(input())
    for i in range(number_of_possible_moves):
        possible_move = input()
    game.mytrees.sort(key=SortBySize,reverse=True)
    nseeds = CountTrees(0, game.mytrees)
    for i in range(len(game.mytrees)):
        m = CountTrees(3, game.mytrees)
        n = CountTrees(game.mytrees[i].size + 1, game.mytrees)
        game.mytrees[i].growcost = n + 2**(game.mytrees[i].size + 1) - 1
        game.mytrees[i].seedtargets = AddSeedTargets(i,game.mytrees,game.alltreesindex)
        seed = FindBestSeedByRichness(i, game.mytrees)
        #print(MyTrees[i].index, MyTrees[i].seedtargets, file=sys.stderr, flush=True)
        if check and not game.mytrees[i].dormant:
            if game.mytrees[i].size > 0 and sun >= nseeds and seed >= 0 and nseeds < 1 and game.day < 24 - m - 1:
                print("SEED", game.mytrees[i].index, seed)
                check = 0
            elif game.mytrees[i].size != 3 and sun >= game.mytrees[i].growcost and game.day < 24 - m -1 :
                print("GROW", game.mytrees[i].index)
                check = 0
            elif game.mytrees[i].size == 3 and sun >= 4 and game.day >= 24 - m - 1:
                print("COMPLETE", game.mytrees[i].index)
                check = 0
    if check:
        print("WAIT")
