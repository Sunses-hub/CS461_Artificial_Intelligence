# Crossword.py

from typing import List, Dict
from WikiPediaScrapper import Crawler
from Tile import Tile
import copy

class Word:
    def __init__(self, x, y, num, word_length, clue, direction):
        self.word_length = word_length
        self.crossword_y = y
        self.crossword_x = x
        self.number = num
        self.clue = clue
        self.domain = []
        self.domainChanged = True
        self.direction = direction



class Constraint:
    def __init__(self, w1, w1i, w2, w2i):
        self.word1 = w1
        self.word1index = w1i
        self.word2 = w2
        self.word2index = w2i


class Crossword:
    def __init__(self, tile_grid: List[List[Tile]], across_clues: Dict[int, str], down_clues: Dict[int, str]):
        self.tile_grid = tile_grid
        self.across_clues = across_clues
        self.down_clues = down_clues
        self.across_word_objects: Dict[int, Word] = dict()
        self.down_word_objects: Dict[int, Word] = dict()
        self.constraints: List[Constraint] = []
        self.steps = []

    def find_domains(self):
        cw = Crawler()
        for item in self.across_word_objects.values():
            item.domain = cw.scrape(item.clue, item.word_length)
            print("Domain received for a", item.number, sep="")
            print(item.domain)

        for item in self.down_word_objects.values():
            item.domain = cw.scrape(item.clue, item.word_length)
            print("Domain received for d", item.number, sep="")
            print(item.domain)

    def find_words(self):
        across_word_objects = dict()
        down_word_objects = dict()
        for i in range(len(self.tile_grid)):
            for j in range(len(self.tile_grid[0])):
                if self.tile_grid[i][j].number is not None:
                    if ((i == 0 or self.tile_grid[i - 1][j].black)
                            and i != len(self.tile_grid) - 1
                            and not self.tile_grid[i + 1][j].black):
                        word_length = self.find_down_word_length(j, i)
                        down_word_objects[self.tile_grid[i][j].number] = Word(j, i, self.tile_grid[i][j].number,
                                                                              word_length, self.down_clues[
                                                                                  self.tile_grid[i][j].number], "down")

                    if ((j == 0 or self.tile_grid[i][j - 1].black)
                            and j != len(self.tile_grid[0]) - 1
                            and not self.tile_grid[i][j + 1].black):
                        word_length = self.find_across_word_length(j, i)
                        across_word_objects[self.tile_grid[i][j].number] = Word(j, i, self.tile_grid[i][j].number,
                                                                                word_length, self.across_clues[
                                                                                    self.tile_grid[i][j].number], "across")

        print("ACROSS WORDS:")
        for item in across_word_objects.keys():
            print(across_word_objects[item].__dict__)

        print("DOWN WORDS:")
        for item in down_word_objects.keys():
            print(down_word_objects[item].__dict__)

        self.across_word_objects = across_word_objects
        self.down_word_objects = down_word_objects

    def find_constraints(self):
        if len(self.across_word_objects) == 0:
            print("Please find the words of the puzzle first.")

        search_points = [(item, item.crossword_x, item.crossword_y) for item in self.across_word_objects.values()]
        constraints: List[Constraint] = []

        for (word, x, y) in search_points:
            length = word.word_length
            # for each across word, examine each block from left to right.
            for i in range(x, x + length):
                # for each block, go up until you reach a block with a number. once that is found, add a constraint.
                consnum = None
                j = 0
                for j in range(y, -1, -1):
                    if self.tile_grid[j][i].black:
                        j += 1
                        break
                    if self.tile_grid[j][i].number is not None:
                        consnum = self.tile_grid[j][i].number

                if consnum is not None:
                    new_cons = Constraint(word, i - x, self.down_word_objects[consnum], y - j)
                    constraints.append(new_cons)

        print("CONSTRAINTS:")
        for item in constraints:
            print("a", item.word1.number, "[", item.word1index, "] = d", item.word2.number, "[", item.word2index, "]",
                  sep="")

        self.constraints = constraints

    def consistency_check(self):
        print("entered consistency check")
        change = True
        while change:
            #print("loop 1")
            change = False
            self.constraints.sort(key=lambda x: x.word1.number)
            for constraint in self.constraints:
                #if constraint.word1.domainChanged:
                result = self.check_for_constraint(constraint, 0)
                if result:
                    change = True
            self.constraints.sort(key=lambda x: x.word2.number)
            for constraint in self.constraints:
                #if constraint.word2.domainChanged:
                result = self.check_for_constraint(constraint, 1)
                if result:
                    change = True
        for item in self.across_word_objects.values():
            print("a", item.number, " domain: ", item.domain, sep="")
            print("Number of Words: ", len(item.domain))
        for item in self.down_word_objects.values():
            print("d", item.number, " domain: ", item.domain, sep="")
            print("Number of Words: ", len(item.domain))

    def check_for_constraint(self, constraint, side):
        if side == 0:
            changeWord = constraint.word1
            changeWordIndex = constraint.word1index
            checkWord = constraint.word2
            checkWordIndex = constraint.word2index
        else:
            changeWord = constraint.word2
            changeWordIndex = constraint.word2index
            checkWord = constraint.word1
            checkWordIndex = constraint.word1index

        if len(checkWord.domain) == 0:
            return False

        domainChanged = False

        for word in changeWord.domain:
            #print("checking word")
            found = False
            for check in checkWord.domain:
                if word[changeWordIndex] == check[checkWordIndex]:
                    found = True
                    break

            if not found:
                print(word, "is removed from", changeWord.direction, changeWord.number)
                self.steps.append(str(word) + " is removed from " + str(changeWord.direction) + str(changeWord.number))
                changeWord.domain.remove(word)
                domainChanged = True

        changeWord.domainChanged = domainChanged

        return domainChanged

    def constraint_dfs(self):
        precedence_list = [*self.across_word_objects.values()] + [*self.down_word_objects.values()]
        nonemptycount = 0
        for item in precedence_list:
            if(len(item.domain) > 0):
                nonemptycount += 1

        current_max = 0
        current_max_count = 0
        queue = [(dict(), precedence_list[0])]
        # queue entry structure = (word choices = dict(word, choice), current word)

        while len(queue) > 0:
            word_choices, current_word = queue.pop(0)

            error = False
            # if any of the current word choices conflict a constraint, disregard this solution.
            for constraint in self.constraints:
                if constraint.word1 in word_choices.keys() and constraint.word2 in word_choices.keys():
                    if word_choices[constraint.word1][constraint.word1index] != word_choices[constraint.word2][constraint.word2index]:
                        error = True
                        break

            if(error):
                continue


            if len(word_choices) == nonemptycount:
                current_max = word_choices
                break
            elif len(word_choices) > current_max_count:
                current_max = word_choices
                current_max_count = len(word_choices)

            if precedence_list.index(current_word) == len(precedence_list) - 1:
                continue

            # if the word's domain is empty, just skip it.
            if len(current_word.domain) == 0:
                currentIndex = precedence_list.index(current_word)
                queue.insert(0, (word_choices, precedence_list[currentIndex + 1]))
                continue

            # for each word in current_word's domain, add it to the dictionary as a word choice
            for word_string in current_word.domain:
                currentIndex = precedence_list.index(current_word)
                new_dict = copy.deepcopy(word_choices)
                new_dict[current_word] = word_string
                queue.insert(0, (new_dict, precedence_list[currentIndex + 1]))


        answer_grid = copy.deepcopy(self.tile_grid)
        for i in range(5):
            for j in range(5):
                if not answer_grid[i][j].black:
                    answer_grid[i][j].letter = ""

        for word in current_max.keys():
            if word.direction == "across":
                self.fill_word_across(word, current_max[word], answer_grid)
            else:
                self.fill_word_down(word, current_max[word], answer_grid)

        return answer_grid, self.steps

    def find_across_word_length(self, x, y):
        length = 0
        for i in range(x, len(self.tile_grid[0])):
            if not self.tile_grid[y][i].black:
                length += 1
            else:
                return length

        return length

    def find_down_word_length(self, x, y):
        length = 0
        for i in range(y, len(self.tile_grid)):
            if not self.tile_grid[i][x].black:
                length += 1
            else:
                return length

        return length

    def fill_word_across(self, word_obj: Word, word_str: str, answer_grid: List[List[Tile]]):
        start_x = word_obj.crossword_x
        start_y = word_obj.crossword_y

        for x in range(start_x, start_x + word_obj.word_length):
            answer_grid[start_y][x].letter = word_str[x - start_x].upper()

    def fill_word_down(self, word_obj: Word, word_str: str, answer_grid: List[List[Tile]]):
        start_x = word_obj.crossword_x
        start_y = word_obj.crossword_y

        for y in range(start_y, start_y + word_obj.word_length):
            answer_grid[y][start_x].letter = word_str[y - start_y].upper()

