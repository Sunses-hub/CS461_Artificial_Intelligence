import copy


# bilinen uzunlukla domain oluşturuluyor
def domainCreater(list_of_words, domainLength):
    domain = []

    for word in list_of_words:
        if len(word) == domainLength:
            domain.append(word)

    return domain  #


# parametre olarak temperory crossword giriliyor ve constraint listesi oluşturuluyor
def constraintCreater(crossword):
    constrain_list = []

    for row in range(0, 5):
        for column in range(0, 5):
            if crossword[row][column] == 0:
                constrain_list.append([row, column])

    return constrain_list


def consistencyCheck(constraintLoc, domainA, domainD):
    flag1 = False  # says if there is common element
    flag2 = False  # says if there is change in domain
    for word1 in domainA:
        for word2 in domainD:
            if word1[constraintLoc[0], constraintLoc[1]] == word2[constraintLoc[0], constraintLoc[1]]:
                flag1 = True

        if flag1 == False:
            domainA.remove(word1)
            flag2 = True
        else:
            flag1 = False

    return [domainA, flag2]


crossword = zeroes(5, 5)
locations = [[3, 5], [4, 5], [1, 5], [2, 5]]
list_of_words = []

for location in locations:
    crossword[location[0]][location[1]] = 1

crosswordT = crossword.transpose()

tempCrossword = copy.deepcopy(crossword)  # Yanlış olabilir

# Do the blackbox adjustment
for row in range(0, 5):
    for column in range(0, 5):
        # Check for row
        # Sadece 0 1 4 5 indexlerinin siyah kutu olabileceğini varsaydık
        if crossword[row][column] == 1 and row <= 1:
            tempCrossword[0][column] = 1
        elif crossword[row][column] == 1 and row >= 4:
            tempCrossword[5][column] = 1
        elif crossword[row][column] == 1 and column <= 1:
            tempCrossword[row][0] = 1
        elif crossword[row][column] == 1 and column >= 4:
            tempCrossword[row][5] = 1

# Create 10 Domain 5 Acsross and 5 Down
# For Accross Domains
dLengthA = []
for row in range(0, 5):
    for column in range(0, 5):
        if crossword[row].count(0) == 5:
            dLengthA.append(5)
        elif crossword[row].count(0) == 3:
            dLengthA.append(3)
        elif crossword[row].count(0) == 4:
            if crossword[row][1] == 1 or crossword[row][3] == 1:
                dLengthA.append(3)
            else:
                dLength.append(4)
# For Down Domains
dLengthD = []
for row in range(0, 5):
    for column in range(0, 5):
        if crosswordT[row].count(0) == 5:
            dLengthD.append(5)
        elif crosswordT[row].count(0) == 3:
            dLengthD.append(3)
        elif crosswordT[row].count(0) == 4:
            if crosswordT[row][1] == 1 or crosswordT[row][3] == 1:
                dLengthD.append(3)
            else:
                dLengthD.append(4)

dA1 = domainCreater(list_of_words, dLengthA[0])
dA2 = domainCreater(list_of_words, dLengthA[1])
dA3 = domainCreater(list_of_words, dLengthA[2])
dA4 = domainCreater(list_of_words, dLengthA[3])
dA5 = domainCreater(list_of_words, dLengthA[4])
dW1 = domainCreater(list_of_words, dLengthW[0])
dW2 = domainCreater(list_of_words, dLengthW[1])
dW3 = domainCreater(list_of_words, dLengthW[2])
dW4 = domainCreater(list_of_words, dLengthW[3])
dW5 = domainCreater(list_of_words, dLengthW[4])

domainListAccross = [[dA1, True], [dA2, True], [dA3, True], [dA4, True], [dA5, True]]
domainListDown = [[dW1, True], [dW2, True], [dW3, True], [dW4, True], [dW5, True]]

constrainList = constraintCreater(tempCrossword)

change = True

