# coding=utf-8
# This is the submission of the project group named WATSON for Homework 5.
# To run normally: python hw5.py

# Members:
#           Mehmet Berk Şahin (CONTACT)
#           Balaj Saleem
#           Mehmet Alper Genç
#           Ege Hakan Karaağaç
#           Fırat Yönak

'''
In this program BACKWARD CHAIN algorithm is implemented.

Until all hypotheses have been tried and none have been supported or until the
animal is identified program does the following for each hypotheses:

For each rule whose consequent matches the current hypothesis,

Try to support each of the rule's antecedents by matching it to assertions in working
memory or by backward chaining through another rule, creating new hypotheses. Program checks
all matching and instantiation alternatives.

If all the rule's antecedents are supported, program announces success and its concludes
that the hypothesis is true.
'''

'''
Our program follows the following rules, which are taken from ZOOKEEPER in WINSTON 

Z1      If   ?x has hair
        then ?x is a mammal

Z2      If   ?x gives milk 
        then ?x is a mammal

Z3      If   ?x has feathers 
        then ?x is a bird
   
Z4      If   ?x flies 
             ?x lays eggs
        then ?x is a bird
        
Z5      If   ?x is a mammal 
             ?x eats meat
        then ?x is a carnivore

Z6      If   ?x is a mammal 
             ?x has pointed teeth
             ?x has claws
             ?x has forward-pointing eyes
        then ?x is a carnivore

Z7      If   ?x is a mammal 
             ?x has hoofs
        then ?x is an ungulate
        
Z8      If   ?x is a mammal 
             ?x chews cud
        then ?x is an ungulate
        
Z9      If   ?x is a carnivore 
             ?x has tawny color
             ?x has dark spots
        then ?x is a cheetah
        
Z10     If   ?x is a carnivore 
             ?x has tawny color
             ?x has black strips
        then ?x is a tiger
        
Z11     If   ?x is a ungulate 
             ?x has long legs
             ?x has long neck
             ?x has tawny color
             ?x has dark spots
        then ?x is a giraffe
        
Z12     If   ?x is a ungulate 
             ?x has white color
             ?x has black stripes
        then ?x is a zebra

Z13     If   ?x is a bird 
             ?x does not fly
             ?x has long legs
             ?x has long neck
             ?x is black and white
        then ?x is an ostrich
        
Z14     If   ?x is a bird
             ?x does not fly
             ?x swims
             ?x is black and white
        then ?x is a penguin
        
Z15     If   ?x is a bird
             ?x is a good flyer
        then ?x is a albatross
        

'''


from PyQt5 import QtWidgets
import window
import sys


## SINGLE STEPPING VARIABLE - TOGGLE FOR SINGLE STEPPING ##
singleStep = True
###########################################################


class ContentWrapper:
    def __init__(self, content):
        self.content = content
        self.index = 0
    def getContent(self):
        if (self.index < len(self.content)):
            self.index = self.index + 1
            out = self.content[0:self.index]
            out = ' '.join(out)
            return  out
        else:
            out = ' '.join(self.content)
            return out
    def setContent(self, content):
        self.content = content
    
    def addContent(self, item):
        self.content.append(item)

output = []

ruleList = [
    "Z1: if ?x has hair,\n then ?x is a mammal\n", 

    "Z2: if ?x gives milk,\n then ?x is a mammal\n",

    "Z3: if ?x has feathers,\n then ?x is a bird\n",

    "Z4: if ?x flies,\n ?x lays eggs,\n then ?x is a bird\n",

    "Z5: if ?x eats meat,\n ?x is a mammal,\n then ?x is a carnivore\n",

    "Z6: if ?x has pointed teeth,\n ?x has claws ,\n ?x has forward-pointing eyes ,\n ?x is a mammal,\n then ?x is a carnivore\n",

    "Z7: if ?x has hoofs ,\n ?x is a mammal,\n then ?x is an ungulate\n",

    "Z8: if ?x chews cud ,\n ?x is a mammal,\n then ?x is an ungulate\n",

    "Z9: if ?x has tawny color ,\n ?x has dark spots ,\n ?x is a carnivore,\n then ?x is a cheetah\n",

    "Z10: if ?x has tawny color ,\n ?x has black stripes ,\n ?x is a carnivore,\n then ?x is a tiger\n",

    "Z11: if ?x has long legs ,\n ?x has a long neck ,\n ?x has a tawny color ,\n ?x has dark spots ,\n ?x is an ungulate,\n then ?x is a giraffe\n",

    "Z12: if ?x has white color ,\n ?x has black stripes ,\n ?x is an ungulate,\n then ?x is a zebra\n",

    "Z13: if ?x does not fly ,\n ?x has long legs ,\n ?x has a long neck ,\n ?x is black and white ,\n ?x is a bird,\n then ?x is an ostrich\n",

    "Z14: if ?x does not fly ,\n ?x swims ,\n ?x is black and white ,\n ?x is a bird,\n then ?x is a penguin\n",

    "Z15: if ?x is a good flyer ,\n ?x is a bird,\n then ?x is an albatross\n"

]

