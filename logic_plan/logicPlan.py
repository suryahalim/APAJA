# logicPlan.py
# ------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In logicPlan.py, you will implement logic planning methods which are called by
Pacman agents (in logicAgents.py).
"""

import util
import sys
import logic
import game


pacman_str = 'P'
ghost_pos_str = 'G'
ghost_east_str = 'GE'
pacman_alive_str = 'PA'

class PlanningProblem:
    """
    This class outlines the structure of a planning problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the planning problem.
        """
        util.raiseNotDefined()

    def getGhostStartStates(self):
        """
        Returns a list containing the start state for each ghost.
        Only used in problems that use ghosts (FoodGhostPlanningProblem)
        """
        util.raiseNotDefined()
        
    def getGoalState(self):
        """
        Returns goal state for problem. Note only defined for problems that have
        a unique goal state such as PositionPlanningProblem
        """
        util.raiseNotDefined()

def tinyMazePlan(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def sentence1():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.
    
    A or B
    (not A) if and only if ((not B) or C)
    (not A) or (not B) or C
    """
    "*** YOUR CODE HERE ***"
    first = logic.Expr('|','A','B')
    second = logic.Expr('<=>',logic.Expr('~','A'), logic.Expr('|',logic.Expr('~','B'),'C'))
    third = logic.Expr('|',logic.Expr('~','A'),logic.Expr('~','B'),'C')
    return logic.Expr('&',first,second,third)

