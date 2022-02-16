
# This is the submission of the project group named WATSON for Homework 6.

# Members:
#           Mehmet Berk Şahin (CONTACT)
#           Balaj Saleem
#           Mehmet Alper Genç
#           Ege Hakan Karaağaç
#           Fırat Yönak

'''
This program finds the class-precedence list (CPL) for a given class hierarchy. To find CPL,
"fish-hook algorithm" given by Winston (Chapter 9) was implemented. In order to implement the algorithm,
topological sorting given in Winston (Chapter 9) was implemented from the scratch.

Also, a proper CPL obeys two rules:
-Each class should appear on class-precedence list before any of its superclasses.
-Each direct superclass of a given class should appear on class-precedence lists before any other direct
superclass that is to its right.

Our topological-sorting algorithm obeys these two important rules.
'''


import copy

#Class Hierarchies

#Note: Each row is fish hook and each element of each row consists of item pair (first two elements)
#and the name of the node/hook (third element)

hooksForA = [[['Squares', 'Rectangles', 'Squares'], ['Rectangles', 'Rhombuses', 'Squares']],
             [['Rectangles', 'Isosceles Trapezoids', 'Rectangles'], ['Isosceles Trapezoids', 'Parallelograms', 'Rectangles']],
             [['Rhombuses', 'Parallelograms', 'Rhombuses'], ['Parallelograms', 'Kites', 'Rhombuses']],
             [['Isosceles Trapezoids', 'Cyclic Quadrilaterals', 'Isosceles Trapezoids'], ['Cyclic Quadrilaterals', 'Trapezoids', 'Isosceles Trapezoids']],
             [['Parallelograms', 'Trapezoids', 'Parallelograms']],
             [['Cyclic Quadrilaterals', 'Quadrilaterals', 'Cyclic Quadrilaterals']],
             [['Trapezoids', 'Quadrilaterals', 'Trapezoids']],
             [['Kites', 'Quadrilaterals', 'Kites']],
             [['Quadrilaterals', 'Everything', 'Quadrilaterals']]]

hooksForBIsosceles = [[['Isosceles Trapezoids', 'Trapezoids', 'Isosceles Trapezoids'], ['Trapezoids', 'Cyclic Quadrilaterals', 'Isosceles Trapezoids']],
                      [['Trapezoids', 'Quadrilaterals', 'Trapezoids']],
                      [['Cyclic Quadrilaterals', 'Quadrilaterals', 'Cyclic Quadrilaterals']],
                      [['Quadrilaterals', 'Everything', 'Quadrilaterals']]]

hooksForBSquares = [[['Squares', 'Rectangles', 'Squares'], ['Rectangles', 'Rhombuses', 'Squares']],
                    [['Rectangles', 'Cyclic Quadrilaterals', 'Rectangles'], ['Cyclic Quadrilaterals', 'Parallelograms', 'Rectangles']],
                    [['Rhombuses', 'Parallelograms', 'Rhombuses'], ['Parallelograms', 'Kites', 'Rhombuses']],
                    [['Cyclic Quadrilaterals', 'Quadrilaterals', 'Cyclic Quadrilaterals']],
                    [['Parallelograms', 'Quadrilaterals', 'Parallelograms']],
                    [['Kites', 'Quadrilaterals', 'Kites']],
                    [['Quadrilaterals', 'Everything','Quadrilaterals', 'Quadrilaterals']]]

hooksForCrazy = [[['Crazy', 'Professors', 'Crazy'], ['Professors', 'Hackers', 'Crazy']],
                [['Professors', 'Eccentrics', 'Professors'], [
                    'Eccentrics', 'Teachers', 'Professors']],
                [['Hackers', 'Eccentrics', 'Hackers'], [
                    'Eccentrics', 'Programmers', 'Hackers']],
                [['Eccentrics', 'Dwarfs', 'Eccentrics']],
                [['Teachers', 'Dwarfs', 'Teachers']],
                [['Programmers', 'Dwarfs', 'Programmers']],
                [['Dwarfs', 'Everything', 'Dwarfs']]]

hooksForJacque = [[['Jacque', 'Weightlifters', 'Jacque'], ['Weightlifters', 'Shotputters', 'Jacque'], ['Shotputters', 'Athletes', 'Jacque']],
                  [['Weightlifters', 'Athletes','Weightlifters'], ['Athletes', 'Endomorphs', 'Weightlifters']],
                  [['Athletes', 'Dwarfs', 'Athletes']],
                  [['Endomorphs', 'Dwarfs', 'Endomorphs']],
                  [['Dwarfs', 'Everything', 'Dwarfs']],
                  [['Shotputters', 'Athletes', 'Shotputters'], ['Athletes', 'Endomorphs', 'Shotputters']]]

