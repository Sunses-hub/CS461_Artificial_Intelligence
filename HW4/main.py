# coding=utf-8
# This is the submission of the project group named WATSON for Homework 3.
# To run: python main.py

# Members:
#           Mehmet Berk Şahin (CONTACT)
#           Balaj Saleem
#           Mehmet Alper Genç
#           Ege Hakan Karaağaç
#           Fırat Yönak

import random
import sys
import plotly.graph_objects as go
import plotly.offline as pyo
import plotly as py
import numpy as np
from copy import deepcopy
import random


# State is a 4x4 array
# moves are left right top bottom
MAX_PATH_LENGTH = 2147483647

def getIdealLocation(num):
    if num == 0:
        return 4, 4
    else:
        col = (num + 4) - 1
        if col < 0:
            col += 4
        row = int(num / 4)
        return row, col

def printPuzzle(puz, puzName):
    """
      This is function generates the figure for the puzzle visualization
      Parameters:
      puz: the state that is to be visualized
      puzName: the name of the puzzle figure
      Returns:
      Returns the figure of the puzzle
    """

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=[[puzName],
                    ['0'],
                    ['1'],
                    ['2'],
                    ['3']],
            fill_color='royalblue',
            line_color='darkslategray',
            font=dict(color='white')),
        cells=dict(values=[
            [0, 1, 2, 3],
            [puz[0][0], puz[1][0], puz[2][0], puz[3][0]],
            [puz[0][1], puz[1][1], puz[2][1], puz[3][1]],
            [puz[0][2], puz[1][2], puz[2][2], puz[3][2]],
            [puz[0][3], puz[1][3], puz[2][3], puz[3][3]]],
            fill=dict(color=['royalblue', 'white', 'white', 'white', 'white']),
            line_color='darkslategray',
            font=dict(color=['white', 'black', 'black', 'black', 'black'])))
    ])
    fig.update_layout(autosize=False, width=400, height=325)

    return fig


def randomPuzzleGenerator(goalState):
    """
      This is function generates the a random puzzle state starting from the goal state
      Parameters:
      goalState: the state that is to shuffled to obtain the final state
      Returns:
      Returns the shuffled state, which is solvable
    """
    directions = ['u', 'd', 'l', 'r']
    forbidden_directions = []
    variation_val = 20
    new_state = goalState
    for i in range(variation_val):
        zero_loc = getZeroLocation(new_state)
        forbidden_directions.clear()
        if (zero_loc[0] == 0):
            forbidden_directions.append('u')
        if (zero_loc[0] == 3):
            forbidden_directions.append('d')
        if (zero_loc[1] == 0):
            forbidden_directions.append('l')
        if (zero_loc[1] == 3):
            forbidden_directions.append('r')

        direction = random.choice(directions)
        while (direction in forbidden_directions):
            direction = random.choice(directions)

        new_state = move_zero(new_state, zero_loc[0], zero_loc[1], direction)
    return new_state


def goalStateGenerater():
    """
      This is function generates the goal state
      Parameters:
      Returns:
      Returns the fully arranged goal state
    """

    goal = [[y * 4 + x for x in range(1, 5)] for y in range(0, 4)]
    goal[3][3] = 0

    return goal


def getZeroLocation(state):
    return np.array(np.where(np.array(state) == 0)).T.flatten()


def move_zero(state, i, j, direction):
    """
      This function moves zero in a specified direction of up down left right
      Parameters:
      state: The state in which the zero is to be moved
      i: The row location of zero
      j: The column location of zero
      direction: the direction to move the zero in
      Returns:
      Returns the final state after the directional change is applied
    """
    return_state = deepcopy(state)
    if direction == 'u':
        return_state[i][j], return_state[i - 1][j] = return_state[i - 1][j], return_state[i][j]
        i = i - 1
    if direction == 'd':
        return_state[i][j], return_state[i + 1][j] = return_state[i + 1][j], return_state[i][j]
        i = i + 1
    if direction == 'l':
        return_state[i][j], return_state[i][j - 1] = return_state[i][j - 1], return_state[i][j]
        j = j - 1
    if direction == 'r':
        return_state[i][j], return_state[i][j + 1] = return_state[i][j + 1], return_state[i][j]
        j = j + 1
    return return_state