#These are rules specialized to ZOOKEEPER

def rules(ruleNo, workMem):
    check = 0
    #STEP-BY-STEP
    checks = []
    output.append("\n")
    output.append("Working Memory:")
    for assertion in workMem:
        output.append(assertion)
    output.append("\n")
    output.append("Rule is Z" + str(ruleNo))


    if ruleNo == 1:
        checks = ["?x has hair"]
        output.append("?x has hair")
        for feature in workMem:
            if feature == "?x has hair":
                checks.remove("?x has hair")
                check += 1
        if check == 1:
            return 2
        output.append("---------")
        output.append("Hypothesis Disproved. Wrong Assertion(s): ")
        for val in checks:
            output.append(val)
        output.append("---------")
        return 0

    elif ruleNo == 2:
        output.append("?x gives milk")
        for feature in workMem:
            if feature == "?x gives milk":
                check += 1
        if check == 1:
            return 2
        return 0

    elif ruleNo == 3:
        output.append("?x has feathers")
        for feature in workMem:
            if feature == "?x has feathers":
                check += 1
        if check == 1:
            return 2
        return 0

    elif ruleNo == 4:
        checks = ["?x flies", "?x lays eggs"]
        output.append("?x flies")
        output.append("?x lays eggs")
        for feature in workMem:
            if feature == "?x flies":
                check += 1
                checks.remove("?x flies")
            elif feature == "?x lays eggs":
                check += 1
                checks.remove("?x lays eggs")
        if check == 2:
            return 2
        output.append("---------")
        output.append("Hypothesis Disproved. Wrong Assertion(s): ")
        for val in checks:
            output.append(val)
        output.append("---------")
        return 0

    elif ruleNo == 5:
        mammalCheck = False
        output.append("?x eats meat")
        output.append("?x is a mammal")
        for feature in workMem:
            if feature == "?x eats meat":
                check += 1
            elif feature == "?x is a mammal":
                mammalCheck = True
        if check == 1:
            if mammalCheck:
                return 2
            return 1
        return 0

    elif ruleNo == 6:
        mammalCheck = False
        checks = ["?x has pointed teeth", "?x has claws", "?x has forward-pointing eyes"]
        output.append("?x has pointed teeth")
        output.append("?x has claws")
        output.append("?x has forward-pointing eyes")
        output.append("?x is a mammal")
        for feature in workMem:
            if feature == "?x has pointed teeth":
                check += 1
                checks.remove("?x has pointed teeth")
            elif feature == "?x has claws":
                check += 1
                checks.remove("?x has claws")
            elif feature == "?x has forward-pointing eyes":
                check += 1
                checks.remove("?x has forward-pointing eyes")
            elif feature == "?x is a mammal":
                mammalCheck = True
        if check == 3:
            if mammalCheck:
                return 2
            return 1
        output.append("---------")
        output.append("Hypothesis Disproved. Wrong Assertion(s): ")
        for val in checks:
            output.append(val)
        output.append("---------")
        return 0

    elif ruleNo == 7:
        mammalCheck = False
        output.append("?x has hoofs")
        output.append("?x is a mammal")
        for feature in workMem:
            if feature == "?x has hoofs":
                check += 1
            elif feature == "?x is a mammal":
                mammalCheck = True
        if check == 1:
            if mammalCheck:
                return 2
            return 1
        return 0

    elif ruleNo == 8:
        mammalCheck = False
        checks = ["?x chews cud"]
        output.append("?x chews cud")
        output.append("?x is a mammal")
        for feature in workMem:
            if feature == "?x chews cud":
                check += 1
                checks.remove("?x chews cud")
            elif feature == "?x is a mammal":
                mammalCheck = True
        if check == 1:
            if mammalCheck:
                return 2
            return 1
        output.append("---------")
        output.append("Hypothesis Disproved. Wrong Assertion(s): ")
        for val in checks:
            output.append(val)
        output.append("---------")
        return 0

    elif ruleNo == 9:
        carnivoreCheck = False
        checks = ["?x has tawny color", "?x has dark spots"]
        output.append("?x has tawny color")
        output.append("?x has dark spots")
        output.append("?x is a carnivore")
        for feature in workMem:
            if feature == "?x has tawny color":
                check += 1
                checks.remove("?x has tawny color")
            elif feature == "?x has dark spots":
                check += 1
                checks.remove("?x has dark spots")
            elif feature == "?x is a carnivore":
                carnivoreCheck = True
        if check == 2:
            if carnivoreCheck:
                return 2
            return 1
        output.append("---------")
        output.append("Hypothesis Disproved. Wrong Assertion(s): ")
        for val in checks:
            output.append(val)
        output.append("---------")
        return 0

    elif ruleNo == 10:
        carnivoreCheck = False
        checks = ["?x has tawny color", "?x has black stripes"]
        output.append("?x has tawny color")
        output.append("?x has black stripes")
        output.append("?x is a carnivore")
        for feature in workMem:
            if feature == "?x has tawny color":
                check += 1
                checks.remove("?x has tawny color")
            elif feature == "?x has black stripes":
                check += 1
                checks.remove("?x has black stripes")
            elif feature == "?x is a carnivore":
                carnivoreCheck = True
        if check == 2:
            if carnivoreCheck:
                return 2
            return 1
        output.append("---------")
        output.append("Hypothesis Disproved. Wrong Assertion(s): ")
        for val in checks:
            output.append(val)
        output.append("---------")
        return 0


    elif ruleNo == 11:
        ungulateCheck = False
        checks = ["?x has long legs", "?x has a long neck", "?x has tawny color", "?x has dark spots"]
        output.append("?x has long legs")
        output.append("?x has a long neck")
        output.append("?x has a tawny color")
        output.append("?x has dark spots")
        output.append("?x is an ungulate")
        for feature in workMem:
            if feature == "?x has long legs":
                check += 1
                checks.remove("?x has long legs")
            elif feature == "?x has a long neck":
                check += 1
                checks.remove("?x has a long neck")
            elif feature == "?x has tawny color":
                check += 1
                checks.remove("?x has tawny color")
            elif feature == "?x has dark spots":
                check += 1
                checks.remove("?x has dark spots")
            elif feature == "?x is an ungulate":
                ungulateCheck = True
        if check == 4:
            if ungulateCheck:
                return 2
            return 1
        output.append("---------")
        output.append("Hypothesis Disproved. Wrong Assertion(s): ")
        for val in checks:
            output.append(val)
        output.append("---------")
        return 0

    elif ruleNo == 12:
        ungulateCheck = False
        checks = ["?x has white color", "?x has black stripes"]
        output.append("?x has white color")
        output.append("?x has black stripes")
        output.append("?x is an ungulate")
        for feature in workMem:
            if feature == "?x has white color":
                check += 1
                checks.remove("?x has white color")
            elif feature == "?x has black stripes":
                check += 1
                checks.remove("?x has black stripes")
            elif feature == "?x is an ungulate":
                ungulateCheck = True
        if check == 2:
            if ungulateCheck:
                return 2
            return 1
        output.append("---------")
        output.append("Hypothesis Disproved. Wrong Assertion(s): ")
        for val in checks:
            output.append(val)
        output.append("---------")
        return 0

    elif ruleNo == 13:
        birdCheck = False
        checks = ["?x does not fly", "?x has long legs", "?x is black and white", "?x has a long neck"]
        output.append("?x does not fly")
        output.append("?x has long legs")
        output.append("?x has a long neck")
        output.append("?x is black and white")
        output.append("?x is a bird")
        for feature in workMem:
            if feature == "?x does not fly":
                check += 1
                checks.remove("?x does not fly")
            elif feature == "?x has long legs":
                check += 1
                checks.remove("?x has long legs")
            elif feature == "?x has a long neck":
                check += 1
                checks.remove("?x has a long neck")
            elif feature == "?x is black and white":
                check += 1
                checks.remove("?x is black and white")
            elif feature == "?x is a bird":
                birdCheck = True
        if check == 4:
            if birdCheck:
                return 2
            return 1
        output.append("---------")
        output.append("Hypothesis Disproved. Wrong Assertion(s): ")
        for val in checks:
            output.append(val)
        output.append("---------")
        return 0

    elif ruleNo == 14:
        birdCheck = False
        checks = ["?x does not fly", "?x swims", "?x is black and white"]
        output.append("?x does not fly")
        output.append("?x swims")
        output.append("?x is black and white")
        output.append("?x is a bird")
        for feature in workMem:
            if feature == "?x does not fly":
                check += 1
                checks.remove("?x does not fly")
            elif feature == "?x swims":
                check += 1
                checks.remove("?x swims")
            elif feature == "?x is black and white":
                check += 1
                checks.remove("?x is black and white")
            elif feature == "?x is a bird":
                birdCheck = True
        if check == 3:
            if birdCheck:
                return 2
            return 1

        output.append("---------")
        output.append("Hypothesis Disproved. Wrong Assertion(s): ")
        for val in checks:
            output.append(val)
        output.append("---------")
        return 0

    elif ruleNo == 15:
        checks = ["?x is a good flyer"]
        birdCheck = False
        output.append("?x is a good flyer")
        output.append("?x is a bird")
        for feature in workMem:
            if feature == "?x is a good flyer":
                check += 1
                checks.remove("?x is a good flyer")
            elif feature == "?x is a bird":
                birdCheck = True
        if check == 1:
            if birdCheck:
                return 2
            return 1
        output.append("---------")
        output.append("Hypothesis Disproved. Wrong Assertion(s): ")
        for val in checks:
            output.append(val)
        output.append("---------")
        return 0

