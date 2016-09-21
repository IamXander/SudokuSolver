import requests
import re
import json

#should pass in what is between the table tags
def parseSudoku(html):
	html = re.sub('&nbsp;', '0', html)
	rows = re.findall('<tr class="grid">(.+?)</tr>', html, flags=re.DOTALL)
	sudoku = []
	for r in rows:
	    cols = [int(numeric_string) for numeric_string in re.findall('<td.*?>(.*?)</td>', r, flags=re.DOTALL)]
	    sudoku.append(cols)
	return sudoku

sudokuList = []
NUM_SUDOKUS = 100 + 1
STEP_SIZE = 123
START_SUDOKU = 123
#6341241
for i in range(START_SUDOKU, STEP_SIZE*NUM_SUDOKUS, STEP_SIZE):
	puzz = requests.get('http://www.menneske.no/sudoku/eng/showpuzzle.html?number=' + str(i))
	sol = requests.get('http://www.menneske.no/sudoku/eng/solution.html?number=' + str(i))
	puzzleNumber = int(re.search('Showing puzzle number: (.*?)<br', puzz.text, re.DOTALL).group(1))
	puzzleDifficulty = re.search('Difficulty: (.*?)<br', puzz.text, re.DOTALL).group(1)
	puzzleType = re.search('Puzzletype: (.*?)<br', puzz.text, re.DOTALL).group(1)
	puzzleStartNums = re.search('Startnumbers: (.*?)<br', puzz.text, re.DOTALL).group(1)

	sudoku = parseSudoku(re.search('<h3>Sudoku puzzle</h3>.*?<div class="grid">.*?<table>(.+?)</table>', puzz.text, re.DOTALL).group(1))
	solution = parseSudoku(re.search('<h3>Solution</h3>.*?<div class="grid">.*?<table>(.+?)</table>', sol.text, re.DOTALL).group(1))

	sudokuList.append({'puzzleNumber': puzzleNumber,
	                   'puzzleDifficulty': puzzleDifficulty,
	                   'puzzleType': puzzleType,
	                   'puzzleStartNums': puzzleStartNums,
	                   'sudoku': sudoku,
					   'solution': solution})
	print('added puzzle number ' + str(puzzleNumber) + ' which is ' + puzzleDifficulty + ' ... Current Progress ' + str((i-START_SUDOKU+STEP_SIZE)*100/((STEP_SIZE*NUM_SUDOKUS)-START_SUDOKU)) + '%')

f = open('sudokuList.json', 'w')
json.dump(sudokuList, f)
f.close()

#<h3>Sudoku puzzle</h3>.*?<div class="grid">.*?<table>(.+?)</table>

# puzzle: http://www.menneske.no/sudoku/eng/showpuzzle.html?number=1448569
# solution: http://www.menneske.no/sudoku/eng/solution.html?number=1448569


# <h3>Sudoku puzzle</h3>
# <div class="grid"><table>
# <tr class="grid">
# <td class="normal">&nbsp;</td>
# <td class="normal">&nbsp;</td>
# <td class="rightedge">1</td>
# <td class="normal">&nbsp;</td>
# <td class="normal">8</td>
# <td class="rightedge">&nbsp;</td>
# <td class="normal">5</td>
# <td class="normal">&nbsp;</td>
# <td class="rightedge">&nbsp;</td>
# </tr>
# <tr class="grid">
# <td class="normal">8</td>
# <td class="normal">&nbsp;</td>
# <td class="rightedge">&nbsp;</td>
# <td class="normal">5</td>
# <td class="normal">7</td>
# <td class="rightedge">&nbsp;</td>
# <td class="normal">&nbsp;</td>
# <td class="normal">&nbsp;</td>
# <td class="rightedge">4</td>
# </tr>
# <tr class="grid">
# <td class="bottomedge">&nbsp;</td>
# <td class="bottomedge">5</td>
# <td class="bottomright">3</td>
# <td class="bottomedge">&nbsp;</td>
# <td class="bottomedge">&nbsp;</td>
# <td class="bottomright">&nbsp;</td>
# <td class="bottomedge">6</td>
# <td class="bottomedge">8</td>
# <td class="bottomright">&nbsp;</td>
# </tr>
# <tr class="grid">
# <td class="normal">&nbsp;</td>
# <td class="normal">&nbsp;</td>
# <td class="rightedge">7</td>
# <td class="normal">&nbsp;</td>
# <td class="normal">5</td>
# <td class="rightedge">9</td>
# <td class="normal">&nbsp;</td>
# <td class="normal">&nbsp;</td>
# <td class="rightedge">&nbsp;</td>
# </tr>
# <tr class="grid">
# <td class="normal">6</td>
# <td class="normal">&nbsp;</td>
# <td class="rightedge">&nbsp;</td>
# <td class="normal">&nbsp;</td>
# <td class="normal">&nbsp;</td>
# <td class="rightedge">&nbsp;</td>
# <td class="normal">&nbsp;</td>
# <td class="normal">&nbsp;</td>
# <td class="rightedge">7</td>
# </tr>
# <tr class="grid">
# <td class="bottomedge">&nbsp;</td>
# <td class="bottomedge">&nbsp;</td>
# <td class="bottomright">&nbsp;</td>
# <td class="bottomedge">7</td>
# <td class="bottomedge">6</td>
# <td class="bottomright">&nbsp;</td>
# <td class="bottomedge">4</td>
# <td class="bottomedge">&nbsp;</td>
# <td class="bottomright">&nbsp;</td>
# </tr>
# <tr class="grid">
# <td class="normal">&nbsp;</td>
# <td class="normal">7</td>
# <td class="rightedge">5</td>
# <td class="normal">&nbsp;</td>
# <td class="normal">&nbsp;</td>
# <td class="rightedge">&nbsp;</td>
# <td class="normal">2</td>
# <td class="normal">1</td>
# <td class="rightedge">&nbsp;</td>
# </tr>
# <tr class="grid">
# <td class="normal">9</td>
# <td class="normal">&nbsp;</td>
# <td class="rightedge">&nbsp;</td>
# <td class="normal">&nbsp;</td>
# <td class="normal">3</td>
# <td class="rightedge">5</td>
# <td class="normal">&nbsp;</td>
# <td class="normal">&nbsp;</td>
# <td class="rightedge">6</td>
# </tr>
# <tr class="grid">
# <td class="bottomedge">&nbsp;</td>
# <td class="bottomedge">&nbsp;</td>
# <td class="bottomright">4</td>
# <td class="bottomedge">&nbsp;</td>
# <td class="bottomedge">1</td>
# <td class="bottomright">&nbsp;</td>
# <td class="bottomedge">3</td>
# <td class="bottomedge">&nbsp;</td>
# <td class="bottomright">&nbsp;</td>
# </tr>
# </table>