def getNewStates(currState, zero_loc, newPath, closed):
    """
       This function gets the states that are reachable from current state, and are not visited.

       Parameters:
           currState - the current state
           zero_loc - the location of zero in the current state graph
           newPath - the path to reach the current state
           closed - the states visited by the current path, to avoid loops.

       Returns: The list of states that will be added to the queue.
    """

    # For each direction (up, down, left, right) the function first checks if the zero can travel that way.
    # If so, computes the next state, and if this next state was not previously visited by the loop, adds it to
    # the new_states list.
    new_states = []
    if zero_loc[0] > 0:
        next_state = move_zero(currState, zero_loc[0], zero_loc[1], 'u')
        if next_state not in closed:
            new_states.append((newPath, next_state))
    if zero_loc[0] < 3:
        next_state = move_zero(currState, zero_loc[0], zero_loc[1], 'd')
        if next_state not in closed:
            new_states.append((newPath, next_state))
    if zero_loc[1] > 0:
        next_state = move_zero(currState, zero_loc[0], zero_loc[1], 'l')
        if next_state not in closed:
            new_states.append((newPath, next_state))
    if zero_loc[1] < 3:
        next_state = move_zero(currState, zero_loc[0], zero_loc[1], 'r')
        if next_state not in closed:
            new_states.append((newPath, next_state))
            # get the top w new states
    new_states.sort(key=lambda tup: tup[1])
    return new_states


def find_in_table(table, state):
    """
        This function finds a given state in the given table.
    """
    for i in range(len(table)):
        if table[i][0] == state:
            return i
    return -1


def getManDistance(p1, p2):
    """
        This function gets the Manhattan distance between two points.

        Parameters:
            p1 - The first point
            p2 - The second point

        Returns:
            The Manhattan distance between the points.
    """

    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def heuristic(state):
    # The heuristic we have chosen is the total Manhattan distance of each
    # item in the 15-puzzle matrix.

    # PROOF OF ADMISSIBILITY:
    # For a heuristic to be admissible it must never overestimate the cost of reaching the goal state[1].
    # Manhattan distance [2] is the heuristic value for a point(with x and y values) on a 2D grid / plane with the
    # formula |x1 - x2| + |y1 - y2|.
    #
    # According to the above definition above and the case of the puzzle, the manhattan distance for one tile is
    # basically the minimum / direct number of moves (up, down, left, right) the tile of a specified value, is away
    # from its ideal location (in goal state). The heuristic value we use for a state in the algorithm is the sum of
    # the Manhattan Distance values for all tiles. Since manhattan distance is the absolute / shortest / direct path
    # to the ideal location this can never overestimate the number of moves to reach the goal state, and thus is
    # admissible.

    # [1]Russell, S.J.; Norvig, P. (2002). Artificial Intelligence: A Modern Approach
    # [2]Paul E. Black, "Manhattan distance", in Dictionary of Algorithms and Data Structures [online], Paul E. Black,
    # ed. 11 February 2019

    totalDistance = 0
    for i in range(4):
        for j in range(4):
            num = state[i][j]
            ideal_location = getIdealLocation(num)
            totalDistance += getManDistance((i, j), ideal_location)
    return totalDistance


def a_star(initState, goalState):
    """
        This function performs the A* search algorithm (branch and bound search with admissible
        heuristic and dynamic programming).

        Parameters:
            initState - the initial state
            goalState - the goal state

        Returns:
            the list of states in the solution path if there is a solution, None otherwise.
    """

    queue = []
    table = []
    # The list is a list of 2-tuples. The second item is the last state in the path,
    # and the first item is the rest of the path. This separation is only done for cleaner code.
    queue.append(([], initState))
    table.append((initState, 0))

    while len(queue) > 0:
        # print("current queue: ", queue)
        # remove the first path from the queue
        curPath, curState = queue.pop(0)

        if curState == goalState:
            # return the solution path by combining the current path and the current state.
            return curPath + [curState]

        # Below is one of the two places where we have implemented DP. This is to check
        # if any shorter paths were found in the time interval between when the current path is added
        # to the queue, and when it is popped. In our experience, doing this becomes more efficient as
        # the queue grows in size, compared to also checking the queue items in the for-loop for DP below.
        curIndex = find_in_table(table, curState)

        if curIndex >= 0:
            if table[curIndex][1] < len(curPath):
                continue

        # create new non-cycle paths from the last state in the path.
        # loops are checked in the getNewStates function.
        zero_loc = getZeroLocation(curState)
        new_states = getNewStates(curState, zero_loc, curPath + [curState], curPath)

        # the below loop is one of the places we have implemented DP. For each possible new state, the loop
        # checks whether or not the terminal node is already in the table. If it is in the table, the code
        # checks whether or not the current solution is shorter, and updates the table if so. If the current
        # terminal node is not in the table, the code adds it to the table with the current solution as the
        # shortest path.
        #
        # In this loop, we decided not to check the paths already in the queue. They are checked after the
        # first path in the queue is removed, with a similar check. This was to make our program more efficient.
        for state in new_states:
            # check the table to try and find the terminal node of the current path.
            index = find_in_table(table, state[1])
            if index >= 0:
                table_entry = deepcopy(table[index])
                if len(state[0]) < table_entry[1]:
                    del table[index]
                    table.append((state[1], len(state[0])))
                    queue.append(state)
            else:
                table.append((state[1], len(state[0])))
                queue.append(state)

        # sort the entire queue by path length summed with the heuristic function.
        queue.sort(key=lambda tup: len(tup[0]) + heuristic(tup[1]))

    # return None if the goal state could not be found.
    return None


