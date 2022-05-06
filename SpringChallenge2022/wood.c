#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <math.h>

#define T_MONSTER 0
#define T_MYHERO 1
#define T_ENHERO 2
#define T_ROLE_DEF 0
#define T_ROLE_ATC 1

#define STARTING_HEALTH 3
#define MONSTER_DAMAGE 1
#define MAX_MAP_X 17630
#define MAX_MAP_Y 9000
#define HERO_MOVE_SPEED 800
#define MONSTER_MOVE_SPEED 400
#define BASE_DANGER_ZONE 300

typedef struct base{
    int x;
    int y;
} base;

typedef struct entity{
    // Unique identifier
    int id;
    int type;
    int x;
    int y;
    int shield_life;
    int is_controlled;
    int health;
    int vx;
    int vy;
    int near_base;
    int distance_base;
    int threat_for;
    int distance_enbase;
} entity;

typedef struct monster{
    int id;
    int x;
    int y;
    int shield_life;
    int is_controlled;
    int health;
    int vx;
    int vy;
    int near_base;
    int threat_for;
    int distance_base;
    int distance_myhero;
    int danger_lvl;
    int distance_enbase;
} monster;

typedef struct hero{
    int id;
    int role;
    int x;
    int y;
    int shield_life;
    int is_controlled;
    int health;
    int vx;
    int vy;
    int near_base;
    int threat_for;
    int distance_base;
    int distance_enbase;
} hero;

typedef struct playerStats{
    int health;
    int mana;
    hero myHero;
    hero enHero;
} playerStats;

typedef struct game{
    playerStats stats[2];
} game;

void showEntities(entity *entities, int nb)
{
    fprintf(stderr,"[E]%16s|%16s|%16s|%16s|%16s|%16s|%16s|%16s|%16s|%16s|%16s|%16s[E]\n","id", "type", "x", "y", "shield_life", "is_controlled", "health", "vx", "vy", "near_base", "threat_for", "distance_base");
    for (int i = 0; i < nb; i++) {
        fprintf(stderr,"->>%16d|%16d|%16d|%16d|%16d|%16d|%16d|%16d|%16d|%16d|%16d|%16d<<-\n", entities[i].id, entities[i].type, entities[i].x, entities[i].y, entities[i].shield_life, entities[i].is_controlled, entities[i].health, entities[i].vx, entities[i].vy, entities[i].near_base, entities[i].threat_for, entities[i].distance_base);
    }
}

void showMonsters(monster *entities, int nb)
{
    fprintf(stderr,"[M]%16s|%16s|%16s|%16s|%16s|%16s|%16s|%16s|%16s|%16s|%16s[M]\n","id", "x", "y", "shield_life", "is_controlled", "health", "vx", "vy", "near_base", "threat_for", "distance_base");
    for (int i = 0; i < nb; i++) {
        fprintf(stderr,"->>%16d|%16d|%16d|%16d|%16d|%16d|%16d|%16d|%16d|%16d|%16d<<-\n", entities[i].id, entities[i].x, entities[i].y, entities[i].shield_life, entities[i].is_controlled, entities[i].health, entities[i].vx, entities[i].vy, entities[i].near_base, entities[i].threat_for, entities[i].distance_base);
    }
}

void wait(char *msg)
{
    printf("WAIT %s\n", msg);
}

int distance(float x1, float y1, float x2, float y2)
{
	return(sqrt(((x2-x1)*(x2-x1))+((y2-y1)*(y2-y1))));
}

void move(int x, int y, char *msg)
{
    printf("MOVE %d %d %s\n", x, y, msg);
}

void attackMonster(monster m)
{
    printf("MOVE %d %d A%d\n", m.x, m.y, m.id);
}

static int cmpMonsterMyDistance(const void *p1, const void *p2)
{
    entity entity_a = * ( (entity*) p1 );
    entity entity_b = * ( (entity*) p2 );
    int a = entity_a.distance_base;
    int b = entity_b.distance_base;

    if ( a == b ) return 0;
    else if ( a < b ) return -1;
    else return 1;
}

static int cmpMonsterEnDistance(const void *p1, const void *p2)
{
    entity entity_a = * ( (entity*) p1 );
    entity entity_b = * ( (entity*) p2 );
    int a = entity_a.distance_enbase;
    int b = entity_b.distance_enbase;

    if ( a == b ) return 0;
    else if ( a < b ) return -1;
    else return 1;
}

monster *monsterCpy(monster *old)
{
    monster *new = calloc(1, sizeof(monster));
    new->x = old->x;
    new->y = old->y;
    new->id = old->id;
    new->is_controlled = old->is_controlled;
    new->near_base = old->near_base;
    new->shield_life = old->shield_life;
    new->vx = old->vx;
    new->vy = old->vy;
    new->danger_lvl =   old->danger_lvl;
    new->distance_base = old->distance_base;
    new->distance_myhero = old->distance_myhero;
    new->health = old->health;
    new->threat_for = old->threat_for;
    free(old);
    return (new);
}

monster *sortMonsters(monster **unsorted, int nb)
{
    monster **sorted;

    sorted = calloc((nb + 1), sizeof(monster*));
    for (int i = 0; i < nb; i++){
        sorted[i] = monsterCpy(unsorted[i]);
    }
    monster *tmp;
    for (int i = 0; i < nb; i++)
    {
        for (int j = 0; j < nb - i - 1; j++)
        {
            if (sorted[j]->distance_base > sorted[j + 1]->distance_base)
            {
                tmp = monsterCpy(sorted[j]);
                sorted[j] = monsterCpy(sorted[j + 1]);
                sorted[j + 1] = monsterCpy(tmp);
            }
        }
    }
    return (*sorted);
}