def displayTable(hook_list, precList):
    '''

    This function takes two lists one consists of fish hooks and other one consists of classes sorted
    by their precedences. By using these parameters, this function displays a table similar to the table
    given in the example of Winston (Chapter 9).

    :param hook_list:
    :param precList:
    :return:

    '''
    print("----------------------------------------------")
    print("Node\t\t\t\tFish-hook Pairs")
    print("----------------------------------------------")
    for row in hook_list:
        if any(row):
            print("{:<15}".format(row[0][2]), end="\t\t\t")
            for pair in row:
                print("{:<20}".format(pair[0]+'-'+pair[1]), end=" ")
            print()
    print("----------------------------------------------")
    print("Class-precedence list (Highest to Lowest): ", end = " -")
    for preNode in precList:
        print(preNode, end = "-")
    if not any(hook_list):
        print("Everything", end = "-")
    print()
    print("-----------------------")


def topological_sorting(hook_list, precedenceList):

    '''

    This function takes hook list and an empty list as a precedence list and make the latter one a list
    of classes sorted by their precedences'. As a sorting algorithm, topological sorting was used.

    :param hook_list:
    :param precedenceList:
    :return:
    '''

    tempList = copy.deepcopy(hook_list) #make a copy of list

    #Until there is no pair in the list, continue to search
    while any(hook_list):
        counterExposedNodes = 0 #Counts exposed nodes
        exposedNodes = [] #List for exposed nodes

        #Loop that iterates through the list and takes the left-most value in the list
        for row in hook_list:
            for pair in row:
                checkEl = pair[0] #First node encountered in hierarchy list
                nodeCounter = 0
                containerList = [] #Keeps track of the locations of items
                checkContains = False #Indication for exposed item
                #At this part, program finds how many different type of exposed items there are and
                #it keeps track of the locations of the item being iterated
                for row2 in hook_list:
                    pairCounter = 0
                    for pair2 in row2:
                        if checkEl == pair2[0]:
                            containerList.append([nodeCounter, pairCounter])
                        if checkEl == pair2[1]:
                            checkContains = True
                            break
                        pairCounter += 1
                    if checkContains:
                        break
                    nodeCounter += 1
                if checkContains == False and containerList not in exposedNodes:
                    counterExposedNodes += 1
                    exposedNodes.append(containerList)

        if counterExposedNodes == 1: #If there is only one type of node was exposed, do the following
            precedenceList.append(
                hook_list[exposedNodes[0][0][0]][exposedNodes[0][0][1]][0]) #add the relevant node to CLP
            for conRow in exposedNodes:
                for conPair in conRow:
                    del hook_list[conPair[0]][conPair[1]] #delete the item pair from hierarchy/fish-hook pairs list

        elif counterExposedNodes > 1: #If various nodes were exposed, do the following
            #At this part, program does the necessary tie-breaker that is explained in Winston (Chapter 9) on p. 194.
            checkIfExpExists = False
            counterRemRow = 0
            for precNode in reversed(precedenceList):
                counterRemRow = 0
                for conRow in exposedNodes:
                    expNode = hook_list[conRow[0][0]][conRow[0][1]][0]
                    for row in tempList:
                        for pair in row:
                            if pair[2] == precNode and expNode == pair[1]:
                                checkIfExpExists = True
                                break
                        if checkIfExpExists:
                            break
                    if checkIfExpExists:
                        break
                    counterRemRow += 1
                if checkIfExpExists:
                    break
            precedenceList.append(
                hook_list[exposedNodes[counterRemRow][0][0]][exposedNodes[counterRemRow][0][1]][0])
            for delNodes in exposedNodes[counterRemRow]:
                del hook_list[delNodes[0]][delNodes[1]] #delete the the item pairs used
        #This part does the single-stepping for make the code easier to follow and debug
        print("Press any key to see fish-hook pairs and class precedence list...")
        input()
        displayTable(hook_list, precedenceList)

#Main Program
precList = []
print("Press any key to see fish-hook pairs and class precedence list...")
input()
#You can change the parameters from here manually
displayTable(hooksForBIsosceles, precList)
topological_sorting(hooksForBIsosceles, precList)
print("Class precedence list is completed")