def sentence2():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.
    
    C if and only if (B or D)
    A implies ((not B) and (not D))
    (not (B and (not C))) implies A
    (not D) implies C
    """
    "*** YOUR CODE HERE ***"
    first = logic.Expr('<=>','C',logic.Expr('|','B','D'))
    second = logic.Expr('>>','A', logic.Expr('&',logic.Expr('~','B'),logic.Expr('~','D')))
    third = logic.Expr('>>',logic.Expr('~',logic.Expr('&','B',logic.Expr('~','C'))),'A')
    forth = logic.Expr('>>',logic.Expr('~','D'),logic.Expr('C'))
    return logic.Expr('&',first,second,third,forth)    

def sentence3():
    """Using the symbols WumpusAlive[1], WumpusAlive[0], WumpusBorn[0], and WumpusKilled[0],
    created using the logic.PropSymbolExpr constructor, return a logic.PropSymbolExpr
    instance that encodes the following English sentences (in this order):

    The Wumpus is alive at time 1 if and only if the Wumpus was alive at time 0 and it was
    not killed at time 0 or it was not alive and time 0 and it was born at time 0.

    The Wumpus cannot both be alive at time 0 and be born at time 0.

    The Wumpus is born at time 0.
    """
    "*** YOUR CODE HERE ***"
    wA1 = logic.PropSymbolExpr("WumpusAlive",1)
    wA0 = logic.PropSymbolExpr("WumpusAlive",0)
    wB0 = logic.PropSymbolExpr("WumpusBorn",0)
    wK0 = logic.PropSymbolExpr("WumpusKilled",0)
    first = logic.Expr('<=>',wA1,logic.Expr('|',logic.Expr('&',wA0,logic.Expr('~',wK0)), logic.Expr('&',logic.Expr('~',wA0),wB0)))  
    second = logic.Expr('~',logic.Expr('&',wA0,wB0))
    return logic.Expr('&',first,second,wB0)
    # return logic.Expr('&',wA1,wA0)

def findModel(sentence):
    """Given a propositional logic sentence (i.e. a logic.Expr instance), returns a satisfying
    model if one exists. Otherwise, returns False.
    """
    "*** YOUR CODE HERE ***"
    # print (sentence)
    # return 0
    sntence = logic.to_cnf(sentence)
    return logic.pycoSAT(sntence)

def atLeastOne(literals) :
    """
    Given a list of logic.Expr literals (i.e. in the form A or ~A), return a single 
    logic.Expr instance in CNF (conjunctive normal form) that represents the logic 
    that at least one of the literals in the list is true.
    >>> A = logic.PropSymbolExpr('A');
    >>> B = logic.PropSymbolExpr('B');
    >>> symbols = [A, B]
    >>> atleast1 = atLeastOne(symbols)
    >>> model1 = {A:False, B:False}
    >>> print logic.pl_true(atleast1,model1)
    False
    >>> model2 = {A:False, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    >>> model3 = {A:True, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    """
    "*** YOUR CODE HERE ***"
    ls = literals[0]
    for l in literals :
        ls|= l
    return ls
    # return logic.disjoin(literals)



def atMostOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form) that represents the logic that at most one of 
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    import itertools
    nLiterals = list()
    for i in literals :
        nLiterals += [logic.Expr('~',i)]
    tLiterals = (list(itertools.combinations(nLiterals,2)))
    oLiterals = logic.Expr('|',tLiterals[0][0],tLiterals[0][1])
    for i in tLiterals:
        oLiterals &= logic.Expr('|',i[0],i[1])
    return oLiterals


def exactlyOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form)that represents the logic that exactly one of 
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    import itertools
    nLiterals = list()
    ls = literals[0]
    for i in literals :
        nLiterals += [logic.Expr('~',i)]
        ls |= i
    tLiterals = (list(itertools.combinations(nLiterals,2)))
    oLiterals = logic.Expr('|',tLiterals[0][0],tLiterals[0][1])
    for i in tLiterals:
        oLiterals &= logic.Expr('|',i[0],i[1])
    return logic.Expr('&',ls,oLiterals)


def extractActionSequence(model, actions):
    """
    Convert a model in to an ordered list of actions.
    model: Propositional logic model stored as a dictionary with keys being
    the symbol strings and values being Boolean: True or False
    Example:
    >>> model = {"North[3]":True, "P[3,4,1]":True, "P[3,3,1]":False, "West[1]":True, "GhostScary":True, "West[3]":False, "South[2]":True, "East[1]":False}
    >>> actions = ['North', 'South', 'East', 'West']
    >>> plan = extractActionSequence(model, actions)
    >>> print plan
    ['West', 'South', 'North']
    """
    result = list()
    for i in range(len(model)):
       if model[model.keys()[i]] == True:
           if model.keys()[i].parseExpr(model.keys()[i])[0] in ["East","North","West","South"] :
               result.append(model.keys()[i].parseExpr(model.keys()[i]))

    sortResult = [x[0] for x in sorted(result, key = lambda x: int(x[1]))]

    return  sortResult


def pacmanSuccessorStateAxioms(x, y, t, walls_grid):
    """
    Successor state axiom for state (x,y,t) (from t-1), given the board (as a 
    grid representing the wall locations).
    Current <==> (previous position at time t-1) & (took action to move to x, y)
    """

    "*** YOUR CODE HERE ***"
    current = logic.PropSymbolExpr(pacman_str,x,y,t)
    posBefore = None
    if not walls_grid[x][y+1] :
        if posBefore == None :
            posBefore = logic.Expr('&',logic.PropSymbolExpr(pacman_str,x,y+1,t-1),logic.PropSymbolExpr('South',t-1))
        else :
            posBefore |= logic.Expr('&',logic.PropSymbolExpr(pacman_str,x,y+1,t-1),logic.PropSymbolExpr('South',t-1))
    if not walls_grid[x][y-1] :
        if posBefore == None :
            posBefore = logic.Expr('&',logic.PropSymbolExpr(pacman_str,x,y-1,t-1),logic.PropSymbolExpr('North',t-1))
        else :  
            posBefore |= logic.Expr('&',logic.PropSymbolExpr(pacman_str,x,y-1,t-1),logic.PropSymbolExpr('North',t-1))
    if not walls_grid[x-1][y] :
        if posBefore == None :
            posBefore = logic.Expr('&',logic.PropSymbolExpr(pacman_str,x-1,y,t-1),logic.PropSymbolExpr('East',t-1))
        else :
            posBefore |= logic.Expr('&',logic.PropSymbolExpr(pacman_str,x-1,y,t-1),logic.PropSymbolExpr('East',t-1))
    if not walls_grid[x+1][y] :
        if posBefore == None :
            posBefore = logic.Expr('&',logic.PropSymbolExpr(pacman_str,x+1,y,t-1),logic.PropSymbolExpr('West',t-1))
        else :
            posBefore |= logic.Expr('&',logic.PropSymbolExpr(pacman_str,x+1,y,t-1),logic.PropSymbolExpr('West',t-1))
    result = current%posBefore
    return result

def positionLogicPlan(problem):
    """
    Given an instance of a PositionPlanningProblem, return a list of actions that lead to the goal.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()
    "*** YOUR CODE HERE ***"    
    startState = problem.getStartState()
    start = logic.PropSymbolExpr("P",startState[0],startState[1],0)
    goalState = problem.getGoalState()
    currentState = startState
    visitedState = list()
    t = 1
    while t<=50:
        rules = list()
        for time in range(t):
            timeList = list()
            for x in range(1,width + 1):
                for y in range(1,height + 1):
                    if not walls[x][y]:
                        rules.append(exactlyOne([logic.PropSymbolExpr(direction, time) for direction in ['North', 'South', 'East', 'West']]))
                        rules.append(pacmanSuccessorStateAxioms(x,y,time+1,walls))
                        timeList.append(logic.PropSymbolExpr("P",x,y,0))
            rules.append(exactlyOne(timeList))
        goal = logic.PropSymbolExpr("P",goalState[0],goalState[1],t)
        model = findModel(logic.Expr('&',start,goal,logic.conjoin(rules)))
        if model:
            actions = extractActionSequence(model, ['North', 'South', 'East', 'West'])
            return actions
        t+=1
    return []

    # startState = problem.getStartState()
    # rules = [logic.PropSymbolExpr("P",startState[0],startState[1],0)]
    # goalState = problem.getGoalState()
    # timeList = list()
    # time = 0    
    # for posx in range(1,width+1):
    #         for posy in range(1,height+1):
    #             timeList.append(logic.to_cnf(logic.PropSymbolExpr("P",posx,posy,0)))
    # rules+=[exactlyOne(timeList)   ]

    # while time<=50:    
    #     for x in range(1,width + 1):
    #         for y in range(1,height + 1):
    #             if not walls[x][y]:
    #                 rules+=[logic.to_cnf(exactlyOne([logic.PropSymbolExpr(direction, time) for direction in ['North', 'South', 'East', 'West']]))]
    #                 rules+=[logic.to_cnf(pacmanSuccessorStateAxioms(x,y,time+1,walls))]

    #     goal = logic.PropSymbolExpr("P",goalState[0],goalState[1],time)
        
    #     model = findModel(logic.Expr('&',goal,logic.conjoin(rules)))

    #     if model:
    #         actions = extractActionSequence(model, ['North', 'South', 'East', 'West'])
    #         return actions
    #     time+=1
    # return []



def foodLogicPlan(problem):
    """
    Given an instance of a FoodPlanningProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()

    "*** YOUR CODE HERE ***"
    foodList =  problem.getStartState()[1].asList()
    startState = problem.getStartState()[0]
    start = logic.PropSymbolExpr("P",startState[0],startState[1],0)
    currentState = startState

    time = 0 
    rules= None

    timeList = list()
    for posx in range(1,width+1):
            for posy in range(1,height+1):
                timeList.append(logic.to_cnf(logic.PropSymbolExpr("P",posx,posy,0)))
    rules=exactlyOne(timeList)   
    
    while time<=50:
        for x in range(1,width + 1):
            for y in range(1,height + 1):
              rules&=exactlyOne([logic.PropSymbolExpr(direction, time) for direction in ['North', 'South', 'East', 'West']])
              rules&=logic.to_cnf(pacmanSuccessorStateAxioms(x,y,time+1,walls))

        goal=None
        for food in foodList:
            foodT = list()
            for t2 in range(time+1):
                foodT.append(logic.PropSymbolExpr("P",food[0],food[1],t2))
            if goal == None :
                goal=atLeastOne(foodT)
            else :
                goal&=atLeastOne(foodT)

        model = logic.pycoSAT(logic.Expr('&',start,goal,rules))
        if model:
            actions = extractActionSequence(model, ['North', 'South', 'East', 'West'])
            return actions
        time+=1

    return []




def ghostPositionSuccessorStateAxioms(x, y, t, ghost_num, walls_grid):
    """
    Successor state axiom for patrolling ghost state (x,y,t) (from t-1).
    Current <==> (causes to stay) | (causes of current)
    GE is going east, ~GE is going west 
    """
    pos_str = ghost_pos_str+str(ghost_num)
    east_str = ghost_east_str+str(ghost_num)
    "*** YOUR CODE HERE ***"
    current = logic.PropSymbolExpr(pos_str,x,y,t)
    posBefore = None
    #move east
    if not walls_grid[x-1][y] :
        causesCur = logic.PropSymbolExpr(pos_str,x-1,y,t-1)& logic.PropSymbolExpr(east_str,t-1)
        if posBefore == None :
            posBefore = causesCur
        else :
            posBefore |= causesCur
    #move west    
    if not walls_grid[x+1][y] :
        causesCur = logic.PropSymbolExpr(pos_str,x+1,y,t-1)& ~logic.PropSymbolExpr(east_str,t-1)
        if posBefore == None :
            posBefore = causesCur
        else :
            posBefore |= causesCur
    if walls_grid[x+1][y] and walls_grid[x-1][y] :
        causesStay1 = logic.PropSymbolExpr(pos_str,x,y,t-1)
        if posBefore == None :
            posBefore = causesStay1
        else :
            posBefore |= causesStay1
    result = current%posBefore
    return result

def ghostDirectionSuccessorStateAxioms(t, ghost_num, blocked_west_positions, blocked_east_positions):
    """
    Successor state axiom for patrolling ghost direction state (t) (from t-1).
    west or east walls.
    Current <==> (causes to stay) | (causes of current)
    """
    pos_str = ghost_pos_str+str(ghost_num)
    east_str = ghost_east_str+str(ghost_num)

    "*** YOUR CODE HERE ***"
    current = logic.PropSymbolExpr(east_str,t)
    conjoined = None
    expressions = logic.PropSymbolExpr(east_str,t-1)

    for x in blocked_east_positions:
        if x not in blocked_west_positions or x in blocked_west_positions:
            if conjoined == None:
                conjoined = ~logic.PropSymbolExpr(pos_str,x[0],x[1],t)
            else : 
                conjoined &= ~logic.PropSymbolExpr(pos_str,x[0],x[1],t)
            conjoined |= ~logic.PropSymbolExpr(east_str, t - 1)

    for x in blocked_west_positions:
        expressions |= logic.PropSymbolExpr(pos_str,x[0],x[1],t) 

    expressions &=conjoined
    result = current%expressions

    return result # Replace this with your expression


def pacmanAliveSuccessorStateAxioms(x, y, t, num_ghosts):
    """
    Successor state axiom for patrolling ghost state (x,y,t) (from t-1).
    Current <==> (causes to stay) | (causes of current)
    """
    ghost_strs = [ghost_pos_str+str(ghost_num) for ghost_num in xrange(num_ghosts)]

    "*** YOUR CODE HERE ***"
    causesCur =None
    current = ~logic.PropSymbolExpr(pacman_alive_str,t)
    for g in ghost_strs: 
        if causesCur == None :
            causesCur = logic.PropSymbolExpr(g,x,y,t-1)
            causesCur |= logic.PropSymbolExpr(g,x,y,t) 
        else : 
            causesCur |= logic.PropSymbolExpr(g,x,y,t-1) 
            causesCur |= logic.PropSymbolExpr(g,x,y,t) 
    return current % ((causesCur& logic.PropSymbolExpr(pacman_str,x,y,t))|~logic.PropSymbolExpr(pacman_alive_str,t-1))


def foodGhostLogicPlan(problem):
    """
    Given an instance of a FoodGhostPlanningProblem, return a list of actions that help Pacman
    eat all of the food and avoid patrolling ghosts.
    Ghosts only move east and west. They always start by moving East, unless they start next to
    and eastern wall. 
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()

    "*** YOUR CODE HERE ***"
    foodList =  problem.getStartState()[1].asList()
    startState = problem.getStartState()[0]
    ghostState = problem.ghostStartStates
    start = logic.PropSymbolExpr("P",startState[0],startState[1],0)
    time = 0

    #only the corners
    
    ghostY = list()
    rules= logic.PropSymbolExpr("PA",0)
    for (index, ghost) in enumerate(ghostState):
        if walls[ghost.getPosition()[0]+1][ghost.getPosition()[1]]:
            rules &= ~logic.PropSymbolExpr("GE"+str(index),0)
        else: 
            rules &= logic.PropSymbolExpr("GE"+str(index),0)
        rules &= logic.PropSymbolExpr("G"+str(index),ghost.getPosition()[0],ghost.getPosition()[1],0)
        ghostY.append(ghost.getPosition()[1])

    blocked_east1 = []
    blocked_west1 = []

    timeList = list()
    for posx in range(1,width+1):
            for posy in range(1,height+1):
                timeList.append(logic.to_cnf(logic.PropSymbolExpr("P",posx,posy,0)))
                if posy in ghostY:
                    if walls[posx+1][posy] and not walls[posx][posy] :
                        blocked_east1 += [(posx, posy)]
                    if walls[posx-1][posy] and not walls[posx][posy]:
                        blocked_west1 += [(posx, posy)]
    rules&=exactlyOne(timeList)   
    
    for index in range(len(ghostState)):
            ghostTimeList = list()
            for x in range(1,width+1):
                for y in range(1,height+1):
                    if y in ghostY:
                        ghostTimeList.append(logic.PropSymbolExpr("G"+str(index),x,y,0))
            rules&=exactlyOne(ghostTimeList)

    while time<=50:
        for x in range(1,width + 1):
            for y in range(1,height + 1):
              rules&=exactlyOne([logic.PropSymbolExpr(direction, time) for direction in ['North', 'South', 'East', 'West']])
              rules&=logic.to_cnf(pacmanSuccessorStateAxioms(x,y,time+1,walls))
              # print logic.to_cnf(pacmanAliveSuccessorStateAxioms(x,y,time+1,len(ghostState)))
              if y in ghostY:
                rules&=logic.to_cnf(pacmanAliveSuccessorStateAxioms(x,y,time+1,len(ghostState)))
                for (index, g) in enumerate(ghostState):            
                    rules&=logic.to_cnf(ghostPositionSuccessorStateAxioms(x,y,time+1,index,walls) & ghostDirectionSuccessorStateAxioms(time+1,index,blocked_west1,blocked_east1))        
        goal=None
        for food in foodList:
            foodT = list()
            for t2 in range(time+1):
                foodT.append(logic.PropSymbolExpr("P",food[0],food[1],t2))
            if goal == None :
                goal=atLeastOne(foodT)
            else :
                goal&=atLeastOne(foodT)

        model = logic.pycoSAT(logic.Expr('&',start,goal,rules, logic.PropSymbolExpr("PA",time)))
        if model:
            actions = extractActionSequence(model, ['North', 'South', 'East', 'West'])
            return actions
        time+=1

    return []


# Abbreviations
plp = positionLogicPlan
flp = foodLogicPlan
fglp = foodGhostLogicPlan

# Some for the logic module uses pretty deep recursion on long expressions
sys.setrecursionlimit(100000)
    