# JSONTileGridParser.py

import json
import re
from Tile import Tile

SQUARE_GRID_LENGTH = 5
class JSONTileGridParser:
    def __init__(self, filepath):
        self.filepath = filepath

    def parse(self):
        with open(self.filepath) as file:
            jsonstr = file.read()

            puzzle = json.loads(jsonstr)
            tile_grid = []
            answer_tile_grid = []

            for i in range(SQUARE_GRID_LENGTH):
                new_empty_row = []
                new_row = []
                for j in range(SQUARE_GRID_LENGTH):

                    jsontile = puzzle["grid"][i][j]
                    if jsontile["number"] is None:
                        number = None
                    else:
                        number = int(jsontile["number"])

                    if jsontile["black"]:
                        new_empty_tile = Tile(jsontile["letter"], number)
                    else:
                        new_empty_tile = Tile("0", number)
                    new_tile = Tile(jsontile["letter"], number)
                    new_empty_row.append(new_empty_tile)
                    new_row.append(new_tile)
                tile_grid.append(new_empty_row)
                answer_tile_grid.append(new_row)

            across_clues = dict()
            down_clues = dict()

            for item in puzzle["across_clues"]:
                search = re.search(r"([0-9]+)\) (.+)", item)
                number = int(search.group(1))
                clue = search.group(2)
                across_clues[number] = clue

            for item in puzzle["down_clues"]:
                search = re.search(r"([0-9]+)\) (.+)", item)
                number = int(search.group(1))
                clue = search.group(2)
                down_clues[number] = clue

            return tile_grid, answer_tile_grid, across_clues, down_clues, puzzle["across_clues"], puzzle["down_clues"]