#Animals specific to ZOOKEEPER scenario

#test cheetah hypothesis
def cheetah(workMem):
    rule9 = rules(9, workMem)
    if rule9 != 0:
        if rule9 == 1:
            rule5 = rules(5, workMem)
            if rule5 != 0:
                if rule5 == 1:
                    if rules(2, workMem) == 2 or rules(1, workMem) == 2:
                        return True
                    else:
                        rule6 = rules(6, workMem)
                        if rule6 != 0:
                            if rule6 == 2:
                                return True
                            elif rule6 == 1:
                                if rules(2, workMem) == 2:
                                    return True
                                elif rules(1, workMem) == 2:
                                    return True
                                else:
                                    return False
                        else:
                            return False
                elif rule5 == 2:
                    return True
            else:
                rule6 = rules(6, workMem)
                if rule6 != 0:
                    if rule6 == 2:
                        return True
                    elif rule6 == 1:
                        if rules(2, workMem) == 2:
                            return True
                        elif rules(1, workMem) == 2:
                            return True
                        else:
                            return False
                else:
                    return False
        elif rule9 == 2:
            return True
    else:
        return False

#test tiger hypothesis
def tiger(workMem):
    rule10 = rules(10, workMem)
    if rule10 != 0:
        if rule10 == 1:
            rule5 = rules(5, workMem)
            if rule5 != 0:
                if rule5 == 1:
                    if rules(2, workMem) == 2 or rules(1, workMem) == 2:
                        return True
                    else:
                        rule6 = rules(6, workMem)
                        if rule6 != 0:
                            if rule6 == 2:
                                return True
                            elif rule6 == 1:
                                if rules(2, workMem) == 2:
                                    return True
                                elif rules(1, workMem) == 2:
                                    return True
                                else:
                                    return False
                        else:
                            return False
                elif rule5 == 2:
                    return True
            else:
                rule6 = rules(6, workMem)
                if rule6 != 0:
                    if rule6 == 2:
                        return True
                    elif rule6 == 1:
                        if rules(2, workMem) == 2:
                            return True
                        elif rules(1, workMem) == 2:
                            return True
                        else:
                            return False
                else:
                    return False
        elif rule10 == 2:
            return True
    else:
        return False

