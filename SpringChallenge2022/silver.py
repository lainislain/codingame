#================================== IMPORTS =========================================

import sys
from math import acos , sin, pi

#================================== CLASSES =========================================

class Hero:

    def __init__(self, _id, x, y, shield, isControlled, distFromBase):
        self._id = _id
        self.x = x
        self.y = y
        self.shield = shield
        self.isControlled = isControlled
        self.distFromBase = distFromBase
        self.targetID = -1
        self.action = "WAIT"
        self.speed = 800

    def printData(self):
        print(f"======== HERO {self._id} =======", file=sys.stderr, flush=True)
        print("x:",self.x, " / y:",self.y, file=sys.stderr, flush=True)
        print("shield:",self.shield, " / is controlled:",self.isControlled, file=sys.stderr, flush=True)
        print("is controlled:", self.isControlled, file=sys.stderr, flush=True)
        print("speed:", self.speed, file=sys.stderr, flush=True)
        print("target ID:", self.targetID, file=sys.stderr, flush=True)
        print("dist from base:", self.distFromBase, file=sys.stderr, flush=True)
        print("=> action:", self.action, file=sys.stderr, flush=True)

class Monster:

    def __init__(self, _id, x, y, shield, isControlled, health, vx, vy, nearBase, threatFor, nAttackers, defScore, attackScore):
        self._id = _id
        self.x = x
        self.y = y
        self.shield = shield
        self.isControlled = isControlled
        self.health = health
        self.vx = vx
        self.vy = vy
        self.nearBase = nearBase
        self.threatFor = threatFor
        self.nAttackers = nAttackers
        self.speed = 400
        self.defScore = defScore
        self.attackScore = attackScore

    def printData(self):
        print(f"======== MONSTER {self._id} =======", file=sys.stderr, flush=True)
        print("x:",self.x, " / y:",self.y, file=sys.stderr, flush=True)
        print("shield:",self.shield, " / is controlled:",self.isControlled, file=sys.stderr, flush=True)
        print("vx:",self.vx, " / vy:",self.vy, file=sys.stderr, flush=True)
        print("health:", self.health, file=sys.stderr, flush=True)
        print("near base:", self.nearBase, file=sys.stderr, flush=True)
        print("nb attackers:", self.nAttackers, file=sys.stderr, flush=True)
        print("speed:", self.speed, file=sys.stderr, flush=True)
        print("defScore:", self.attackScore, file=sys.stderr, flush=True)
        print("attackScore:", self.attackScore, file=sys.stderr, flush=True)

class GameState:
    
    def __init__(self, myhealth, mymana, ophealth, opmana, mybase, hisbase):
        self.myhealth = myhealth
        self.mymana = mymana
        self.ophealth = ophealth
        self.opmana = opmana
        self.mybase = mybase
        self.hisbase = hisbase
        self.monstersInMyBase = []
        self.monstersTargetingMyBase = []
        self.monstersInHisBase = []
        self.monstersTargetingHisBase = []
        self.turn = 0
        self.useShield = False
    
    def printData(self):
        print("======== GAME STATE =======", file=sys.stderr, flush=True)
        print("Actual turn:", self.turn, file=sys.stderr, flush=True)
        print("use shield:", self.useShield, file=sys.stderr, flush=True)
        print("My health:",self.myhealth, " / My mana:",self.mymana, file=sys.stderr, flush=True)
        print("En health:",self.ophealth, " / En mana:",self.opmana, file=sys.stderr, flush=True)
        print("My base:", self.mybase, file=sys.stderr, flush=True)
        print("His base:", self.hisbase, file=sys.stderr, flush=True)
        print("Monsters in my base:", self.monstersInMyBase, file=sys.stderr, flush=True)
        print("Monsters targeting my base:", self.monstersTargetingMyBase, file=sys.stderr, flush=True)
        print("Monsters in his base:", self.monstersInHisBase, file=sys.stderr, flush=True)
        print("Monsters targeting his base:", self.monstersTargetingHisBase, file=sys.stderr, flush=True)

#================================== UNCOMPLETED UTILS =========================================

def heroIsAttackingMonster(hero, monster):
    if distance(hero.x, hero.y, monster.x, monster.y) < 800:
        return True
    return False

def stepsFromCatch(monster, hero, baseX, baseY):
    distMonsterFromBase = distance(monster.x, monster.y, baseX, baseY)
    return calculateSteps(distance(hero.x, hero.y, monster.x, monster.y), hero.speed)

def monsterIsCatchableByHero(monster, hero, baseX, baseY):
    if stepsFromBase(monster, baseX, baseY) < stepsFromCatch(monster, hero, baseX, baseY):
        return False
    return True

