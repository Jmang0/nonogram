from itertools import permutations
import math
from copy import copy
import pyautogui as p
import time
from PIL import ImageGrab

#-------------------------------------------------------------------------------

def printGrid():
    print("--------------------")
    global grid
    for clm in grid:
        line = ""
        for i in clm:
            if i == '1':
                line += "X"
            elif i == '2':
                line += u"\u2588"
            else:
                line += " "
        print(line)
    print("--------------------")

def find_cmbs(clue,line_length): #arguements are a list of integers as a clue and a 0 or 1 (column or rows) find_cmbs([1,2],0)
    #A list with the filled in blocks
    filled_blocks = ["".join(["2" for i in range(i)]) for i in clue]

    #A list containing the right AMOUNT of 1s(Xs) and 2s(filled)
    blocks = copy(filled_blocks)
    for i in range(line_length - sum(clue)):
        blocks.append("1")

    #Get all permutations
    cmbs = list(set(permutations(blocks)))

    #Filter permutations that are not allowed
    final_cmbs = []
    for cmb in cmbs:
        order = copy(filled_blocks) #a copy of the correct order
        valid = True
        gap = False
        for block in cmb:
            if gap:
                if block != '1':
                    valid = False
                    break
                else:
                    gap = False
            elif len(order) == 0:
                break
            elif block == order[0]:
                order.pop(0)
                gap = True
        if valid and not len(order):
            final_cmbs.append("".join(cmb))

    return final_cmbs

def enter(entry,rows):
    global grid
    for x,line in enumerate(entry):
        #first put in everything with only 1 possibility
        if len(line) == 1:
            for y,char in enumerate(line[0]):
                if rows:
                    grid[x][y] = char
                else:
                    grid[y][x] = char
            line.remove(line[0])
        elif len(line) > 1:
            confirmed = []
            for i in line[0]:
                confirmed.append(i)
            for poss in line:
                for count,char in enumerate(poss):
                    if char != confirmed[count]:
                        confirmed[count] = '0'
            for y,char in enumerate(confirmed):
                if char != '0':
                    if rows:
                        grid[x][y] = char
                    else:
                        grid[y][x] = char
def narrow(cmbs,rows):
    global grid
    for x,line in enumerate(cmbs):
        remove = []
        for poss in line:
            for y,char in enumerate(poss):
                if rows:
                    if char != grid[x][y] and grid[x][y] != '0':
                        remove.append(poss)
                        break

                else:
                    if char != grid[y][x] and grid[y][x] != '0':
                        remove.append(poss)
                        break

        for i in remove:
            line.remove(i)
def isDone():
    global grid
    for i in grid:
        for i2 in i:
            if i2 == '0':
                return False
    return True

#-------------------------------------------------------------------------------

def solve(columnClues,rowClues,prnt=False):
    global grid,size
    size = [len(columnClues),len(rowClues)]

    #Set up blank grid
    grid = [['0' for i in range(size[1])] for i in range(size[0])]

    #grid[column][row]
    #to access 1st row, 3rd column you would use grid[2][0]
    #0 is nothing, 1 is cross, 2 is filled

    #-----Get all possibilities
    columnCombinations = []
    rowCombinations = []

    print('Finding all possibilities for each row/column...')
    progress = str(len(rowClues) + len(columnClues))
    count = 0
    for i in rowClues:
        rowCombinations.append(find_cmbs(i,size[1]))
        count += 1
        print("%s / %s" % (count,progress))

    for i in columnClues:
        columnCombinations.append(find_cmbs(i,size[0]))
        count += 1
        print("%s / %s" % (count,progress))

    #compare the current possibilities with the info in the grid
    #delete posibilities that don't match up
    enter(rowCombinations,True)
    enter(columnCombinations,False)
    if prnt:
        printGrid()


    while not isDone():
        narrow(rowCombinations,True)
        enter(rowCombinations,True)
        if prnt:
            printGrid()

        narrow(columnCombinations,False)
        enter(columnCombinations,False)
        if prnt:
            printGrid()
    return grid

if __name__ == '__main__':
    #Tests
    #animals 18 (9x9 test)
    #columnClues = [[1,2],[2,3],[1,2],[2,3],[1,2],[2,3],[1,2]]
    #rowClues = [[],[1,1,1],[7],[],[1,1,1],[7],[7]]

    #5x5
    # columnClues = [[1,1],[2],[3],[3],[3]]
    # rowClues = [[3],[1,3],[3],[2],[1]]

    #10x10
    columnClues = [[3,4],[1,2],[1,3],[1],[3],[5,3],[7],[6],[6],[5]]
    rowClues = [[1,8],[1,6],[2,6],[5],[1,1,5],[3,3],[3,1],[1,1],[1],[1]]

    solve(columnClues,rowClues,prnt=True)