def trace_states(states):
    """
      This function traces / prints an array of states in an orderly fashion
      Parameters:
        states: a set of states
      Returns:
        Nothing
    """
    print('STATE HISTORY:')
    for state in states:
        print("----------------")
        print(np.array(state))


goal = goalStateGenerater()
print("Goal State:")
print(np.array(goal))

s = []
for i in range(10):
    new_start = randomPuzzleGenerator(goal)
    while new_start in s or new_start == goal:  # to avoid duplicate initial states, and also the goal state
        new_start = randomPuzzleGenerator(goal)
    s.append(new_start)

results = [a_star(item, goal) for item in s]


lengthS = []
c = 0 
avrg = 0
with open("homework4_initial_states.txt", "w") as f:
    for result in results:
        if result is not None:
            print(f"INITIAL STATE {c + 1}:")
            f.write(f"INITIAL STATE {c + 1}:\n")
            print(np.array(result[0]))
            f.write(str(np.array(result[0])) + "\n")
            # printout the 25 initial states to the command line.
            lengthS.append(len(result) - 1)
            c = c + 1
            avrg = avrg + len(result) - 1

allPlots = []
goal1 = printPuzzle(goal, "Goal")
allPlots.append(goal1)
f = open("homework4_solution_sequences.html", "w")
f.write("<h1> Goal State:</h1>")
f.write(goal1.to_html(full_html=False, include_plotlyjs='cdn'))
f.write("<hr>")

index0 = 0
index1 = 0

while index0 == index1:
    index0 = random.randrange(0, 10)
    index1 = random.randrange(0, 10)

f.write(f"<h2> Solution for S{index0 + 1}:</h2>")
f.write(f"<h3>Number of moves: {len(results[index0]) - 1}</h3>")
i = 0
for move in results[index0]:
    move_g = printPuzzle(move, (f"Initial State S{index0 + 1}: ")) if i == 0 else printPuzzle(move, ("S1 move: " + str(i)))
    allPlots.append(move_g)
    f.write(move_g.to_html(full_html=False, include_plotlyjs='cdn'))
    i = i + 1

f.write("<hr>")
f.write(f"<h2> Solution for S{index1 + 1}:</h2>")
f.write(f"<h3> Number of moves: {len(results[index1]) - 1}</h3>")
i = 0
for move in results[index1]:
    move_g = printPuzzle(move, (f"Initial State S{index1 + 1}: ")) if i == 0 else printPuzzle(move, ("S2 move: " + str(i)))
    allPlots.append(move_g)
    f.write(move_g.to_html(full_html=False, include_plotlyjs='cdn'))
    i = i + 1
f.close()

stateN = ["State1","State2","State3","State4","State5","State6","State7","State8","State9","State10"]

fig = go.Figure()
fig.add_trace(go.Scatter(x=stateN, y=lengthS, name='State Length',
                         line=dict(color='firebrick', width=4)))

avrg = avrg/10
avrg = format(avrg, '.3f')
print(avrg)
avg = "Average of Solutions = " + avrg

fig.update_layout(title="Length of each solution and the average length (" + avrg + "). 2 random solutions are printed in the homework4_solution_sequences.html file.",
                   xaxis_title='State',
                   yaxis_title='Length of Shortest Solution')

fig.update_layout(shapes=[
    # adds line at y=5
    dict(
      type= 'line',
      xref= 'paper', x0= 0, x1= 1,
      yref= 'y', y0= float(avrg), y1= float(avrg),
    )
])

fig.write_html('homework4_graph.html', auto_open=True)

