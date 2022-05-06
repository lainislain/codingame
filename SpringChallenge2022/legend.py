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
        self.monstersNearMyBase = []
        self.monstersTargetingMyBase = []
        self.monstersInHisBase = []
        self.monstersNearHisBase = []
        self.monstersTargetingHisBase = []
        self.turn = 0
        self.useShield = False
        self.ennemyNearMyBase = False
        self.ennemiesNearHisBase = []
        self.ennemyAttacker = -1
        self.ennemyDefender = -1
        self.ultimatAttack = False
    
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

def monsterIsKillable(monster, hero, interX, interY, baseX, baseY):
    distMonsterHero = distance(hero.x, hero.y, monster.x, monster.y)
    distHeroBase = distance(hero.x, hero.y, baseX, baseY)
    distMonsterBase = distance(monster.x, monster.y, baseX, baseY)
    stepsMonsterHero = calculateSteps(distMonsterHero, 800)
    
    if distHeroBase < distMonsterBase: stepsMonsterHero *= -1
    if pointOnMap(interX, interY):
        steps = stepsFromBase(interX, interY, baseX, baseY, 400)
    else:
        steps = stepsFromBase(monster.x, monster.y, baseX, baseY, 400)

    # print("distMonsterHero", distMonsterHero,file=sys.stderr, flush=True)
    # print("distMonsterBase", distMonsterBase,file=sys.stderr, flush=True)
    # print("distHeroBase", distHeroBase,file=sys.stderr, flush=True)
    # print("stepsMonsterHero", stepsMonsterHero,file=sys.stderr, flush=True)
    # print("stepsInterBase", steps,file=sys.stderr, flush=True)

    if steps < ( monster.health / 2 ) + stepsMonsterHero :
        #print(hero._id , "can't solo kill", monster._id,file=sys.stderr, flush=True)
        return False , steps

    #print(hero._id , "is solo killing", monster._id, file=sys.stderr, flush=True)
    return True , steps

def monsterIsKillableBy2(monster, hero, interX, interY, steps, baseX, baseY):
    distMonsterHero = distance(hero.x, hero.y, monster.x, monster.y)
    distHeroBase = distance(hero.x, hero.y, baseX, baseY)
    distMonsterBase = distance(monster.x, monster.y, baseX, baseY)
    stepsMonsterHero = calculateSteps(distMonsterHero, 800)

    if distHeroBase < distMonsterBase: stepsMonsterHero *= -1
    if pointOnMap(interX, interY):
        steps2 = stepsFromBase(interX, interY, baseX, baseY, 400) + steps
    else:
        steps2 = stepsFromBase(monster.x, monster.y, baseX, baseY, 400) + steps

    # print("distMonsterHero", distMonsterHero,file=sys.stderr, flush=True)
    # print("distMonsterBase", distMonsterBase,file=sys.stderr, flush=True)
    # print("distHeroBase", distHeroBase,file=sys.stderr, flush=True)
    # print("stepsMonsterHero", stepsMonsterHero,file=sys.stderr, flush=True)
    # print("steps2", steps2,file=sys.stderr, flush=True)
    # print((monster.health / 2),file=sys.stderr, flush=True)

    if steps2  <= (monster.health / 2)  + stepsMonsterHero:
        #print(hero._id , "cannot help killing", monster._id,file=sys.stderr, flush=True)
        return False, steps

    #print(hero._id , "can help killing", monster._id,file=sys.stderr, flush=True)
    return True, steps2

#================================== UNCOMPLETED FUNCTIONS =========================================