def monsterIsKillable(monster):

    if monster.health > stepsFromBase(monster, state.mybase[0], state.mybase[1]) :
        pass

#================================== UNCOMPLETED FUNCTIONS =========================================

def monsterCatchPoint(monster, hero):
    xh = hero.x
    yh = hero.y
    xa = xh - monster.x
    xb = monster.vx
    ya = yh - monster.y
    yb = monster.vy
    denom = (((xa**2 + ya**2)**.5) * ((xb**2 + yb**2)**.5))
    if denom == 0: return (-1, -1)
    coef = (xa * xb + ya * yb) / denom
    if coef > 1 or coef < -1:
        return (-1, -1)
    angle = acos(coef)
    B = 4 * (monster.vx**2 + monster.vy**2) * ((xh - monster.x)**2 + (yh - monster.y)**2) * (sin(angle))**2 / 800**4
    b = B**.5
    delta = B + 4 * (xh - monster.x + yh - monster.y) / 800**2
    if delta >= 0:
        t1 = (b - delta**.5) / (2 * (-1))
        t2 = (b + delta**.5) / (2 * (-1))
        t = min(t1, t2)
    else:
        return (-1, -1)
    HI = 800 * t2
    HI1 = 800 * t1
    xi = HI * monster.vx / 800 + monster.x
    yi = HI * monster.vy / 800 + monster.y
    xi1 = HI1 * monster.vx / 800 + monster.x
    yi1 = HI1 * monster.vy / 800 + monster.y
    return (int(xi1), int(yi1))

#================================== UTILS =========================================

def sortByClosestMyBase(monster):
    return monster[1]

def sortByClosestHisBase(monster):
    return monster[2]

def distance(x1, y1, x2, y2):
    return ((x1-x2)**2+(y1-y2)**2)**.5

def calculateSteps(dist, speed):
    return dist // speed

#================================== FIND CLOSEST =========================================

def findClosestEntity(entities, x, y):
    dist = 42000000
    res = -1
    for key, entity in entities.items():
        temp = distance(entity.x, entity.y, x, y)
        if temp < dist:
            dist = temp
            res = key
    return res , dist

def findClosestWindTarget(target, points):
    dist = 42000000
    res = (-1 , -1)
    for p in points:
        temp = distance(p[0], p[1], target.x, target.y)
        if temp < dist:
            dist = temp
            res = p
    return res , dist

def findClosestHeroToMonster(heroes, monster):
    dist = 42000000
    res = -1
    for key, entity in heroes.items():
        temp = distance(entity.x, entity.y, monster.x, monster.y)
        if temp < dist and key not in busy and (entity.targetID == monster._id or entity.targetID == -1) and (state.turn <= 100 or key != firstHero + 2):
            dist = temp
            res = key
    return res , dist

#================================== LOCAT FROM BASE =========================================

def nearMyBase(x , y):
    if distance(x, y, state.mybase[0], state.mybase[1]) <= 6000:
        return True
    return False

def nearHisBase(x , y):
    if distance(x, y, state.hisbase[0], state.hisbase[1]) <= 6000:
        return True
    return False

def entityIsInBase(entity, baseX, baseY):
    if distance(entity.x, entity.y, baseX, baseY) < 300:
        return True
    return False

def stepsFromBase(entity, baseX, baseY):
    return calculateSteps(distance(entity.x, entity.y, baseX, baseY) - 300, entity.speed)

#================================== MONSTER / BASE =========================================

def monstersInMyBase(monsters):
    res = []
    for monster in monsters.values():
        if monster.nearBase and monster.threatFor == 1:
            res += [monster._id]
    return res

def monstersTargetingMyBase(monsters):
    res = []
    for monster in monsters.values():
        if monster.threatFor == 1:
            res += [monster._id]
    return res

def monstersInHisBase(monsters):
    res = []
    for monster in monsters.values():
        if monster.nearBase and monster.threatFor == 2:
            res += [monster._id]
    return res

def monstersTargetingHisBase(monsters):
    res = []
    for monster in monsters.values():
        if monster.threatFor == 2:
            res += [monster._id]
    return res

#================================== ATTACK FUNCTIONS =========================================

def inAttackZone(x , y):
    if distance(x, y, state.hisbase[0], state.hisbase[1]) > 8000:
        return False
    return True

def attackEnnemyPotential(ennemy):
    if state.mymana >= 70 and ennemy.shiel == 0 and len(state.monstersInHisBase) and nearHisBase(ennemy.x, ennemy.y):
        return True
    return False

def attackBasePotential(monster):
    if state.mymana >= 50 and monster.shield == 0 and monster.health >= 11:# and nearHisBase(monster.x, monster.y) and stepsFromBase(monster, Ex, Ey) // 2:
        return True
    return False