#test giraffe hypothesis
def giraffe(workMem):
    rule11 = rules(11, workMem)
    if rule11 != 0:
        if rule11 == 1:
            rule7 = rules(7, workMem)
            if rule7 != 0:
                if rule7 == 1:
                    if rules(2, workMem) == 2 or rules(1, workMem) == 2:
                        return True
                    else:
                        rule8 = rules(8, workMem)
                        if rule8 != 0:
                            if rule8== 2:
                                return True
                            elif rule8 == 1:
                                if rules(2, workMem) == 2:
                                    return True
                                elif rules(1, workMem) == 2:
                                    return True
                                else:
                                    return False
                        else:
                            return False
                elif rule7 == 2:
                    return True
            else:
                rule8 = rules(8, workMem)
                if rule8 != 0:
                    if rule8 == 2:
                        return True
                    elif rule8 == 1:
                        if rules(2, workMem) == 2:
                            return True
                        elif rules(1, workMem) == 2:
                            return True
                        else:
                            return False
                else:
                    return False
        elif rule11 == 2:
            return True
    else:
        return False

#test zebra hypothesis
def zebra (workMem):
    rule12 = rules(12, workMem)
    if rule12 != 0:
        if rule12 == 1:
            rule7 = rules(7, workMem)
            if rule7 != 0:
                if rule7 == 1:
                    if rules(2, workMem) == 2 or rules(1, workMem) == 2:
                        return True
                    else:
                        rule8 = rules(8, workMem)
                        if rule8 == 1:
                            if rules(2, workMem) == 2:
                                return True
                            elif rules(1, workMem) == 2:
                                return True
                            else:
                                return False
                        else:
                            return False
                elif rule7 == 2:
                    return True
            else:
                rule8 = rules(8, workMem)
                if rule8 != 0:
                    if rule8 == 2:
                        return True
                    elif rule8 == 1:
                        if rules(2, workMem) == 2:
                            return True
                        elif rules(1, workMem) == 2:
                            return True
                        else:
                            return False
                else:
                    return False
        elif rule12 == 2:
            return True
    else:
        return False