# def monsterCatchPoint(monster, hero):
#     xh = hero.x
#     yh = hero.y
#     xa = xh - monster.x
#     xb = monster.vx
#     ya = yh - monster.y
#     yb = monster.vy
#     denom = (((xa**2 + ya**2)**.5) * ((xb**2 + yb**2)**.5))
#     if denom == 0: return (-1, -1)
#     coef = (xa * xb + ya * yb) / denom
#     if coef > 1 or coef < -1:
#         return (-1, -1)
#     angle = acos(coef)
#     B = 4 * (monster.vx**2 + monster.vy**2) * ((xh - monster.x)**2 + (yh - monster.y)**2) * (sin(angle))**2 / 800**4
#     b = B**.5
#     delta = B + 4 * (xh - monster.x + yh - monster.y) / 800**2
#     if delta >= 0:
#         t1 = (b - delta**.5) / (2 * (-1))
#         t2 = (b + delta**.5) / (2 * (-1))
#         t = min(t1, t2)
#     else:
#         return (-1, -1)
#     HI = 800 * t2
#     HI1 = 800 * t1
#     xi = HI * monster.vx / 800 + monster.x
#     yi = HI * monster.vy / 800 + monster.y
#     xi1 = HI1 * monster.vx / 800 + monster.x
#     yi1 = HI1 * monster.vy / 800 + monster.y
#     return (int(xi1), int(yi1))

#================================== UTILS =========================================

def isInCircle(circle_x, circle_y, x, y):
    if ((x - circle_x) * (x - circle_x) +
        (y - circle_y) * (y - circle_y) - 5000 **2 <= 1):
        return True
    else:
        return False

def pointOnMap(x , y):
    if x > 17630 or x < 0 or y < 0 or y > 9000: 
        return False
    return True

def sortByClosestMyBase(monster):
    return monster[1]

def sortByClosestHisBase(monster):
    return monster[2]

def distance(x1, y1, x2, y2):
    return ((x1-x2)**2+(y1-y2)**2)**.5

def calculateSteps(dist, speed):
    return dist // speed

def findIntersection(monster, hero):
    i = 1
    interX = monster.x + vx
    interY = monster.y + vy
    distMonsterInter = distance(monster.x, monster.y, interX, interY)
    distHeroInter = distance(hero.x, hero.y, interX, interY)
    while distMonsterInter < (distHeroInter / 2):
        interX = monster.x + i * monster.vx
        interY = monster.y + i * monster.vy
        if interX < 0 or interX > 17630 or interY < 0 or interY > 90000:
            pass
        distMonsterInter = distance(monster.x, monster.y, interX, interY)
        distHeroInter = distance(hero.x, hero.y, interX, interY)
        i += 1
    return monster.x + (i - 2) * monster.vx , monster.y + (i - 2) * monster.vy

def heroIsAttackingMonster(hero, monster):
    if distance(hero.x, hero.y, monster.x, monster.y) < 800:
        return True
    return False

def attackerInPostion(hero, monster):
    dist = distance(hero.x, hero.y, monsters[monster[0]].x, monsters[monster[0]].y)
    if dist <= 1280:
        return True
    return False

def allAttackersInPostion(monster):
    res = 0
    for i in range(2):
        if not attackerInPostion(heroes[i + firstHero], monster):
            res += 1
            return False
    return True


#================================== FIND CLOSEST =========================================

def findClosestEntity(entities, x, y):
    dist = 42000000
    res = -1
    for key, entity in entities.items():
        temp = distance(entity.x, entity.y, x, y)
        if temp < dist and temp:
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

def findClosestControlTarget(points, heroId):
    if heroId == firstHero + 1:
        return points[0]
    return points[1]

def findClosestHeroToMonster(heroes, monster):
    dist = 42000000
    res = -1
    for key, entity in heroes.items():
        temp = distance(entity.x, entity.y, monster.x, monster.y)
        if temp < dist and key not in busy and (entity.targetID == monster._id or entity.targetID == -1) and not entity.isControlled:
            dist = temp
            res = key
    return res , dist

#================================== LOCAT FROM BASE =========================================

def nearMyBase(x , y):
    if distance(x, y, state.mybase[0], state.mybase[1]) <= 6000:
        return True
    return False

