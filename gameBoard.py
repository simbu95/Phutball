import json
import random
import copy
import ipdb
import time
from src.MCTS import GameState, MCTS

class Action:
    def __init__(self,is_jump,act):
        self.is_jump=is_jump
        self.act=act
        
    def __eq__(self, other):
        """
        :type other: Action
        """
        return self.act == other.act

    def __hash__(self):
        if self.is_jump:
            return hash(','.join(map(str,self.act)))
        else:
            return hash(self.act)

    def __repr__(self) -> str:
        return 'Action(action_type={})'.format(self.act)

    def __str__(self) -> str:
        if self.is_jump:
            return ','.join(map(str,self.act))
        else:
            return self.act
        

class gameBoard(GameState):
    def __init__(self):
        self.topWins=False;
        self.bottomWins=False;
        self.gameOver=False;
        self.gameBoard={"0":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        "1":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        "2":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        "3":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        "4":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        "5":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        "6":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        "7":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        "8":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        "9":[0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0],
                        "10":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        "11":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        "12":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        "13":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        "14":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        "15":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        "16":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        "17":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        "18":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}
    def put(self,x,y):
        self.gameBoard[str(x)][y]=1
    def toJson(self):
        return json.dumps(self.gameBoard,indent=2)
    def reset(self):
        self.topWins=False;
        self.bottomWins=False;
        self.gameOver=False;
        self.gameBoard={"0":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        "1":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        "2":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        "3":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        "4":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        "5":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        "6":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        "7":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        "8":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        "9":[0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0],
                        "10":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        "11":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        "12":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        "13":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        "14":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        "15":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        "16":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        "17":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        "18":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}
                        
    def jump(self,dir):
        #ipdb.set_trace()
        for i in range(len(self.gameBoard)):
            for j in range(len(self.gameBoard[str(i)])):
                if self.gameBoard[str(i)][j] == 2:
                    x = i
                    y = j
        l = 1;
        switcher={"N":[0,1],"NE":[1,1],"E":[1,0],
                "SE":[1,-1],"S":[0,-1],"SW":[-1,-1],"W":[-1,0],"NW":[-1,1]}
        i=switcher[dir][0]
        j=switcher[dir][1]
        if(checkBounds(x + l * i, y + l * j) and self.gameBoard[str(x + l * i)][y + l * j] == 1):
            self.gameBoard[str(x)][y] = 0
            while checkBounds(x + l * i, y + l * j) and self.gameBoard[str(x + l * i)][y + l * j] == 1:
                self.gameBoard[str(x + l * i)][y + l * j] = 0
                l = l + 1
            if (y + l * j) <= 17:
                if((y + l * j) >= 1):
                    self.gameBoard[str(x + l * i)][y + l * j] = 2
                else:
                    self.gameOver = True
                    self.bottomWins = True
            else:
                self.gameOver = True
                self.topWins = True
                print("Game Over")
        
    def AIMove(self):
        puts, jumps = findAllMoves(self.gameBoard)
        if len(jumps) == 0 or random.randint(0, 1) == 0:
            p = random.choice(puts)
            self.gameBoard[p.split(",")[1]][int(p.split(",")[2])] = 1
        else:
            j = random.choice(jumps)
            for js in j['jumps']:
                self.jump(js[0])
        return
        
    def mc(self):
        p,j=findAllMoves(self.gameBoard)
        print(len(p))
        print(len(j))
        
    def is_terminal(self):
        return self.gameOver
        
    def get_possible_actions(self):
        #print("Finding Actions")
        #print(self.gameBoard)
        puts,jumps=findAllMoves(self.gameBoard)
        #print("Actions Found")
        actions=[]
        for p in puts:
            actions.append(Action(False,p))
        for j in jumps:
            actions.append(Action(True,j['jumps']))
        return actions
        
    def take_action(self,action):
        new_state = copy.deepcopy(self)
        if action.is_jump:
            for j in action.act:
                new_state.jump(j[0])
        else:
            new_state.put(int(action.act.split(",")[1]),int(action.act.split(",")[2]))
        return new_state
        
    def get_reward(self):
        if self.topWins:
            return 1
        else:
            return 0;