#test ostrich hypothesis
def ostrich(workMem):
    rule13 = rules(13, workMem)
    if rule13 != 0:
        if rule13 == 1:
            if rules(3, workMem) == 2:
                return True
            elif rules(4, workMem) == 2:
                return True
            else:
                return False
        elif rules(12, workMem) == 2:
            return True
    else:
        return False

#test penguin hypothesis
def penguin(workMem):
    rule14 = rules(14, workMem)
    if rule14 != 0:
        if rule14 == 1:
            if rules(3, workMem) == 2:
                return True
            elif rules(4, workMem) == 2:
                return True
            else:
                return False
        elif rule14 == 2:
            return True
    else:
        return False

#test albatross hypothesis
def albatross(workMem):
    rule15 = rules(15, workMem)
    if rule15 != 0:
        if rule15 == 1:
            if rules(3, workMem) == 2:
                return True
            elif rules(4, workMem) == 2:
                return True
            else:
                return False
        elif rule15 == 2:
            return True
    else:
        return False



#Here is the working memory, you can put any assertion as you want from ZOOKEEPER
# workMem = [
#     "?x has hair",
#     "?x chews cud",
#     "?x has long legs",
#     "?x has a long neck",
#     "?x has tawny color",
#     "?x has dark spots",
# ]
#(Giraffe)

# workMem = [
#     "Bellus flies",
#     "Bellus lays eggs",
#     "Bellus is a good flyer",
# ]
# (Albatross)
# workMem = [
#     "Parvus gives milk",
#     "Parvus has hoofs",
#     "Parvus has black stripes",
#     "Parvus has white color",
# ]
# (Zebra)
# workMem = [
#      "Swifty has pointed teeth",
#      "Swifty has claws",
#      "Swifty has forward-pointing eyes",
#      "Swifty has hair",
#      "Swifty has tawny color",
#      "Swifty has dark spots",
               
#]
# (Book example, cheetah)
# workMem = [
#     "Bellus has feathers",
#     "Bellus does not fly",
#     "Bellus has long legs",
#     "Bellus is black and white",
#     "Bellus has a long neck",
# ]
# 
# (Ostrich)

