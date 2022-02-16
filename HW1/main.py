# coding=utf-8
# This is the submission of the project group named WATSON for Homework 1. Coded on Python 3.9.1.
# To run normally: python main.py
# To run in single-stepping mode: python main.py trace

# Members:
#           Mehmet Berk Şahin (CONTACT)
#           Balaj Saleem
#           Mehmet Alper Genç
#           Ege Hakan Karaağaç
#           Fırat Yönak

# We have achieved nondeterminism by inserting the tuples into the queues in a random index, as it was required
# by the non-deterministic search pseudocode.
# We have done this by using Python's "random" library and its random.randint(x, y) function that returns a random
# number in the range [x, y]. For us, it was the range [0, <length_of_queue>].

# We have avoided loops in 2 areas:
# First, while calculating all possible river crossings using the "move" function, we implemented a check to not
# consider any river crossings that lead to a visited state. We have done so by taking the list of visited states
# as a parameter into the "move" function.
#
# Secondly, while calculating the non-deterministic search, we implemented 2 checks:
# The first check is done while considering the states safely reachable by the current first state in the queue.
# For each such states, the code first checks if that state was previously visited, and adds it to the queue only
# if it has not been previously visited. Secondly, before considering the state at the head of the queue, we check
# if it has been visited before using a different path. This is used to counteract any duplicates in the queue due
# to the randomness of the Non-Deterministic Search algorithm.

import random
import sys


class State:
    def __init__(self, mWest, cWest, mEast, cEast, boatloc):
        """
          This is the only constructor for a State object.

          Parameters:
          mWest   : The number of missionaries on the west bank.
          cWest   : The number of cannibals on the wast bank.
          mEast   : The number of missionaries on the east bank.
          cEast   : The number of cannibals on the east bank.
          boatloc : The bank on which the boat currently is.
        """
        self.mWest = mWest
        self.cWest = cWest
        self.mEast = mEast
        self.cEast = cEast
        self.boatloc = boatloc

    def print(self):
        """
          This function prints the details of the State object.

          Parameters:
          None

          Returns:
          None
        """
        print("Cannibals on West Bank: " + str(self.cWest))
        print("Missionaries on West Bank: " + str(self.mWest))
        print("Cannibals on East Bank: " + str(self.cEast))
        print("Missionaries on East Bank: " + str(self.mEast))
        print("")

    def lite_print(self):
        """
          This function prints the details of the State object, in a lighter manner
          compared to the print() function.

          Parameters:
          None

          Returns:
          None
        """
        print((self.mWest, self.cWest, self.mEast, self.cEast, self.boatloc))


def is_equal(state1, state2):
    """
      This function compares two State objects to see if they are equal to one another.
      The condition for equality regarding this function is the number of
      missionaries and cannibals on either bank, and the location of the boat.

      Parameters:
      state1 : The first State object to be compared.
      state2 : The Second State object to be compared.

      Returns:
      True if the two objects are equal, False otherwise.
    """
    if state1.cWest is not state2.cWest:
        return False
    if state1.cEast is not state2.cEast:
        return False
    if state1.mWest is not state2.mWest:
        return False
    if state1.mEast is not state2.mEast:
        return False
    if state1.boatloc is not state2.boatloc:
        return False

    return True


def find(states, state):
    """
      This function checks the given "states" list to see if there is a state in it
      that is equal to the given "state" parameter. The equality is checked by the is_equal() method.

      Parameters:
      states: The list of states that will be checked.
      state: The State object that the algorithm tries to find the equal of in the "states" list.

      Returns:
      The equal State object in states if there is any, None if not.
    """
    for s in states:
        if is_equal(s, state):
            return s

    return None


def move(state, to_east, visited):
    """
      This function is used during Non-Deterministic Search to get a list of all unvisited states
      that can be reached through the state provided by the "state" parameter.

      Parameters:
      state      : The State object whose next possible states will be calculated.
      to_east    : A Boolean that denotes whether or not the next states will have the boat on the
      east or west bank.
      visited    : A list of all states currently visited. This list is used to avoid loops.

      Returns:
      The list of states that are unvisited and can be reached by the "state" parameter.
    """
    # the first way we have avoided loops is by checking the "visited" list to make sure we
    # do not return any states that were visited before.

    result = []
    for boat_c in range(5, -1, -1):
        for boat_m in range(0, 5 - boat_c + 1):

            # the given loop can result in no people being taken into the boat.
            # this if statement below is to counter that.
            if boat_c + boat_m == 0:
                continue

            # if the boat would be unsafe with the current number of cannibals and missionaries,
            # do not consider this river crossing.
            if 0 < boat_m < boat_c:
                continue

            # calculate the new number of missionaries and cannibals on each side depending on boat load
            # and previous state.
            if to_east:
                newWestM = state.mWest - boat_m
                newWestC = state.cWest - boat_c
                newEastM = state.mEast + boat_m
                newEastC = state.cEast + boat_c
            else:
                newWestM = state.mWest + boat_m
                newWestC = state.cWest + boat_c
                newEastM = state.mEast - boat_m
                newEastC = state.cEast - boat_c

            # if any of the number of cannibals or missionaries are negative or greater than 6, this state
            # is unnatural, so we skip this state.
            if not (0 <= newWestM <= 6 and 0 <= newEastM <= 6 and 0 <= newWestC <= 6 and 0 <= newEastC <= 6):
                continue

            # similarly, if on any side the cannibals outnumber the missionaries,
            # this is an unsafe state, so we skip this state.
            elif 0 < newWestM < newWestC or 0 < newEastM < newEastC:
                continue

            else:
                if to_east:
                    new_dir = "east"
                else:
                    new_dir = "west"

                # we create a potentially new state, and check if such a state has been encountered before.
                new_state = State(newWestM, newWestC, newEastM, newEastC, new_dir)
                found = find(visited, new_state)
                if found is None:
                    # this means that this state has never been reached before. so, we add it to
                    # the list of states reachable by the current state.

                    result.append(new_state)
                # if the new state has been reached before, then we do not add it to the
                # list of states returned, to avoid loops in the solution.
    return result


