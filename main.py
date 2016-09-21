import argparse
import json
import collections
import rule
import math
import copy
from tkinter import *
from tkinter import ttk

BOX_ROWS = 3
BOX_COLS = 3
SUDOKU_ROWS = 9
SUDOKU_COLS = 9
NUM_MIN = 1
NUM_MAX = 9
# Format:
# 0 = unsolved
#Array = guesses
# E = No box here (for odd formats)

def load(location):
    return json.load(location)

def save(sudoku, location):
    f = open(location, mode='w')
    json.dump(sudoku, f)


def printSudoku(sudoku):
    outstring = '\n'
    for x in range(len(sudoku[0])):
        outstring += '____'
    outstring += '__\n'

    line = ''
    for row in sudoku:
        for col in row:
            outstring += ' | '
            if col != 0 and not isinstance(col, list):
                outstring += str(col)
            else:
                outstring += ' '
        outstring += ' |\n'
        for x in range(len(row)):
            outstring += '____'
        outstring += '__\n'
    print(outstring)


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


def solveSudoku(sudoku):
    sudoku = getPossibilities(sudoku)
    sudokuModified = True
    while sudokuModified:
        sudokuModified = False
        for row in range(0, SUDOKU_ROWS):
            for col in range(0, SUDOKU_COLS):
                if isinstance(sudoku[row][col], list):
                    newValue = rule1(sudoku, row, col)
                    #print(newValue, sudoku[row][col])
                    if newValue != sudoku[row][col]:
                        #print(True)
                        sudokuModified = True
                        if not validMove(sudoku, row, col, newValue):
                            print('NO BAD MOVE')
                        sudoku[row][col] = newValue
                        sudoku = getPossibilities(sudoku)
                    else:
                        newValue = rule2(sudoku, row, col)
                        if newValue != sudoku[row][col]:
                            sudokuModified = True
                            if not validMove(sudoku, row, col, newValue):
                                print('NO BAD MOVE 2')
                            sudoku[row][col] = newValue
                            sudoku = getPossibilities(sudoku)
    return sudoku

def renderSudoku(sudokuOutput, sudoku):
    for row in range(SUDOKU_ROWS):
        for col in range(SUDOKU_COLS):
            if isinstance(sudoku[row][col], list):
                output = ''
                for x in range(NUM_MIN, NUM_MAX+1):
                    if x in sudoku[row][col]:
                        output += str(x) + ' '
                    else:
                        output += '_ '
                    if x % 3 == 0:
                        output = output[:-1] + '\n'
                output = output[:-1]
                sudokuOutput[row][col].config(text=output)
            else:
                sudokuOutput[row][col].config(text='\n__' + str(sudoku[row][col]) + '__\n')

def action():
    if (args.print != None):
        printSudoku(load(args.print[0])[0])
        root.destroy()
    elif (args.solve != None):
        i = 0
        for puzzle in sudokuList:
            if (puzzle['puzzleNumber'] != 615):
                continue
            #printSudoku(puzzle['sudoku'])
            sudoku = solveSudoku(copy.deepcopy(puzzle['sudoku']))
            if puzzle['solution'] == sudoku:
                i+=1
            printSudoku(puzzle['solution'])
            renderSudoku(sudokuOutput, sudoku)
            #printSudoku(sudoku)
            #print(puzzle['solution'] == sudoku)
            if puzzle['solution'] != sudoku:
                print('Could not solve puzzle ' + str(puzzle['puzzleNumber']) + ' difficulty:' + puzzle['puzzleDifficulty'])

        print('Solved ' + str(i) + ' puzzles out of ' + str(len(sudokuList)) + ' which is ' + str(i*100/len(sudokuList)) + '%')
        #root.destroy()
        #save(sudoku, 'output.json')
    else:
        print("No Args... Please enter args")
        root.destroy()
        exit(0)


parser = argparse.ArgumentParser(description='Lib for sudoku function')
parser.add_argument('--print', nargs=1, type=argparse.FileType(),
                    help='prints the sudoku stored in JSON')
parser.add_argument('--solve', nargs=1, type=argparse.FileType(),
                    help='prints the sudoku stored in JSON')

args = parser.parse_args()

root = Tk()
root.title("Sudoku")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
solveBtn = ttk.Button(mainframe)
solveBtn.grid(column=0, row=SUDOKU_ROWS+1, columnspan=SUDOKU_COLS, sticky=(W, E))
solveBtn.config(text='Solve', command=action)
sudokuOutput = []
for row in range(SUDOKU_ROWS):
    sudokuOutput.append([])
    for col in range(SUDOKU_COLS):
        sudokuOutput[row].append(ttk.Label(mainframe))
        sudokuOutput[row][col].grid(column=col, row=row, sticky=(W, E))
        sudokuOutput[row][col].config(font=("Courier", 12), relief=SOLID, borderwidth=5, text='1 2 3\n4 5 6\n7 8 9')

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

if (args.print != None):
    renderSudoku(sudokuOutput, load(args.print[0])[0])
elif (args.solve != None):
    sudokuList = load(args.solve[0])
    for puzzle in sudokuList:
        if (puzzle['puzzleNumber'] == 615):
            renderSudoku(sudokuOutput, getPossibilities(puzzle['sudoku']))
else:
    print("No Args... Please enter args")
    root.destroy()
    exit(0)

root.mainloop()