workMem = [
    "Splashy has feathers.",
    "Splashy lays eggs.",
    "Splashy swims.",
    "Splashy does not fly.",
    "Splashy is black and white.",
    "Splashy has tawny color.",
]
# (Penguin)

#cleans up the WorkMem
for i in range(len(workMem)):
    s = workMem[i]
    s = s.replace('.', '')
    replacement = '?x'
    s = s.split()
    s[0] = replacement
    workMem[i] = ' '.join(s)

for assertion in workMem:
        output.append(assertion)

#Create and test hypotheses, then display the result.
hypothesis_verified = False

output.append("\nHypothesis is '?x is an albatross'")
workMem.append("?x is an albatross")
if albatross(workMem):
    output.append("Hypothesis Verified!\n?x is an albatross")
    hypothesis_verified = True
else:
    workMem.remove("?x is an albatross")

if not hypothesis_verified:
    output.append("Hypothesis is '?x is a penguin'")
    workMem.append("?x is a penguin")
    if penguin(workMem):
        output.append("Hypothesis Verified!\n?x is a penguin")
        hypothesis_verified = True
    else:
        workMem.remove("?x is a penguin")

if not hypothesis_verified:
    output.append("Hypothesis is '?x is an ostrich'")
    workMem.append("?x is an ostrich")
    if ostrich(workMem):
        output.append("Hypothesis Verified!\n?x is an ostrich")
        hypothesis_verified = True
    else:
        workMem.remove("?x is an ostrich")

if not hypothesis_verified:
    output.append("Hypothesis is '?x is a zebra'")
    workMem.append("?x is a zebra")
    if zebra(workMem):
        output.append("Hypothesis Verified!\n?x is a zebra")
        hypothesis_verified = True
    else:
        workMem.remove("?x is a zebra")

if not hypothesis_verified:
    output.append("Hypothesis is '?x is a giraffe'")
    workMem.append("?x is a giraffe")
    if giraffe(workMem):
        output.append("Hypothesis Verified!\n?x is a giraffe")
        hypothesis_verified = True
    else:
        workMem.remove("?x is a giraffe")

if not hypothesis_verified:
    output.append("Hypothesis is '?x is a tiger'")
    workMem.append("?x is a tiger")
    if tiger(workMem):
        output.append("Hypothesis Verified!\n?x is a tiger")
        hypothesis_verified = True
    else:
        workMem.remove("?x is a tiger")

if not hypothesis_verified:
    output.append("Hypothesis is '?x is a cheetah'")
    workMem.append("?x is a cheetah")
    if cheetah(workMem):
        output.append("Hypothesis Verified!\n?x is a cheetah")
        hypothesis_verified = True
    else:
        workMem.remove("?x is a cheetah")

if not hypothesis_verified:
    output.append("\nThe animal could not be identified.")
    output.append("\n ")
    output.append("Working Memory:")
    for assertion in workMem:
        output.append(assertion)


sep = "\n"
rulesString = sep.join(ruleList)
memString = sep.join(workMem)
outString = sep.join(output)
splitIndexes = [i for i, j in enumerate(output) if j == '---------']
dividedOutput = [output[i:j] for i, j in zip([0]+splitIndexes, splitIndexes)] 
dividedOutput.append(output[splitIndexes[-1]: (len(output) + 1)  ])
print(outString)
print(len(dividedOutput))

app = QtWidgets.QApplication(sys.argv)
MainWindow1 = QtWidgets.QMainWindow()
MainWindow2 = QtWidgets.QMainWindow()
ui = window.Ui_MainWindow()
ui2 = window.Ui_MainWindow()
c1 = ContentWrapper(["RULES LIST: \n" + rulesString])
c2 = ContentWrapper(["Working Memory: " ])
ui.setupUi(MainWindow1, "Rules", c1)
ui2.setupUi(MainWindow2, "Working Memory", c2, ui.refresh)
MainWindow1.show()
MainWindow2.show()
print("Displaying application UI. (TWO WINDOWS)")
print("----- PLEASE PRESS REFRESH -----.")



if(singleStep):
    for s in dividedOutput:
        out = sep.join(s)
        c2.addContent(out)
else:
    c2.addContent(outString)
        

app.exec_()
print("UI window closed. Program will now exit.")
