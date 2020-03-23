from time import sleep
from selenium import webdriver
from pprint import pprint
from nonogram import solve

driver = webdriver.Chrome('/Users/jaimangos/Desktop/chromedriver')  # Optional argument, if not specified will search path.
driver.get('https://www.puzzle-nonograms.com/?size=1');

# Get top clues
top = driver.find_element_by_id('taskTop')
boxes = top.find_elements_by_class_name('task-group')
columnClues = [
    [int(i.text) for i in box.find_elements_by_class_name('selectable')]
for box in boxes]

# Get side clues
side = driver.find_element_by_id('taskLeft')
boxes = side.find_elements_by_class_name('task-group')
rowClues = [
    [int(i.text) for i in box.find_elements_by_class_name('selectable')]
for box in boxes]

#Enter solution
all_cells = driver.find_element_by_class_name('nonograms-cell-back')
rows = all_cells.find_elements_by_class_name('row')

solution = solve(columnClues,rowClues)
for row in range(len(solution)):
    for column in range(len(solution)):
        if solution[row][column] == '2':
            cells = rows[row].find_elements_by_class_name('cell')
            cells[column].click()

#Click done
driver.find_element_by_id('btnReady').click()

sleep(10)
driver.quit()
