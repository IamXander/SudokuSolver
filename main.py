import argparse
import json
import collections
import math
import copy

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

BOX_ROWS = 3
BOX_COLS = 3
SUDOKU_ROWS = 9
SUDOKU_COLS = 9
NUM_MIN = 1
NUM_MAX = 9

def load(location):
    return json.load(location)

def save(sudoku, location):
    f = open(location, mode='w')
    json.dump(sudoku, f)


def printSudoku(sudoku):
    outstring = ''
    for x in range(len(sudoku[0])):
        outstring += '\u2015\u2015\u2015\u2015'
    outstring += '\u2015\u2015\u2015'
    print(outstring)

    line = ''
    for row in range(len(sudoku)):
        prow1 = []
        prow2 = []
        prow3 = []
        for col in range(len(sudoku[row])):
            rowString = '|   '
            if col % 3 == 0 and col != 0:
                rowString = color.BOLD + color.CYAN + '||' + color.END + '   '
            prow1 += rowString
            prow2 += rowString
            prow3 += rowString
            if isinstance(sudoku[row][col], list):
                for x in sudoku[row][col]:
                    if x >= 1 and x <= 3:
                        prow1[x-4] = str(x)
                    elif x >= 4 and x <= 6:
                        prow2[x-7] = str(x)
                    else:
                        prow3[x-10] = str(x)
            elif sudoku[row][col] != 0:
                prow2[-2] = color.BOLD + color.RED + str(sudoku[row][col]) + color.END;
        print("".join(prow1) + '|')
        print("".join(prow2) + '|')
        print("".join(prow3) + '|')
        #outstring += "".join(prow1) + '|\n' + "".join(prow2) + '|\n' + "".join(prow3) + '|\n'
        if row % 3 == 2 and row != len(sudoku[row]) - 1:
            print(color.BOLD + color.YELLOW + color.UNDERLINE + outstring + color.END)
            #print(color.BOLD + color.YELLOW + outstring + color.END)
        else:
            print(outstring)
    print()


def getBox(sudoku, row, col):
    rowStart = math.floor(row / BOX_ROWS) * BOX_ROWS
    colStart = math.floor(col / BOX_COLS) * BOX_COLS
    box = []
    for r in range(rowStart, rowStart + BOX_ROWS):
        for c in range(colStart, colStart + BOX_COLS):
            box.append(sudoku[r][c])
    return box


def getRow(sudoku, row):
    return sudoku[row]


def getCol(sudoku, col):
    c = []
    for x in range(0, SUDOKU_ROWS):
        c.append(sudoku[x][col])
    return c


def validMove(sudoku, row, col, val):
    # is empty box
    if isinstance(val, list):
        return True
    elif val in getRow(sudoku, row):
        return False
    elif val in getCol(sudoku, col):
        return False
    elif val in getBox(sudoku, row, col):
        return False
    # that is a valid move son
    else:
        return True


def getPossibilities(sudoku):
    for row in range(0, SUDOKU_ROWS):
        for col in range(0, SUDOKU_COLS):
            if sudoku[row][col] == 0 or isinstance(sudoku[row][col], list):
                newGuesses = []
                for x in range(NUM_MIN, NUM_MAX + 1):
                    if validMove(sudoku, row, col, x):
                        newGuesses.append(x)
                if sudoku[row][col] == 0 or len(newGuesses) < len(sudoku[row][col]):
                    if len(newGuesses) == 0: #There should always be guesses. If there is not the we have found a paradox
                        raise ValueError('Invalid Sudoku')
                    sudoku[row][col] = newGuesses
    return sudoku

# if there is only one guess solve that sucka
def rule1(sudoku, row, col):
    if len(sudoku[row][col]) == 1:
        return sudoku[row][col][0]
    return sudoku[row][col]

#if only type in row, col, or box
def rule2(sudoku, row, col):
    for possibility in sudoku[row][col]:

        #check row
        colIdx = 0
        for colElt in getRow(sudoku, row):
            if colIdx != col and isinstance(colElt, list):
                if possibility in colElt:
                    break
            colIdx += 1
        else:
            return possibility

        #check col
        rowIdx = 0
        for rowElt in getCol(sudoku, col):
            if rowIdx != row and isinstance(rowElt, list):
                if possibility in rowElt:
                    break
            rowIdx += 1
        else:
            return possibility

        #check box
        boxIdx = 0
        for boxElt in getBox(sudoku, row, col):
            if boxIdx != (row%3)*3+(col%3) and isinstance(boxElt, list):
                if possibility in boxElt:
                    break
            boxIdx += 1
        else:
            return possibility

    return sudoku[row][col]

def isSolved(sudoku):
    for row in sudoku:
        for col in row:
            if isinstance(col, list):
                return False
    return True


def solveSudoku(sudoku):
    try:
        sudoku = getPossibilities(sudoku)
    except ValueError as ve:
        return False
    sudokuModified = True
    possRow = 0;
    possCol = 0;
    sudokuCompleted = True;
    while sudokuModified:
        sudokuModified = False
        sudokuCompleted = True;
        for row in range(0, SUDOKU_ROWS):
            for col in range(0, SUDOKU_COLS):
                if isinstance(sudoku[row][col], list):
                    sudokuCompleted = False;
                    possRow = row
                    possCol = col
                    newValue = rule1(sudoku, row, col)
                    if newValue != sudoku[row][col]:
                        sudokuModified = True
                        sudoku[row][col] = newValue
                        try:
                            sudoku = getPossibilities(sudoku)
                        except ValueError as ve:
                            return False
                    else:
                        newValue = rule2(sudoku, row, col)
                        if newValue != sudoku[row][col]:
                            sudokuModified = True
                            sudoku[row][col] = newValue
                            try:
                                sudoku = getPossibilities(sudoku)
                            except ValueError as ve:
                                return False
    #Rule 1 and 2 didn't pan out. Time to brute force
    if sudokuCompleted == False:
        guessList = sudoku[possRow][possCol]
        #print('Not solved')
        for x in guessList:
            sudoku[possRow][possCol] = x;
            tmpSudoku = solveSudoku(copy.deepcopy(sudoku))
            if tmpSudoku != False and isSolved(tmpSudoku) == True:
                return tmpSudoku
    return sudoku


parser = argparse.ArgumentParser(description='Lib for sudoku function')
parser.add_argument('--print', nargs=1, type=argparse.FileType(),
                    help='prints the sudoku stored in JSON')
parser.add_argument('--solve', nargs=1, type=argparse.FileType(),
                    help='prints the sudoku stored in JSON')

args = parser.parse_args()

if (args.print != None):
    sudokuList = load(args.print[0])
    currentSudoku = sudokuList[0]['sudoku'];
    currentSudoku = getPossibilities(currentSudoku)
    printSudoku(currentSudoku)
elif (args.solve != None):
    sudokuList = load(args.solve[0])
    i = 0
    for puzzle in sudokuList:
        printSudoku(puzzle['sudoku'])
        sudoku = solveSudoku(copy.deepcopy(puzzle['sudoku']))
        if puzzle['solution'] == sudoku:
            i+=1
        printSudoku(sudoku)
        # if puzzle['solution'] != sudoku:
        #     print('Could not solve puzzle ' + str(puzzle['puzzleNumber']) + ' difficulty:' + puzzle['puzzleDifficulty'])

    print('Solved ' + str(i) + ' puzzles out of ' + str(len(sudokuList)) + ' which is ' + str(i*100/len(sudokuList)) + '%')
else:
    print("No Args... Please enter args")
    exit(0)

#python main.py --solve sudokuList.py