def nearHisBase(x , y):
    if distance(x, y, state.hisbase[0], state.hisbase[1]) <= 5000:
        return True
    return False

def entityIsInBase(entity, baseX, baseY):
    if distance(entity.x, entity.y, baseX, baseY) < 300:
        return True
    return False

def stepsFromBase(x, y, baseX, baseY, speed):
    return calculateSteps(distance(x, y, baseX, baseY) - 300, speed)

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

def inAttackerFarmZone(x , y):
    if 9000 >= distance(x, y, state.hisbase[0], state.hisbase[1]) > 5000:
        return True
    return False

def attackBasePotential(monster):
    if state.mymana >= 50:
        return True
    return False

def shieldMonsterPotential(monster):
    if state.mymana >= 50 and monster.threatFor == 2 and monster.shield == 0 and monster.health >= 16 and distance(monster.x, monster.y, state.hisbase[0], state.hisbase[1]) < 4800:
        return True
    return False

def windMonsterPotential(monster , distMonsterHero):
    distMonsterBase = distance(monster.x, monster.y, state.hisbase[0], state.hisbase[1])
    if distMonsterHero <= 1280 and distMonsterBase <= 2600:
        return True
    return False

def windMonsterPotential2(monster , distMonsterHero):
    if distMonsterHero <= 1280 and nearHisBase(monster.x , monster.y) and not monster.shield and monster.health >= 10:
        return True
    return False

def windEnnemyPotential2(monster, ennemy):
    distMonsterBase = distance(monster.x, monster.y, state.hisbase[0], state.hisbase[1])
    if monster.nearBase and monster.threatFor == 2 and ennemy.shield == 0 and distMonsterBase >  distance(ennemy.x, ennemy.y, state.hisbase[0], state.hisbase[1]):
        return True
    return False

def controlHealthiestMonster(hero):
    res = -1
    current = -1
    for monster in monsters.values():
        dist = distance(monster.x , monster.y, hero.x, hero.y)
        if dist <= 2200 and monster.health >= current and monster._id not in controlled  and not monster.nearBase and monster.threatFor != 2:
            current = monster.health
            res = monster._id
    return res

def monstersNearHero(hero):
    pass