def shieldMonsterPotential(monster):
    if state.mymana >= 50 and monster.threatFor == 2 and monster.shield == 0 and monster.health >= 16 and distance(monster.x, monster.y, state.hisbase[0], state.hisbase[1]) < 4800:
        return True
    return False

def attackBase(monster):
    attackPoint = (14500, 7200)
    if state.mybase[0] != 0: attackPoint = (1500, 5000)
    dist = distance(monster.x , monster.y, heroes[2 + firstHero].x, heroes[2 + firstHero].y)
    if attackBasePotential(monster):
        if dist <= 1280 and nearHisBase(monster.x, monster.y):
            state.mymana -= 10
            return "SPELL WIND " + str(state.hisbase[0]) + " " + str(state.hisbase[1])
        elif dist <= 2200 and monster.threatFor != 2  and monster.health >= 20 :
            state.mymana -= 10
            return "SPELL CONTROL " + str(monster._id) + " " + str(state.hisbase[0]) + " " + str(state.hisbase[1])
    if shieldMonsterPotential(monster) and dist <= 2200:
        state.mymana -= 10
        return "SPELL SHIELD " + str(monster._id)
    if (monster.threatFor != 2 or state.mymana < 10) and inAttackZone(monster.x, monster.y):
        return "MOVE " + str(monster.x) + " " + str(monster.y)
    elif state.turn % 10 > 4:
        return "MOVE " + str(attackPoint[0]) + " " + str(attackPoint[1])
    else:
        return "MOVE " + str(offsets[2][0]) + " " + str(offsets[2][1])
    
def attackEnnemy(ennemy):
    if attackEnnemyPotential(ennemy):
        hero , dist = findClosestEntity(heroes, ennemy.x, ennemy.y)
        if dist <= 1280:
            return "SPELL WIND " + str(state.mybase[0]) + " " + str(state.mybase[1])
        elif dist <= 2200:
            return "SPELL CONTROL " + str(ennemy._id) + " " + str(state.mybase[0]) + " " + str(state.mybase[1])
    return "MOVE " + str(offsets[2][0]) + " " + str(offsets[2][1])

#================================== DEFANCE FUNCTIONS =========================================

def inDefenceZone(x, y):
    if distance(x, y, state.hisbase[0], state.hisbase[1]) > 6000:
        return False
    return True

#================================== ENNEMY FUNCTIONS =========================================

def ennemyDanger(ennemies, hero):
    for key, ennemy in ennemies.items():
        if len(state.monstersInMyBase) and state.opmana >= 10 and 2200 <= distance(hero.x, hero.y, ennemy.x, ennemy.y) <= 2600:
            return True
    return False

def ennemiesNearMonster(ennemies, monster):
    res = 0
    for ennemy in ennemies.values():
        if distance(ennemy.x, ennemy.y, monster.x, monster.y) < 800:
            res += 1
    print(res, monster._id,file=sys.stderr, flush=True)
    return res

#================================== GLOBAL VARIABLES =========================================

Bx, By = [int(i) for i in input().split()]
Ex , Ey = 17630 - Bx, 9000 - By
heroesCount = int(input())
firstHero = 0
heroes = {}
controlled = []
state = GameState(-1, -1, -1, -1, (-1, -1), (-1, -1))
defPoints = [(1500, 6000), (6000, 1500), (9000, 2500)]
attackPoints = [(1500, 6000), (6000, 1500), (9000, 2500)]

#================================== GAME LOOP =========================================