def findAllMoves(game):
    x, y = 0, 0
    puts = []
    for i in range(len(game)):
        for j in range(len(game[str(i)])):
            if game[str(i)][j] == 0:
                puts.append('P,{0},{1}'.format(i, j))
            elif game[str(i)][j] == 2:
                x = i
                y = j
    g = {'x': x, 'y': y, 'jumps': [], 'game': game}
    jumps = findAllJumps(g)
    return puts, jumps


def findAllJumps(g):
    #print("NextLayer")
    x = g['x']
    y = g['y']
    #print(x)
    #print(y)
    #print(g['game'])
    #print(g['jumps'])
    jumps = g['jumps']
    game = g['game']
    states = []
    if x > 0 and game[str(x-1)][y] == 1:
        gp = jumpDir(x, y, -1, 0, game)
        if 0 <= gp['x'] <= 18:
            gp['jumps'] = jumps.copy()
            gp['jumps'].append(['W'])
            #print("W")
            states.append(gp)
            if 1 <= gp['y'] <= 17:
                states = states + findAllJumps(gp)
    if x > 0 and y > 0 and game[str(x-1)][y-1] == 1:
        gp = jumpDir(x, y, -1, -1, game)
        if 0 <= gp['x'] <= 18:
            gp['jumps'] = jumps.copy()
            gp['jumps'].append(['SW'])
            states.append(gp)
            #print("SW")
            if 1 <= gp['y'] <= 17:
                states = states + findAllJumps(gp)
    if y > 0 and game[str(x)][y-1] == 1:
        gp = jumpDir(x, y, 0, -1, game)
        if 0 <= gp['x'] <= 18:
            gp['jumps'] = jumps.copy()
            gp['jumps'].append(['S'])
            states.append(gp)
            #print("S")
            if 1 <= gp['y'] <= 17:
                states = states + findAllJumps(gp)
    if x < 18 and y > 0 and game[str(x+1)][y-1] == 1:
        gp = jumpDir(x, y, +1, -1, game)
        if 0 <= gp['x'] <= 18:
            gp['jumps'] = jumps.copy()
            gp['jumps'].append(['SE'])
            states.append(gp)
            #print("SE")
            if 1 <= gp['y'] <= 17:
                states = states + findAllJumps(gp)
    if x < 18 and game[str(x+1)][y] == 1:
        gp = jumpDir(x, y, +1, 0, game)
        if 0 <= gp['x'] <= 18:
            gp['jumps'] = jumps.copy()
            gp['jumps'].append(['E'])
            states.append(gp)
            #print("E")
            if 1 <= gp['y'] <= 17:
                states = states + findAllJumps(gp)
    if x < 18 and y < 18 and game[str(x+1)][y+1] == 1:
        gp = jumpDir(x, y, +1, +1, game)
        if 0 <= gp['x'] <= 18:
            gp['jumps'] = jumps.copy()
            gp['jumps'].append(['NE'])
            states.append(gp)
            #print("NE")
            if 1 <= gp['y'] <= 17:
                states = states + findAllJumps(gp)
    if y < 18 and game[str(x)][y+1] == 1:
        gp = jumpDir(x, y, 0, +1, game)
        if 0 <= gp['x'] <= 18:
            gp['jumps'] = jumps.copy()
            gp['jumps'].append(['N'])
            states.append(gp)
            #print("N")
            if 1 <= gp['y'] <= 17:
                states = states + findAllJumps(gp)
    if x > 0 and y < 18 and game[str(x-1)][y+1] == 1:
        gp = jumpDir(x, y, -1, +1, game)
        if 0 <= gp['x'] <= 18:
            gp['jumps'] = jumps.copy()
            gp['jumps'].append(['NW'])
            states.append(gp)
            #print("NW")
            if 1 <= gp['y'] <= 17:
                states = states + findAllJumps(gp)
    return states


def jumpDir(x, y, i, j, game):
    l = 1;
    g = copy.deepcopy(game)
    g[str(x)][y] = 0
    while checkBounds(x + l * i, y + l * j) and game[str(x + l * i)][y + l * j] == 1:
        g[str(x + l * i)][y + l * j] = 0
        l = l + 1
    if checkBounds(x + l * i, y + l * j):
        g[str(x + l * i)][y + l * j] = 2
    r = {'x': x + l * i, 'y': y + l * j, 'game': g}
    return r


def checkBounds(x, y):
    return 0 <= x <= 18 and 0 <= y <= 18