def attackBase(monster):
    attackPoint = (14500, 7800)
    attackPoint2 = (16500, 5500)
    ennemy = None
    if len(state.monstersInHisBase) < 2:
        attackPoint = (11800, 7500)
        attackPoint2 = (16000, 3000)
    if state.mybase[0] != 0: 
        attackPoint = (17630 - attackPoint[0], 9000 - attackPoint[1])
        attackPoint2 = (17630 - attackPoint2[0], 9000 - attackPoint2[1])
    if state.ennemyDefender == -1:
        ennemyShield = 1
        distEnnemyBase = 0
        distMonsterEnnemy = 6000
        distHeroEnnemy = 6000
    else:
        ennemy = ennemies[state.ennemyDefender]
        ennemyShield = ennemy.shield
        distEnnemyBase = distance(ennemy.x, ennemy.y, state.hisbase[0], state.hisbase[1])
        distMonsterEnnemy = distance(ennemy.x, ennemy.y, monster.x, monster.y)
        distHeroEnnemy = distance(ennemy.x, ennemy.y, heroes[firstHero].x, heroes[firstHero].y)
    dist = distance(monster.x , monster.y, heroes[firstHero].x, heroes[firstHero].y)
    distMonsterBase = distance(monster.x , monster.y, state.hisbase[0], state.hisbase[1])
    controlPotential, ennemiesToControl = controlEnnemyPotential(ennemies, heroes[firstHero], monster)
    ennemiesToControl.sort(key=sortByClosestHisBase)
    if ennemy and attackBasePotential(monster):
        #print("===>",dist,monster._id,distMonsterEnnemy,distEnnemyBase,distMonsterBase,windMonsterPotential2(monster, dist),file=sys.stderr, flush=True)
        # if windMonsterPotential2(monster, dist) and (distHeroEnnemy > 1280 or ennemyShield) and distMonsterBase > distEnnemyBase:
        # if state.ennemyDefender != -1 and windEnnemyPotential2(monster, ennemy):
        #     state.mymana -= 10
        #     return "SPELL WIND " + str(state.mybase[0]) + " " + str(state.mybase[1])
        if windMonsterPotential2(monster, dist):
            state.mymana -= 10
            return "SPELL WIND " + str(state.hisbase[0]) + " " + str(state.hisbase[1])
        if dist <= 2200 and monster.threatFor != 2  and monster.health >= 20 :
            state.mymana -= 10
            return "SPELL CONTROL " + str(monster._id) + " " + str(state.hisbase[0]) + " " + str(state.hisbase[1])
    if controlPotential:
        return attackEnnemyControl(ennemies[ennemiesToControl[0][0]])
    if shieldMonsterPotential(monster) and dist <= 2200 and monster.health >= 15 and ennemiesNearMonster(ennemies, monster) == 0:# and shieldedMonstersNearMonster(monsters, monster) == 0:
        state.mymana -= 10
        return "SPELL SHIELD " + str(monster._id)
    # if len(state.monstersInHisBase) > 0:
        # heroes[firstHero].targetID = monster._id
        # monsters[monster._id].nAttackers += 1
    #     return "MOVE " + str(monster.x) + " " + str(monster.y)
    # if len(state.monstersInHisBase):
    #     heroes[firstHero].targetID = monster._id
    #     monsters[monster._id].nAttackers += 1
        # return "MOVE " + str(monster.x) + " " + str(monster.y)
    # if len(state.monstersInHisBase):
    #     if (dist >= 800+900):
    #         heroes[firstHero].targetID = monster._id
    #         monsters[monster._id].nAttackers += 1
    #         return "MOVE " + str(monster.x) + " " + str(monster.y)
    # if state.ennemyDefender > 0 and nearHisBase(ennemy.x, ennemy.y):
    #     return "MOVE " + str(ennemy.x) + " " + str(ennemy.y)
    # elif state.turn % 15 > 9:
    #     return "MOVE " + str(attackPoint[0]) + " " + str(attackPoint[1])
    elif state.turn % 15 < 9:
        return "MOVE " + str(attackPoint[0]) + " " + str(attackPoint[1])  
    return "MOVE " + str(offsets[0][0]) + " " + str(offsets[0][1])

#================================== DEFANCE FUNCTIONS =========================================

def inDefenceZone(x, y):
    if distance(x, y, state.hisbase[0], state.hisbase[1]) > 6000:
        return False
    return True

#================================== ENNEMY FUNCTIONS =========================================

def ennemyWindDanger(ennemies, hero, monster):
    keys = []
    for key, ennemy in ennemies.items():
        distHeroEnnemy = distance(hero.x, hero.y, ennemy.x, ennemy.y)
        distMonsterEnnemy = distance(monster.x, monster.y, ennemy.x, ennemy.y)
        distMonsterBase = distance(monster.x, monster.y, state.mybase[0], state.mybase[1])
        if state.opmana >= 10 and distMonsterEnnemy <= 3000 and distMonsterBase <= 3000:
            keys += [(key, dist)]
    return (len(keys) != 0), keys

def ennemiesNearMonster(ennemies, monster):
    res = 0 
    for ennemy in ennemies.values():
        if distance(ennemy.x, ennemy.y, monster.x, monster.y) <= 1280:
            res += 1
    return res 

def shieldedMonstersNearMonster(monsters, monster):
    res = 0 
    for monst in monsters.values():
        if distance(monst.x, monst.y, monster.x, monster.y) <= 800:
            res += 1
    return res 

def attackEnnemyPotential(ennemy):
    if state.mymana >= 60 and ennemy.shield == 0:
        return True
    return False

def windEnnemyPotential(ennemy, hero):
    return True

