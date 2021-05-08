import sys
import time
from collections import deque 

potionsleft = 6
turns = 0

class Potion:
    def __init__(self, pid, d, p):
        self.pid = pid
        self.d = d
        self.p = p
        self.basics = None
        self.needs = None
        self.score = None
        self.dur = None

class Spell:
    def __init__(self, sid, d, ti, tc, c, r):
        self.sid = sid
        self.d = d
        self.ti = ti
        self.tc = tc
        self.c = c
        self.r = r

class State: 
    def __init__(self,delta): 
        self.delta = delta
        self.path = []
  
class queueNode: 
    def __init__(self,st,dur): 
        self.st = st
        self.dur = dur

def FinalState(potions,state):
    for potion in potions:
        checkpo = 1
        for i in range(4):
            if -potion.d[i] > state[i]:
                checkpo = 0
                break
        if checkpo:
            return 1,potion
    return 0,potions[0]

def ValidSpell(spell,myinv,cost):
    if ConsumerSpell(spell) == 0 and sum(myinv) + sum(spell.d) <= 10:
        return 1
    elif ConsumerSpell(spell) and sum(myinv) + sum(spell.d) <= 10:
        for i in range(4):
            if myinv[i] + spell.d[i] < 0:
                return 0
        return 1
    else:
        return 0

def BFS(potions,myinv,myspells):
    q = deque()
    state = State(myinv)
    q.append(state)
    #while (time.process_time()-start)*10**3 < 40: 
    while q:
        curr = q.popleft()
        fst,potion = FinalState(potions,curr.delta)
        if fst:
            return curr
            #solutions.add((curr.stid,curr))
        checksp = 1
        for spell in myspells:
            if spell.c and ValidSpell(spell,curr.delta,-sum(potion.d)) and (spell.r or spell.sid not in curr.path): 
                curr.path += [spell.sid]
                end = (time.process_time()-start)*10**3
                print(curr.delta,curr.path,f'{end:.3f}',file=sys.stderr)
                nextdelta = [0]*4
                for i in range(4):
                    nextdelta[i] = curr.delta[i]+spell.d[i]
                nextstate = State(nextdelta) 
                nextstate.path = curr.path
                q.append(nextstate) 
                checksp = 0
        #if checksp:
        
    return -1 

def SortByPrice(potion):
    return potion.p

def SortByDuration(potion):
    return potion.dur

def SortByScore(potion):
    return potion.score

def ConsumerSpell(spell):
    for i in range(4):
        if spell.d[i] < 0:
            return 1
    return 0

def LastDelivery(potions,myscore,opscore):
    potions.sort(key=SortByDuration)
    for i in range(len(potions)):
        if potions[i].p + myscore > opscore:
            potions[0] , potions[i] = potions[i] , potions[0]
            break

def ForbiddenPotion(potion,myinv):
    if sum(potion.needs) > 10 - sum(myinv):
        return 1
    else:
        return 0

def EvalNextState(spell,myinv,potion):
    state = spell.d + myinv
    need = []
    for i in range(3,-1,-1):
        need += [max(0,-potion.d[i]-state[i])]
    return sum(potion.needs) - sum(need)

def EnoughSpells(myspells):
    test = [0]*4
    for spell in myspells:
        for i in range(4):
            if spell.d[i] < 0:
                test[i] = 1
    res = 1
    for i in range(4):
        res *= test[i]
    return res


for _ in iter(int, 1):

    start = time.process_time()
    potions = []
    myspells = []
    opspells = []
    tomespells = []

    action_count = int(input())
    for i in range(action_count):
        action_id, action_type, delta_0, delta_1, delta_2, delta_3, price, tome_index, tax_count, castable, repeatable = input().split()
        action_id = int(action_id)
        delta_0 = int(delta_0)
        delta_1 = int(delta_1)
        delta_2 = int(delta_2)
        delta_3 = int(delta_3)
        delta = [delta_0, delta_1, delta_2, delta_3]
        price = int(price)
        tome_index = int(tome_index)
        tax_count = int(tax_count)
        castable = castable != "0"
        repeatable = repeatable != "0"
        ordercost = delta_0 + delta_1 + delta_2 + delta_3
        
        if action_type=="BREW":
            potion = Potion(action_id,delta,price)
            potions += [potion]
        else:
            s = Spell(action_id,delta,tome_index, tax_count, castable, repeatable)
            if action_type=="CAST" or (action_type=="LEARN" and castable):
                myspells += [s]
            elif action_type=="OPPONENT_CAST":
                opspells = [s]
            else:
                tomespells += [s]

    inv_0, inv_1, inv_2, inv_3, myscore = [int(j) for j in input().split()]
    myinv = [inv_0,inv_1,inv_2,inv_3]

    inv_0, inv_1, inv_2, inv_3, opscore = [int(j) for j in input().split()]
    opinv = [inv_0,inv_1,inv_2,inv_3]

    nspells = len(myspells)
    avscore = 0
    turns += 1

    for potion in potions:
        count = 0
        potion.needs = [0]*4
        potion.basics = [0]*4
        for i in range(3,-1,-1):
            count += - potion.d[i] - myinv[i]
            potion.basics[i] = max(0,count)
            count = potion.basics[i]
            potion.needs[i] = max(0,-potion.d[i]-myinv[i])
        potion.basics[0] //= 2
        potion.basics[0] += 1
        potion.dur = sum(potion.basics) + max(potion.basics) - 1
        if potion.dur:
            potion.score = potion.p / potion.dur
        else:
            potion.score = potion.p * 1.15
        avscore += potion.score
    
    avscore /= 5
    potions.sort(key=SortByPrice,reverse=True)

    #if potionsleft < 2:
    #    LastDelivery(potions,myscore,opscore)
    
    checkbrew = 1
    for potion in potions:
        #print(potion.d,file=sys.stderr)
        check = 1
        for i in range(4):
            if potion.d[i]+myinv[i]<0:
                check = 0
        if check:
            end = (time.process_time()-start)*10**3
            print("BREW",potion.pid,f'{end:.3f}')
            potionsleft -= 1
            checkbrew = 0
            break

    checklearn = 1
    for spell in tomespells:
        if checkbrew and spell.tc == 0 and EnoughSpells(myspells)==0:
            print("LEARN",spell.sid)
            checklearn = 0
            break

    checkbfs = 1
    result = BFS(potions,myinv,myspells)
    if checkbrew and checklearn and result != -1 and result.path:
        for spell in myspells:
            if spell.c and spell.sid in result.path and ValidSpell(spell,myinv,0):
                end = (time.process_time()-start)*10**3
                print("CAST",spell.sid,"sa",f'{end:.3f}')
                checkbfs = 0
                break
    
    checkspell = 1
    if checkbrew and checklearn and checkbfs:
        for i in range(len(myspells)):
            if myspells[i].c and ValidSpell(myspells[i],myinv,-sum(potions[0].d)):# and (potions[0].basics[i]):
                end = (time.process_time()-start)*10**3
                print("CAST",myspells[i].sid,f'{end:.3f}')
                #potions[0].basics[i] -= 1
                checkspell = 0
                break
                
    if checkbrew and checkspell and checklearn and checkbfs:
        end = (time.process_time()-start)*10**3
        print("REST",f'{end:.3f}')