if __name__ == "__main__":
    js = JSONTileGridParser("2021-04-14.json")

    (tile_grid, answer_tile_grid, across_clues, down_clues) = js.parse()
    print(tile_grid)
    print(answer_tile_grid)
    print(across_clues)
    print(down_clues)

# below code was added to main.py of demo 1 to make it work

cw = Crossword(tile_grid, acrossCluesDict, downCluesDict)
cw.find_words()
cw.find_constraints()
cw.find_domains()
cw.consistency_check()
tile_grid, steps = cw.constraint_dfs()


# WikiPediaScrapper.py

# from urllib.request import urlopen as uReq
# from bs4 import BeautifulSoup as soup
#
# metro_url = 'https://metro-online.pk/category/frozen-food/frozen-ready-to-cook'
# user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
# headers = {'User-Agent':user_agent}
# uClient = uReq(metro_url)
# uClient.add_header=headers
# metro_html = uClient.read()
# uClient.close()
# page_soup = soup(metro_html, 'html.parser')
# print(page_soup.h1)
#
#


# import urllib.request
# from bs4 import BeautifulSoup as soup
# user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
#
# url = "https://metro-online.pk/category/frozen-food/frozen-ready-to-cook"
# headers={'User-Agent':user_agent,}
#
# request = urllib.request.Request(url,None,headers) #The assembled request
# response = urllib.request.urlopen(request)
# data = response.read() # The data u need
# response.close()
# page_soup = soup(data, 'html.parser')
# items = page_soup.findAll("div",{"class":"productdivinner"})
# print(items)