def controlEnnemyPotential(ennemies, hero, monster):
    targets = []
    res = False
    for ennemy in ennemies.values():
        if not attackEnnemyPotential(ennemy): continue
        distEnnemyMonster = distance(ennemy.x, ennemy.y, monster.x, monster.y)
        distMonsterHero = distance(hero.x, hero.y, monster.x, monster.y)
        distEnnemyHero = distance(ennemy.x, ennemy.y, hero.x, hero.y)
        distEnnemyBase = distance(ennemy.x, ennemy.y, state.hisbase[0], state.hisbase[1])
        distMonsterBase = distance(monster.x, monster.y, state.hisbase[0], state.hisbase[1])
        if distEnnemyMonster < 1600 and monster.nearBase and monster.threatFor == 2 and ennemy.shield == 0 and distMonsterBase <= 1600:
            res = True
            targets += [(ennemy._id, distEnnemyMonster, distEnnemyBase)]
    return res, targets

def attackEnnemyControl(ennemy):
    if nearHisBase(ennemy.x, ennemy.y):
        return "SPELL CONTROL " + str(ennemy._id) + " " + str(state.mybase[0]) + " " + str(state.mybase[1])
    elif nearMyBase(ennemy.x, ennemy.y)  and not ennemy.shield:
        return "SPELL CONTROL " + str(ennemy._id) + " " + str(state.hisbase[0]) + " " + str(state.hisbase[1])
    return -1

def attackEnnemyWind(ennemy, hero):
    if attackEnnemyPotential(ennemy) and windEnnemyPotential(ennemy, hero):
        if nearHisBase(ennemy.x, ennemy.y):
            return "SPELL WIND "  + str(state.mybase[0]) + " " + str(state.mybase[1])
        elif nearMyBase(ennemy.x, ennemy.y):
            return "SPELL WIND "  + str(state.hisbase[0]) + " " + str(state.hisbase[1])
    return -1

#================================== GLOBAL VARIABLES =========================================

Bx, By = [int(i) for i in input().split()]
Ex , Ey = 17630 - Bx, 9000 - By
heroesCount = int(input())
firstHero = 0
heroes = {}
controlled = []
state = GameState(-1, -1, -1, -1, (-1, -1), (-1, -1))
defPoints = ((1500, 6000), (4500, 3500), (6000, 1500))
attackPoints = ((17500, 4250), (12800, 8900))
if Bx != 0:
    defPoints = [(17630 - defPoints[0][0], 9000 - defPoints[0][1]), (17630 - defPoints[1][0], 9000 - defPoints[1][1]), (17630 - defPoints[2][0], defPoints[2][1])]
    attackPoints = [(17630 - attackPoints[0][0], 9000 - attackPoints[0][1]), (17630 - attackPoints[1][0], 9000 - attackPoints[1][1])]

#================================== GAME LOOP =========================================