while change == True:

    change = False

    if domainListAccross[0][1] == True:  # DA1 has changed so need to
        domainListAccross[0][1] = False
        for constraint in constrainList:
            if constraint[0] == 0:  # if constraint is in 1st row
                check = consistencyCheck(constraint, domainListAccross[0][0],
                                         domainListDown[constraint[1]][0])  # if true, there is change
                domainListAccross[0][1] = check[1]
                if check[1]:
                    domainListDown[constraint[1]][1] = True
                    domainListAccross[0][0] = check[0]

    if domainListAccross[1][1] == True:  # DA2 has changed so need to
        domainListAccross[1][1] = False
        for constraint in constrainList:
            if constraint[0] == 1:
                check = consistencyCheck(constraint, domainListAccross[1][0],
                                         domainListDown[constraint[1]][0])  # if true, there is change
                domainListAccross[1][1] = check[1]
                if check[1]:
                    domainListDown[constraint[1]][1] = True
                    domainListAccross[1][0] = check[0]

    if domainListAccross[2][1] == True:  # DA3 has changed so need to
        domainListAccross[2][1] = False
        for constraint in constrainList:
            if constraint[0] == 2:
                check = consistencyCheck(constraint, domainListAccross[2][0],
                                         domainListDown[constraint[1]][0])  # if true, there is change
                domainListAccross[2][1] = check[1]
                if check[1]:
                    domainListDown[constraint[1]][1] = True
                    domainListAccross[2][0] = check[0]

    if domainListAccross[3][1] == True:  # DA4 has changed so need to
        domainListAccross[3][1] = False
        for constraint in constrainList:
            if constraint[0] == 3:
                check = consistencyCheck(constraint, domainListAccross[3][0],
                                         domainListDown[constraint[1]][0])  # if true, there is change
                domainListAccross[3][1] = check[1]
                if check[1]:
                    domainListDown[constraint[1]][1] = True
                    domainListAccross[3][0] = check[0]

    if domainListAccross[4][1] == True:  # DA5 has changed so need to
        domainListAccross[4][1] = False
        for constraint in constrainList:
            if constraint[0] == 4:
                check = consistencyCheck(constraint, domainListAccross[4][0],
                                         domainListDown[constraint[1]][0])  # if true, there is change
                domainListAccross[4][1] = check[1]
                if check[1]:
                    domainListDown[constraint[1]][1] = True
                    domainListAccross[4][0] = check[0]

    if domainListDown[0][1] == True:  # DW1 has changed so need to
        domainListDown[0][1] = False
        for constraint in constrainList:
            if constraint[1] == 0:
                check = consistencyCheck(constraint, domainListDown[0][0],
                                         domainListAccross[constraint[0]][0])  # if true, there is change
                domainListDown[0][1] = check[1]
                if check[1]:
                    domainListAccross[constraint[0]][1] = True
                    domainListDown[0][0] = check[0]

    if domainListDown[1][1] == True:  # DW2 has changed so need to
        domainListDown[1][1] = False
        for constraint in constrainList:
            if constraint[1] == 1:
                check = consistencyCheck(constraint, domainListDown[1][0],
                                         domainListAccross[constraint[0]][0])  # if true, there is change
                domainListDown[1][1] = check[1]
                if check[1]:
                    domainListAccross[constraint[0]][1] = True
                    domainListDown[1][0] = check[0]

    if domainListDown[2][1] == True:  # DW3 has changed so need to
        domainListDown[2][1] = False
        for constraint in constrainList:
            if constraint[1] == 2:
                check = consistencyCheck(constraint, domainListDown[2][0],
                                         domainListAccross[constraint[0]][0])  # if true, there is change
                domainListDown[2][1] = check[1]
                if check[1]:
                    domainListAccross[constraint[0]][1] = True
                    domainListDown[2][0] = check[0]

    if domainListDown[3][1] == True:  # DW4 has changed so need to
        domainListDown[3][1] = False
        for constraint in constrainList:
            if constraint[1] == 3:
                check = consistencyCheck(constraint, domainListDown[3][0],
                                         domainListAccross[constraint[0]][0])  # if true, there is change
                domainListDown[3][1] = check[1]
                if check[1]:
                    domainListAccross[constraint[0]][1] = True
                    domainListDown[3][0] = check[0]

    if domainListDown[4][1] == True:  # DW5 has changed so need to
        domainListDown[4][1] = False
        for constraint in constrainList:
            if constraint[1] == 4:
                check = consistencyCheck(constraint, domainListDown[4][0],
                                         domainListAccross[constraint[0]][0])  # if true, there is change
                domainListDown[4][1] = check[1]
                if check[1]:
                    domainListAccross[constraint[0]][1] = True
                    domainListDown[4][0] = check[0]

    for domain in domainListAccross:
        if domain[1] == True:
            change = True
            break

    if change:
        continue

    for domain in domainListDown:
        if domain[1] == True:
            change = True
            break

            break