import time
import csv
import threading
import re
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Crawler:
    url = ""

    driver = webdriver

    def __init__(self,
                 url="https://en.wikipedia.org/w/index.php?title=Special%3ASearch&profile=advanced&fulltext=1&ns0=1&ns1=1&ns2=1&ns3=1&ns4=1&ns5=1&ns6=1&ns7=1&ns8=1&ns9=1&ns10=1&ns11=1&ns12=1&ns13=1&ns14=1&ns15=1&ns100=1&ns101=1&ns108=1&ns109=1&ns118=1&ns119=1&ns446=1&ns447=1&ns710=1&ns711=1&ns828=1&ns829=1&ns2300=1&ns2301=1&ns2302=1&ns2303=1&search="):
        self.driver = webdriver.Chrome("/Users/berksahin/PycharmProjects/pythonProject6/chromedriver")
        print('Crawler Made...')
        self.url = url
        # self.driver.get(url)
        # self.driver.maximize_window()

    # def scroll_down(self):
    #     """A method for scrolling the page."""
    #
    #     # Get scroll height.
    #     last_height = self.driver.execute_script("return document.body.scrollHeight")
    #
    #     while True:
    #
    #         # Scroll down to the bottom.
    #         self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #
    #         # Wait to load the page.
    #         time.sleep(2)
    #
    #         # Calculate new scroll height and compare with last scroll height.
    #         new_height = self.driver.execute_script("return document.body.scrollHeight")
    #
    #         if new_height == last_height:
    #             break
    #
    #         last_height = new_height

    def scrape(self, query='', word_length=5):
        elimination_regex = r'[^A-Za-z]'
        found_words = []
        start_time = time.time()
        self.driver.get(self.url + query)
        try:
            element = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "searchresults"))
            )
            headings = self.driver.find_elements_by_class_name("searchmatch")
            descriptions = self.driver.find_elements_by_class_name("searchresult")
        except:
            print('ok done')
            return
        end_time = time.time()
        #print(end_time - start_time)

        for heading in headings:
            split = heading.text.split()
            for word in split:
                filtered_word = re.sub(elimination_regex, '', word).lower()
                if len(filtered_word) is word_length:
                    if filtered_word not in found_words:
                        found_words.append(filtered_word)

        for description in descriptions:
            split = description.text.split()
            for word in split:
                filtered_word = re.sub(elimination_regex, '', word).lower()
                if len(filtered_word) is word_length:
                    if filtered_word not in found_words:
                        found_words.append(filtered_word)

        end_time = time.time()
        #print(end_time - start_time)
        return found_words

    def close(self):
        self.driver.close()


# the list the crawlers contributed to
if __name__ == "__main__":
    st_time = time.time()
    wikiCrawler = Crawler()
    words = wikiCrawler.scrape(query='This and or but if the that', word_length=5)
    print(words)
    wikiCrawler.close()
    # TODO
    # write to csv


# window.py, which was also used in hw5

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, title, content_wrapper, other_refresh=None):
        self.title = title
        self.content_wrapper = content_wrapper
        self.other_refresh = other_refresh
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 800)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 750, 750))
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setPlainText(content_wrapper.getContent())
        if other_refresh is not None:
            self.pushButton = QtWidgets.QPushButton(self.centralwidget)
            self.pushButton.setGeometry(QtCore.QRect(720, 750, 75, 23))
            self.pushButton.setObjectName("pushButton")

            def change_text():
                other_refresh()
                self.textEdit.setPlainText(content_wrapper.getContent())

            self.pushButton.clicked.connect(change_text)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", self.title))
        if self.other_refresh is not None:
            self.pushButton.setText(_translate("MainWindow", "Refresh"))

    def refresh(self):
        self.textEdit.setPlainText(self.content_wrapper.getContent())