while True:
    
    monsters = {}
    ennemies = {}
    gamedata = []
    monsterIDs = []
    busy = []
    controlledEnnemies = []

    for i in range(2):
        gamedata += [int(j) for j in input().split()]

    if state.turn == 0:
        state = GameState(gamedata[0], gamedata[1], gamedata[2], gamedata[3], (Bx, By), (Ex, Ey))
    else:
        state.myhealth = gamedata[0]
        state.mymana = gamedata[1]
        state.ophealth = gamedata[2]
        state.opmana = gamedata[3]
        state.ennemiesNearHisBase = []
        state.monstersInMyBase = []
        state.monstersNearMyBase = []
        state.monstersInHisBase = []
        state.monstersNearHisBase = []
        state.ennemyAttacker = -1
        state.ennemyDefender = -1
 
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
            if nearHisBase(x, y): state.monstersNearHisBase += [_id]
            if nearMyBase(x, y): state.monstersNearMyBase += [_id]

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
            if nearHisBase(x, y):
                state.ennemiesNearHisBase += [_id]

    monsterIDs.sort(key=sortByClosestMyBase)
    if state.ultimatAttack:
        monsterIDs.sort(key=sortByClosestHisBase)
    state.monstersInMyBase = monstersInMyBase(monsters)
    state.monstersInHisBase = monstersInHisBase(monsters)
    state.monstersTargetingMyBase = monstersTargetingMyBase(monsters)
    state.monstersTargetingHisBase = monstersTargetingHisBase(monsters)

    #state.printData()

    if state.mymana < 30: state.ultimatAttack = False
    
    if not state.ennemyNearMyBase: 
        offsets = [(9500, 7000), (5000, 1500), (5500, 7500)]
    else: offsets = [(9500, 7000), (6500, 1500), (3500, 4500)]

    if (state.turn > 60 and len(state.monstersNearMyBase) == 0) or state.ultimatAttack: 
        offsets[0] = (11750, 7500)
        offsets[1] = (11750, 7500)
        offsets[2] = (3000, 2000)
        state.ultimatAttack = True

    
    revOffsets = [(17630 - offsets[0][0], 9000 - offsets[0][1]), (17630 - offsets[1][0], 9000 - offsets[1][1]), (17630 - offsets[2][0], 9000 - offsets[2][1])]
    controlOffset = 1000

    if Bx != 0: 
        firstHero = 3
        offsets = revOffsets
        controlOffset *= -1

    for i in range(3):
        if heroes[i + firstHero].isControlled == 1:
            state.useShield = True
        if heroes[i + firstHero].targetID not in monsters:
            heroes[i + firstHero].targetID = -1

    state.ennemyNearMyBase = False
    distMyBase = 9999999
    distHisBase = 9999999
    for ennemy in ennemies.values():
        dmb = distance(ennemy.x, ennemy.y, state.mybase[0], state.mybase[1])
        dhb = distance(ennemy.x, ennemy.y, state.hisbase[0], state.hisbase[1])
        if dmb < distMyBase:
            distMybase = dmb
            state.ennemyAttacker = ennemy._id
        if dhb < distHisBase:
            distHisbase = dhb
            state.ennemyDefender = ennemy._id
        if nearMyBase(ennemy.x, ennemy.y):
            state.ennemyNearMyBase = True

    heroes[firstHero].action = "MOVE " + str(offsets[0][0]) + " " + str(offsets[0][1])
    heroes[firstHero + 1].action = "MOVE " + str(offsets[1][0]) + " " + str(offsets[1][1])
    heroes[firstHero + 2].action = "MOVE " + str(offsets[2][0]) + " " + str(offsets[2][1])

    check = 0
    if state.ultimatAttack:
        check = 1
    if len(monsterIDs) and state.ultimatAttack:
        monster = monsterIDs[0]
        for monst in monsterIDs:
            if distance(monsters[monst[0]].x, monsters[monst[0]].y, offsets[0][0], offsets[0][1]) < 1280 and monsters[monster[0]].health > 6:
                monster = monst
                break

        distMonsterBase = distance(monsters[monster[0]].x, monsters[monster[0]].y, state.hisbase[0], state.hisbase[1])
        if allAttackersInPostion(monster) and state.mymana >= 30 and distMonsterBase < 6900:
            for i in range(2):
                heroes[i + firstHero].action = "SPELL WIND " + str(heroes[i + firstHero].x + (state.hisbase[0] - monsters[monster[0]].x)) + " " + str(heroes[i + firstHero].y + (state.hisbase[1] - monsters[monster[0]].y))
                busy += [i + firstHero]
            # for hero in heroes.values():
            #     heroes[hero._id].action = "SPELL WIND " + str(hero.x + (state.hisbase[0] - monsters[monster[0]].x)) + " " + str(hero.y + (state.hisbase[1] - monsters[monster[0]].y))
            #     busy += [hero._id]
        else:
            for i in range(2):
                if state.mymana >= 70 and i + firstHero not in busy:
                    action = controlHealthiestMonster(heroes[i + firstHero])
                    if action != -1:
                        heroes[i + firstHero].action = "SPELL CONTROL " + str(action) + " " + str(offsets[0][0]) + " " + str(offsets[0][1])
                        busy += [i + firstHero]
                        controlled += [action]
            # for hero in heroes.values():
            #         if state.mymana >= 70 and hero._id not in busy:
            #             action = controlHealthiestMonster(hero)
            #             if action != -1:
            #                 heroes[hero._id].action = "SPELL CONTROL " + str(action) + " " + str(offsets[0][0]) + " " + str(offsets[0][1])
            #                 busy += [hero._id]
            #                 controlled += [action]


    monsterIDs.sort(key=sortByClosestMyBase)
    for monster in monsterIDs:
        #if check: break   
        
        if len(busy) == 3:
            break
        if (monsters[monster[0]].threatFor == 1 and monsters[monster[0]].nearBase and monsters[monster[0]].nAttackers == 0):
            for i in range(3):
                heroes[i + firstHero].targetID = -1
        
        #monsters[monster[0]].printData()

        x = monsters[monster[0]].x
        y = monsters[monster[0]].y
        closestHero , dist = findClosestHeroToMonster(heroes, monsters[monster[0]])
        if closestHero == -1: continue

        other = -1
        if state.mybase[0] == 0:
            if closestHero == 1: other = 2
            elif closestHero == 2: other = 1
            else: other, temp = findClosestEntity(heroes, heroes[closestHero].x, heroes[closestHero].y)
        else:
            if closestHero == 4: other = 5
            elif closestHero == 5: other = 4
            else: other, temp = findClosestEntity(heroes, heroes[closestHero].x, heroes[closestHero].y)
        
        interX, interY = findIntersection(monsters[monster[0]], heroes[closestHero])
        interX2, interY2 = findIntersection(monsters[monster[0]], heroes[other])
        killable, steps1 = monsterIsKillable(monsters[monster[0]], heroes[closestHero], interX, interY, state.mybase[0], state.mybase[1])
        killable2, steps2 = monsterIsKillableBy2(monsters[monster[0]], heroes[other], interX2, interY2, steps1, state.mybase[0], state.mybase[1])

        mainX = mainY = otherX = otherY = -1
        if heroIsAttackingMonster(heroes[closestHero], monsters[monster[0]]):
            mainX = monsters[monster[0]].x
            mainY = monsters[monster[0]].y
        else:
            mainX = interX
            mainY = interY
        if heroIsAttackingMonster(heroes[other], monsters[monster[0]]):
            otherX = monsters[monster[0]].x
            otherY = monsters[monster[0]].y
        else:
            otherX = interX2
            otherY = interY2

        C = findClosestControlTarget(attackPoints, closestHero)
        #W, distW = findClosestWindTarget(monsters[monster[0]], defPoints)
        W = state.hisbase

        danger, attackingEnnemies = ennemyWindDanger(ennemies, heroes[closestHero], monsters[monster[0]])
        attackingEnnemies.sort(key=sortByClosestMyBase)

        if monsters[monster[0]].shield == 0 and dist <= 1280 and monsters[monster[0]].threatFor == 1 and monsters[monster[0]].nearBase and danger and state.mymana >= 10: 
            heroes[closestHero].action = "SPELL WIND " + str(W[0]) + " " + str(W[1])
            busy += [closestHero]
            state.mymana -= 10
            continue
            
        if state.useShield and state.mymana >= 50 and state.opmana >= 10 and heroes[closestHero].shield < 1 and len(state.monstersNearMyBase) and state.ennemyNearMyBase:
            heroes[closestHero].action = "SPELL SHIELD " + str(closestHero)
            busy += [closestHero]
            state.mymana -= 10
            continue

        # if danger:
        #     check = 0
        #     for ennemy in attackingEnnemies:
        #         attackAction = attackEnnemyControl(ennemies[ennemy[0]])
        #         if attackAction != -1 and ennemy[0] not in controlledEnnemies:
        #             heroes[closestHero].action = attackAction
        #             busy += [closestHero]
        #             state.mymana -= 10
        #             check = 1
        #             controlledEnnemies += [ennemy[0]]
        #             break
        #     if check: continue
            

        if not killable:
            if killable2 and not state.ultimatAttack:
                if other not in busy:
                    heroes[other].action = "MOVE " + str(otherX) + " " + str(otherY)
                    heroes[closestHero].action = "MOVE " + str(mainX) + " " + str(mainY)
                    heroes[closestHero].targetID = monster[0] 
                    heroes[other].targetID = monster[0] 
                    monsters[monster[0]].nAttackers += 2
                    busy += [closestHero]
                    busy += [other]
                    continue

            if state.mymana >= 10 and monsters[monster[0]].shield == 0 and dist <= 1280 and monsters[monster[0]].threatFor == 1 and monsters[monster[0]].nearBase: 
                heroes[closestHero].action = "SPELL WIND " + str(W[0]) + " " + str(W[1])
                busy += [closestHero]
                state.mymana -= 10
                continue
            
        elif not killable and not killable2: continue
        
        elif monsters[monster[0]].shield == 0 and dist <= 2200 and state.mymana >= 50 and monster[2] > 5000 and monster[1] > 5000 and monsters[monster[0]].health >= 20 and monster[0] not in controlled:
            heroes[closestHero].action = "SPELL CONTROL " + str(monster[0]) + " " + str(C[0]) + " " + str(C[1])
            busy += [closestHero]
            state.mymana -= 10
            controlled += [monster[0]]
            continue

        if (monsters[monster[0]].threatFor != 2):
            heroes[closestHero].action = "MOVE " + str(mainX) + " " + str(mainY)
            heroes[closestHero].targetID = monster[0]
            monsters[monster[0]].nAttackers += 1
            busy += [closestHero]

        # for i in range(heroesCount):
        #     if heroes[i + firstHero].targetID == monster[0]:
        #         heroes[i + firstHero].targetID = -1
        

    monsterIDs.sort(key=sortByClosestHisBase)

    
    # if len(monsterIDs) and state.mymana >= 70 and not check:
    #     heroes[firstHero].action = attackBase(monsters[monsterIDs[0][0]])
    # elif not check:
    #     for monster in monsterIDs:
    #         if  inAttackerFarmZone(monsters[monster[0]].x, monsters[monster[0]].y) and monsters[monster[0]].threatFor != 2:
    #             heroes[firstHero].action = heroes[firstHero].action = "MOVE " + str(monsters[monster[0]].x) + " " + str(monsters[monster[0]].y) + " A " + str(monster[0])
    #             break
    # else:
    #     heroes[firstHero].action = searchTarget(monsters[monsterIDs[0][0]])

    # lasttarget = -1
    # if state.turn == 70: lasttarget = heroes[firstHero + 2].targetID
    # if state.turn > 70 and len(monsterIDs):
    #     if heroes[firstHero + 2].targetID == lasttarget: pass
    #     # elif oportunity:
    #     #     for ennemy in defendingEnnemies:
    #     #         attackAction = attackEnemyControl(ennemies[ennemy[0]])
    #     #         if attackAction != -1 and ennemy[0] not in controlledEnnemies:
    #     #             heroes[firstHero + 2].action = attackAction
    #     #             busy += [firstHero + 2]
    #     #             state.mymana -= 10
    #     #             check = 1
    #     #             controlledEnnemies += [ennemy[0]]
    #     else:heroes[firstHero + 2].action = attackBase(monsters[monsterIDs[0][0]])

    for i in range(heroesCount):
        #heroes[i + firstHero].printData()
        print(heroes[i + firstHero].action)

    state.turn += 1