while True:
    
    monsters = {}
    ennemies = {}
    gamedata = []
    monsterIDs = []
    busy = []

    for i in range(2):
        gamedata += [int(j) for j in input().split()]

    if state.turn == 0:
        state = GameState(gamedata[0], gamedata[1], gamedata[2], gamedata[3], (Bx, By), (Ex, Ey))
    else:
        state.myhealth = gamedata[0]
        state.mymana = gamedata[1]
        state.ophealth = gamedata[2]
        state.opmana = gamedata[3]
    
    if state.turn < 50:
        offsets = ((7090, 1250), (5162, 7372), (10000, 5000))
        revOffsets = ((17630 - 7090, 9000 - 1250), (17630 - 5162, 9000 - 7372), (17630 - 10000, 9000 - 5000))
    else:
        offsets = ((6000, 1250), (3200, 4600), (15000, 4500))
        revOffsets = ((17630 - 6000, 9000 - 1250), (17630 - 3200, 9000 - 4600), (5000, 1500))

    if Bx != 0: 
        firstHero = 3
        offsets = revOffsets

    entityCount = int(input())

    for i in range(entityCount):
        _id, _type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for = [int(j) for j in input().split()]
        if _type == 0: 
            d1 = distance(x, y, Bx, By)
            d2 = distance(x, y, Ex, Ey)
            s1 = health / d1
            s2 = health / d2
            monsters[_id] = Monster(_id, x, y, shield_life, is_controlled, health, vx, vy,  near_base, threat_for, 0, s1, s2)
            monsterIDs += [(_id, d1, d2)]

        elif _type == 1: 
            if state.turn == 0:
                heroes[_id] = Hero(_id, x, y, shield_life, is_controlled, distance(x, y, Bx, By))
            else:
                heroes[_id].x = x
                heroes[_id].y = y
                heroes[_id].shield = shield_life
                heroes[_id].isControlled = is_controlled
                heroes[_id].distFromBase = distance(x, y, Bx, By)
        else: 
            ennemies[_id] = Hero(_id, x, y, shield_life, is_controlled, distance(x, y, Bx, By))

    monsterIDs.sort(key=sortByClosestMyBase)
    state.monstersInMyBase = monstersInMyBase(monsters)
    state.monstersInHisBase = monstersInHisBase(monsters)
    state.monstersTargetingMyBase = monstersTargetingMyBase(monsters)
    state.monstersTargetingHisBase = monstersTargetingHisBase(monsters)

    #print("====== SORTED VISIBLE MONSTERS =========", file=sys.stderr, flush=True)
    #print(monsterIDs, file=sys.stderr, flush=True)

    #state.printData()

    for i in range(3):
        if heroes[i + firstHero].isControlled == 1:
            state.useShield = True
        if heroes[i + firstHero].targetID not in monsters:
            heroes[i + firstHero].targetID = -1

    heroes[firstHero].action = "MOVE " + str(offsets[0][0]) + " " + str(offsets[0][1])
    heroes[firstHero + 1].action = "MOVE " + str(offsets[1][0]) + " " + str(offsets[1][1])
    heroes[firstHero + 2].action = "MOVE " + str(offsets[2][0]) + " " + str(offsets[2][1])

    for monster in monsterIDs:

        if (monsters[monster[0]].threatFor == 1 and monsters[monster[0]].nAttackers == 0):
                for i in range(3):
                    heroes[i + firstHero].targetID = -1
  
        x = monsters[monster[0]].x
        y = monsters[monster[0]].y
        closestHero , dist = findClosestHeroToMonster(heroes, monsters[monster[0]])
        
        if closestHero == -1: continue
        
        #inter = monsterCatchPoint(monsters[monster[0]], heroes[closestHero])
        
        if state.mymana >= 10 and monsters[monster[0]].shield == 0 and dist <= 2200:
            W, distW = findClosestWindTarget(monsters[monster[0]], defPoints)
            if monsters[monster[0]].nearBase and monsters[monster[0]].threatFor == 1 and dist <= 1280:# and not monsterIsKillable(monsters[monster[0]]):
                heroes[closestHero].action = "SPELL WIND " + str(W[0]) + " " + str(W[1])
                busy += [closestHero]
                state.mymana -= 10
                continue
            elif state.mymana >= 40 and state.useShield and heroes[closestHero].shield < 2 and ennemyDanger(ennemies, heroes[closestHero]):
                heroes[closestHero].action = "SPELL SHIELD " + str(closestHero)
                busy += [closestHero]
                state.mymana -= 10
                continue
            elif monsters[monster[0]].threatFor == 1 and state.mymana >= 50 and monster[2] > 5000 and monster[1] > 5000 and monsters[monster[0]].health == 23 and monster[0] not in controlled:
                heroes[closestHero].action = "SPELL CONTROL " + str(monster[0]) + " " + str(state.hisbase[0]) + " " + str(state.hisbase[1])
                busy += [closestHero]
                state.mymana -= 10
                controlled += [monster[0]]
                continue
        #if inter[0] == -1:
        if monsters[monster[0]].threatFor != 2:
            heroes[closestHero].action = "MOVE " + str(monsters[monster[0]].x) + " " + str(monsters[monster[0]].y)
        
            # else:
            #     heroes[closestHero].action = "MOVE " + str(inter[0]) + " " + str(inter[1]) + " A" + str(monster[0]) + str(inter)

        for i in range(heroesCount):
            if heroes[i + firstHero].targetID == monster[0]:
                heroes[i + firstHero].targetID = -1
        
        heroes[closestHero].targetID = monster[0]
        monsters[monster[0]].nAttackers += 1
        busy += [closestHero]

    monsterIDs.sort(key=sortByClosestHisBase)

    if state.turn > 100 and len(monsterIDs):
        heroes[firstHero + 2].action = attackBase(monsters[monsterIDs[0][0]])

    for i in range(heroesCount):
        #heroes[i + firstHero].printData()
        print(heroes[i + firstHero].action)

    state.turn += 1