void bubbleSort(int array[], int size) {

  // loop to access each array element
  for (int step = 0; step < size - 1; ++step) {
      
    // loop to compare array elements
    for (int i = 0; i < size - step - 1; ++i) {
      
      // compare two adjacent elements
      // change > to < to sort in descending order
      if (array[i] > array[i + 1]) {
        
        // swapping occurs if elements
        // are not in the intended order
        int temp = array[i];
        array[i] = array[i + 1];
        array[i + 1] = temp;
      }
    }
  }
}
int md_comparator(const void *v1, const void *v2)
{
    const monster *p1 = (monster *)v1;
    const monster *p2 = (monster *)v2;
    if (p1->distance_base < p2->distance_base)
        return -1;
    else if (p1->distance_base > p2->distance_base)
        return +1;
    else
        return 0;
}
int main()
{
    // The corner of the map representing your base
    base myBase;
    base enBase;

    scanf("%d%d", &myBase.x, &myBase.y);
    enBase.x = 0;
    enBase.y = 0;
    if (myBase.x == 0)
    {
        enBase.x = MAX_MAP_X;
        enBase.y = MAX_MAP_Y;
    }
    // Always 3
    int heroes_per_player;
    scanf("%d", &heroes_per_player);
    // game loop
    game g;
    int turn = 0;
    while (1) {
        turn++;
        for (int i = 0; i < 2; i++) {
            scanf("%d%d", &g.stats[i].health, &g.stats[i].mana);
        }
        int entity_count;
        scanf("%d", &entity_count);
        entity entities[entity_count];
        bzero(&entities, sizeof(entity) * entity_count);
        hero   myHeroes[3];
        hero   enHeroes[3];
        int    nbMonsters = 0;
        int    nbEnHeroes = 0;
        int j = 0;
        for (int i = 0; i < entity_count; i++) {
            scanf("%d%d%d%d%d%d%d%d%d%d%d", &entities[i].id, &entities[i].type, &entities[i].x, &entities[i].y, &entities[i].shield_life, &entities[i].is_controlled, &entities[i].health, &entities[i].vx, &entities[i].vy, &entities[i].near_base, &entities[i].threat_for);
            entities[i].distance_base = distance(entities[i].x, entities[i].y, myBase.x, myBase.y);
            entities[i].distance_enbase = distance(entities[i].x, entities[i].y, enBase.x, enBase.y);
            if (entities[i].type == T_MYHERO)
            {
                myHeroes[j].id = entities[i].id;
                myHeroes[j].health = entities[i].health;
                myHeroes[j].is_controlled = entities[i].is_controlled;
                myHeroes[j].near_base = entities[i].near_base;
                myHeroes[j].threat_for = entities[i].threat_for;
                myHeroes[j].x = entities[i].x;
                myHeroes[j].y = entities[i].y;
                myHeroes[j].vx = -1;
                myHeroes[j].vy = -1;
                myHeroes[j].shield_life = entities[i].shield_life;
                myHeroes[j].distance_base = entities[i].distance_base;
                myHeroes[j].distance_enbase = entities[i].distance_enbase;
                j++; 
            }
            else if (entities[i].type == T_ENHERO)
            {
                enHeroes[nbEnHeroes].id = entities[i].id;
                enHeroes[nbEnHeroes].health = entities[i].health;
                enHeroes[nbEnHeroes].is_controlled = entities[i].is_controlled;
                enHeroes[nbEnHeroes].near_base = entities[i].near_base;
                enHeroes[nbEnHeroes].threat_for = entities[i].threat_for;
                enHeroes[nbEnHeroes].x = entities[i].x;
                enHeroes[nbEnHeroes].y = entities[i].y;
                enHeroes[nbEnHeroes].vx = -1;
                enHeroes[nbEnHeroes].vy = -1;
                enHeroes[nbEnHeroes].shield_life = entities[i].shield_life;
                enHeroes[nbEnHeroes].distance_base = entities[i].distance_base;
                enHeroes[nbEnHeroes].distance_enbase = entities[i].distance_enbase;
                nbEnHeroes++;
            }
            else
                nbMonsters++;
        }
        monster *monsters = calloc(nbMonsters + 1, sizeof(monster));
        j = 0;
        for (int i = 0; i < entity_count; i++)
        {
            if (entities[i].type == T_MONSTER)
            {
                monsters[j].id = entities[i].id;
                monsters[j].is_controlled = entities[i].is_controlled;
                monsters[j].near_base = entities[i].near_base;
                monsters[j].x = entities[i].x;
                monsters[j].y = entities[i].y;
                monsters[j].vx = entities[i].vx;
                monsters[j].vy = entities[i].vy;
                monsters[j].threat_for = entities[i].threat_for;
                monsters[j].health = entities[i].health;
                monsters[j].shield_life = entities[i].shield_life;
                monsters[j].distance_base = entities[i].distance_base;
                monsters[j++].distance_enbase = entities[i].distance_enbase;

            }
        }
        //showEntities(entities, entity_count);
        qsort(monsters, nbMonsters, sizeof(monster), cmpMonsterMyDistance);
        char *enMonsters = calloc(nbMonsters + 1, sizeof(monster));
        memcpy(enMonsters, monsters, sizeof(monster) * nbMonsters);
        qsort(monsters, nbMonsters, sizeof(monster), cmpMonsterEnDistance);
        for (int i = 0; i < 3; i++){
                move(monsters[i].x,monsters[i].y,"test");
        }
        for (int i = 0; i < 1; i++) {
            
        }
    }
    return 0;
}