def nd_search(start_state, goal_state, trace=False):
    """
      This function performs a non deterministic search algorithm on the start state
      to try and find a state equal to the goal state. Equality is again checked with the
      is_equal() method.

      Parameters:
      start_state : The State object that is the starting point for the algorithm.
      goal_state  : The State object representation that the algorithm aims to find.
      trace       : Whether or not the search algorithm will run on "single-stepping" mode.

      Returns:
      If the goal state is found, returns a list of states representing the path between the start and
      goal states.

      If the goal state could not be found, returns None.
    """
    # the queue is structured as follows: each member is a 2-tuple, whose second member
    # is a state, and the first member is the path that was used to reach that state.
    # with this structure, we can easily keep track of both the states and the solution path.
    queue = [([], start_state)]
    visited = []
    if trace:
        print("Single-stepping mode enabled. You will now be able to inspect each river-crossing used by the algorithm.")
    while len(queue) > 0:
        (current_path, current_state) = queue.pop(0)

        # this "if" block is to counteract any duplicates that might occur in the queue
        # due to the randomness of the non-deterministic search queue insertion.
        if find(visited, current_state) is not None:
            continue

        if trace:
            if len(current_path) > 0:
                prev = current_path[-1]
                curr = current_state
                print("------------------------------")
                print("State before crossing: ", end="")
                prev.lite_print()
                print("State after crossing: ", end="")
                curr.lite_print()

                if prev.boatloc == "west":
                    boat_c = abs(prev.cEast - curr.cEast)
                    boat_m = abs(prev.mEast - curr.mEast)
                else:
                    boat_c = abs(prev.cWest - curr.cWest)
                    boat_m = abs(prev.mWest - curr.mWest)

                print(f"{boat_m} missionaries and {boat_c} cannibals were moved to the {curr.boatloc} bank.")
                print("------------------------------")
                input("Press Enter to proceed to the next step.")

        # if the current state is the goal state, the search is stopped and the
        # solution path is returned.
        if is_equal(current_state, goal_state):
            current_path.append(current_state)
            return current_path  # announces success

        # if the current state is not the goal state, nor previously visited, then
        # we first append it to the visited list, and move on to inspect the states safely reachable by
        # the current state.
        visited.append(current_state)
        for next_state in move(current_state, current_state.boatloc == "west", visited):
            # if this next state was visited before, we ignore it. otherwise, we make a new 2-tuple
            # with the state as the second item and the path as the first item. then, we insert
            # this new tuple into a random spot in the queue.
            if find(visited, next_state) is None:
                new_tuple = (current_path + [current_state], next_state)
                queue.insert(random.randint(0, len(queue)), new_tuple)

    return None  # announces failure


def verbalize_path(path):
    """
      This function prints the list of river-crossings that eventually obtain the goal state.

      Parameters:
      path : The list of states returned by the nd_search function call.

      Returns:
      None
    """
    print("Initial:")
    print(f"West Bank: {path[0].mWest} missionaries and {path[0].cWest} cannibals")
    print(f"East Bank: {path[0].mEast} missionaries and {path[0].cEast} cannibals")
    for i in range(len(path) - 1):
        start = path[i]
        end = path[i + 1]
        # calculate how many cannibals and missionaries were carried with the boat this crossing.
        if start.boatloc == "west":
            boat_c = abs(start.cEast - end.cEast)
            boat_m = abs(start.mEast - end.mEast)
        else:
            boat_c = abs(start.cWest - end.cWest)
            boat_m = abs(start.mWest - end.mWest)

        # print the details of current crossing.
        print(f"{i + 1}) {boat_m} missionaries and {boat_c} cannibals are carried to the {end.boatloc} bank.")
        print(f"West Bank: {end.mWest} missionaries and {end.cWest} cannibals")
        print(f"East Bank: {end.mEast} missionaries and {end.cEast} cannibals")


if __name__ == "__main__":
    trace = False
    if "trace" in sys.argv:
        print("Single-stepping mode activated.")
        trace = True

    # construct the start state and the prototype of the goal state.

    # we call the goal state "prototype" because it is not the actual goal state, but it is a State object template
    # template of the goal state that the is_equal function can use to check if the current state is goal state.
    # Our non-deterministic search algorithm is still an uninformed search.
    start_state = State(6, 6, 0, 0, "west")

    goal_state = State(0, 0, 6, 6, "east")

    # run the non-deterministic search algorithm.
    path = nd_search(start_state, goal_state, trace)
    if path is None:
        print("not found")
        exit(1)

    # try to find a path that reaches the goal state on 7 river crossings.
    while len(path) > 8:
        if trace:
            print("The previous algorithm run did not yield a path of only 7 river crossings. "
                  "Would you like to try again?")
            user_input = input("Enter 'Y' if so, or anything else to display results of last run and exit.")
            if user_input != 'Y':
                break
        path = nd_search(start_state, goal_state, trace)

    # verbalize the river-crossings.
    print("------------------------------")
    print("The solution:")
    verbalize_path(path)
    exit(0)
