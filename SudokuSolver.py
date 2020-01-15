import tkinter as tk
import copy
import random

WIDTH = 544
HEIGHT = 600
TILE = 50
PADDING = 40
DIFF = 1
FONT = 'Helvetica'

bg_color = '#C8C8C8'
board_color = '#000000'
tile_color = '#999999'

test_values = {(0, 0): 0, (0, 1): 0, (0, 2): 0, (0, 3): 0, (0, 4): [2], (0, 5): 0, (0, 6): [1], (0, 7): 0, (0, 8): 0, (1, 0): 0, (1, 1): 0, (1, 2): [5], (1, 3): 0, (1, 4): 0, (1, 5): 0, (1, 6): [9], (1, 7): 0, (1, 8): 0, (2, 0): 0, (2, 1): [2], (2, 2): 0, (2, 3): 0, (2, 4): [6], (2, 5): 0, (2, 6): 0, (2, 7): 0, (2, 8): [4], (3, 0): [1], (3, 1): [5], (3, 2): [7], (3, 3): 0, (3, 4): 0, (3, 5): 0, (3, 6): 0, (3, 7): 0, (3, 8): 0, (4, 0): 0, (4, 1): 0, (4, 2): 0, (4, 3): 0, (4, 4): [4], (4, 5): 0, (4, 6): 0, (4, 7): 0, (4, 8): 0, (5, 0): 0, (5, 1): [8], (5, 2): 0, (5, 3): 0, (5, 4): 0, (5, 5): 0, (5, 6): [7], (5, 7): [5], (5, 8): 0, (6, 0): [6], (6, 1): 0, (6, 2): [2], (6, 3): [9], (6, 4): 0, (6, 5): 0, (6, 6): 0, (6, 7): [3], (6, 8): 0, (7, 0): 0, (7, 1): 0, (7, 2): [1], (7, 3): 0, (7, 4): 0, (7, 5): 0, (7, 6): 0, (7, 7): 0, (7, 8): [9], (8, 0): 0, (8, 1): 0, (8, 2): 0, (8, 3): [6], (8, 4): 0, (8, 5): [3], (8, 6): [8], (8, 7): 0, (8, 8): 0}
TESTING = True
#LET'S START
root = tk.Tk()
root.title('Sudoku Solver')

canvas = tk.Canvas(root, height = HEIGHT, width = WIDTH, bg = bg_color)
canvas.pack()

tk_bg = tk.Frame(root, bg = bg_color)
tk_bg.place(x = 0, y = 0, relwidth = 1, relheight = 1)

#LABEL
tk_MainLabel = tk.Label(root, font = (FONT, 20, 'bold'), bg = '#9D9D9D', fg = 'black', text='SUDOKU SOLVER', borderwidth=2, relief="solid")
tk_MainLabel.place(x = PADDING , y = PADDING, width = 250, height = 40)

#BOARD
tk_frame = tk.Frame(root, bg = board_color, bd = 0, relief = 'solid')
tk_frame.place(x = PADDING, y = HEIGHT - (DIFF*14 + TILE*9 + PADDING), width = DIFF*14 + TILE*9, height = DIFF*14 + TILE*9)

def createTile (a,b):
    try:
        value = test_values[(a,b)][0]
    except:
        value = ''
    tk_tile = tk.Entry(tk_frame, font = (FONT, 18, 'bold'), justify='center', bg = tile_color, fg = 'black', relief = 'flat')
    tk_tile.place(x = DIFF*(a+1 + 2*(a//3)) + TILE*a, y = DIFF*(b+1 + 2*(b//3)) + TILE*b, width = TILE, height = TILE)
    if TESTING == True:
        tk_tile.insert(0,value)
    return tk_tile

#CREATE TILES
tile_dict = dict()
for a in range (0,9):
    for b in range (0,9):
        tile_dict[(a,b)] = createTile(a,b)

def getEntries():
    """ Gets filled values from the board"""
    Entries = dict()
    for a in range (0,9):
        for b in range (0,9):
            value = tile_dict[(a,b)].get()
            try:
                Entries[(a,b)] = [int(value)]
            except:
                Entries[(a,b)] = 0
    return Entries

variants = dict()
solve_button_used = False
#SOLVE

def reset():
    global solve_button_used
    solve_button_used = False
    variants = dict()
    tk_solve_button['text'] = 'SOLVE'
    for a in range (0,9):
        for b in range (0,9):
            tile_dict[(a,b)].delete(0, 'end')
            tile_dict[(a,b)]['fg'] = 'black'


def partialReset():
    global solve_button_used
    solve_button_used = False
    variants = dict()
    tk_solve_button['text'] = 'SOLVE'
    for a in range (0,9):
        for b in range (0,9):
            if tile_dict[(a,b)]['fg'] != 'black':
                tile_dict[(a,b)].delete(0, 'end')
                tile_dict[(a,b)]['fg'] = 'black'

def solve():
    global solve_button_used
    if solve_button_used == False:
        found_randomized_solution = False
        solve_button_used = True
        inputted_values = getEntries()
        print('IN:',inputted_values)
        if TESTING == True:
            inputted_values = test_values
        variants = addVariants(inputted_values)
        iterateSolution(variants)
        # print('VAR:',variants)
        # short_string_coor = findShortListIndex(variants)
        # print('short string:',short_string)
        if checkSolution(variants): #first check if easy methods worked
            print('FOUND A SOLUTION')
            showResults(variants)
            # print('IN:',inputted_values)
            # print('------------')
            
            # checkSolution(variants)
        else:  #if easy methods didnt work, try guessing some points
            print("DIDN'T FOUND A SOLUTION")
            for a in range(0,50):
                #try 10-times guessing from the start
                variants_test = copy.deepcopy(variants)
                for b in range(0,20):
                    #choose 10-times random coordinate with legth > 2 and <3, choose randomly one
                    random_coor = getRandomDicCoorForShortList(variants_test,4)
                    if random_coor == -1:
                        print('Didnt find random coor')
                        break
                    variants_test[random_coor] = [random.choice(variants_test[random_coor])]
                    iterateSolution(variants_test)

                    if checkSolution(variants_test):
                        found_randomized_solution = True
                        break

                if checkSolution(variants_test):
                    found_randomized_solution = True
                    break

            
            if found_randomized_solution == True:
                showResults(variants_test)
            else:
                showResults(variants)

        tk_solve_button['text'] = 'EDIT'

    else:
        partialReset()

def addVariants(inputdict):
    """ Replaces zero values with [1,2,3,4,5,6,7,8,9] """
    temp = copy.deepcopy(inputdict)
    for a in range (0,9):
        for b in range (0,9):
            if inputdict[(a,b)] == 0:
                temp[(a,b)] = [1,2,3,4,5,6,7,8,9]
    return temp

def showResults(dictionary):
    """ shows the number of outputs """
    for a in range (0,9):
        for b in range (0,9):
            if tile_dict[(a,b)].get() == "":
                if len(dictionary[(a,b)]) == 1:
                    tile_dict[(a,b)].insert(0,dictionary[(a,b)][0])
                    tile_dict[(a,b)]['fg'] = 'blue'
                else:
                    tile_dict[(a,b)].insert(0,len(dictionary[(a,b)]))
                    tile_dict[(a,b)]['fg'] = 'red'


def collapseToUnique(dictionary, coodinates): 
    temp_list = list()
    temp_index_list = list()

    for idx,coor in enumerate(coodinates):
        for idx2,value in enumerate(dictionary[coor]):
            temp_list.append(value)
            temp_index_list.append(idx) 

    for idx, item in enumerate(temp_list):
        if temp_list.count(item) == 1: #if there is a single, collapse that element
            dictionary[coodinates[temp_index_list[idx]]] = [temp_list[idx]]


def getRandomDicCoorForShortList(dictionary,max):
    for a in range(0,200000):
        coor = (random.randint(0,8),random.randint(0,8))
        lenght = len(dictionary[coor])
        if lenght > 1 and lenght <= max:
            return coor 
    return -1


def findShortListIndex(dictionary): 
    """ finds a minimum of list lengths in a dictionary, higher than 1"""
    length_list = list()
    coor_list = list()
    for idx, item in enumerate(dictionary):
        # print(item,dictionary[item])
        coor_list.append(item)
        try:
            length_list.append(len(dictionary[item]))
        except:
            length_list.append(1)

    # print(length_list)
    for a in range(2,9):
        if a in length_list:
            print('short list / returning: ',coor_list[length_list.index(a)],'lenght','/ index:',length_list.index(a))
            return coor_list[length_list.index(a)]
    return -1   

def iterateSolution(dictionary):
    """  """
    for repeat in range(0,500):
        for typeiter in range(1,4): 
            for a in range(0,9):
                doubles_index = list()
                doubles_values = list()
                triples_values = list()
                quadruples_values = list()
                current_coordinate_list = getCoordinatelist(typeiter,a) 
                collapseToUnique(dictionary, current_coordinate_list)
                for index, coor in enumerate(current_coordinate_list):
                    #SINGLES
                    if len(dictionary[coor]) == 1:
                        value = dictionary[coor][0]
                        removeValueFromCoordExceptOne(index, value, current_coordinate_list,dictionary)
                    #DOUBLES
                    elif len(dictionary[coor]) == 2:
                        if dictionary[coor] in doubles_values: #that means there is the same double
                            otherindex = doubles_index[doubles_values.index(dictionary[coor])]
                            removeValueFromCoordExceptTwo(index, otherindex, dictionary[coor], current_coordinate_list, dictionary)                          
                        else:
                            doubles_values.append(dictionary[coor])
                            doubles_index.append(index)
                    #TRIPLES
                    elif len(dictionary[coor]) == 3:
                        if triples_values.count(dictionary[coor]) == 2: #that means there is the same triple
                            # print('found triple')
                            removeValueFromCoordExceptThree(dictionary[coor], current_coordinate_list, dictionary)                          
                        else:
                            triples_values.append(dictionary[coor])
                    #QUADRUPLES
                    elif len(dictionary[coor]) == 4:
                        if quadruples_values.count(dictionary[coor]) == 3: #that means there is the same quadruple
                            # print('found quadruple')
                            removeValueFromCoordExceptFour(dictionary[coor], current_coordinate_list, dictionary)                          
                        else:
                            quadruples_values.append(dictionary[coor])

# These following fuctions could be made into one

def removeValueFromCoordExceptFour(valuelist, coordinates, dictionary):
    """ Goes over a list of coordinates, and removes elements from valuelist except if dictionary[coor] == valuelist"""
    for idx, coor in enumerate(coordinates):
        if dictionary[coor] != valuelist: #remove valuelist only from elements that aren't equal to valuelist
            if valuelist[0] in dictionary[coor]: 
                dictionary[coor].remove(valuelist[0])
            if valuelist[1] in dictionary[coor]: 
                dictionary[coor].remove(valuelist[1])    
            if valuelist[2] in dictionary[coor]: 
                dictionary[coor].remove(valuelist[2])   
            if valuelist[3] in dictionary[coor]: 
                dictionary[coor].remove(valuelist[2]) 


def removeValueFromCoordExceptThree(valuelist, coordinates, dictionary):
    """ Goes over a list of coordinates, and removes elements from valuelist except if dictionary[coor] == valuelist"""
    for idx, coor in enumerate(coordinates):
        if dictionary[coor] != valuelist: #remove valuelist only from elements that aren't equal to valuelist
            if valuelist[0] in dictionary[coor]: 
                dictionary[coor].remove(valuelist[0])
            if valuelist[1] in dictionary[coor]: 
                dictionary[coor].remove(valuelist[1])    
            if valuelist[2] in dictionary[coor]: 
                dictionary[coor].remove(valuelist[2])                 

def removeValueFromCoordExceptTwo(index1, index2, valuelist, coordinates, dictionary):
    """ Goes over a list of coordinates, and removes elements from valuelist from dictionary[coor] except for index1 and index2"""
    for idx, coor in enumerate(coordinates):
        if idx != index1 and idx != index2:
            if valuelist[0] in dictionary[coor]: 
                dictionary[coor].remove(valuelist[0])
            if valuelist[1] in dictionary[coor]: 
                dictionary[coor].remove(valuelist[1])    

def removeValueFromCoordExceptOne(index, value, alist, dictionary):
    """ Goes over a list of coordinates, and removes value from dictionary[coor] except for index index"""
    for idx, coor in enumerate(alist):
        if idx != index:
            if value in dictionary[coor]:
                dictionary[coor].remove(value)

def getCoordinatelist(type,number):
    """ Provides coordinates - rows, columns or squares over which to iterate (list of tuples)"""
    coordinates = list()
    if type == 1: #columns
        for a in range(0,9):
            coordinates.append((number,a))
    elif type == 2: #rows
        for a in range(0,9):
            coordinates.append((a,number))
    elif type == 3: #squares
        for a in range(0,3):
            for b in range (0,3):
                coordinates.append((a + 3*(number % 3),b + 3*(number // 3)))
    return coordinates

def checkSolution(dictionary):
    passed = True
    for typeiter in range(1,4): 
        for a in range(0,9):
            value_list = list()
            current_coordinate_list = getCoordinatelist(typeiter,a) 
            for index, coor in enumerate(current_coordinate_list):
                if len(dictionary[coor]) == 1:
                    value_list.append(dictionary[coor][0])
                # else:
                    # print('ERROR - final list not of length one')
            # print(value_list)
            if len(set(value_list)) != 9:
                passed = False
    if passed == False:
        print('INVALID SOLUTION')
    else:
        print('VALID SOLUTION')
    return passed
                
button_width = 90

tk_solve_button = tk.Button(root, font = (FONT, 16, 'bold'), bg = tile_color, fg = 'black', text='RESET', relief='groove', command=lambda: reset())
tk_solve_button.place(x = WIDTH  - PADDING - 10 - button_width, y = PADDING, width = button_width, height = 40, anchor = 'ne')

tk_solve_button = tk.Button(root, font = (FONT, 16, 'bold'), bg = tile_color, fg = 'black', text='SOLVE', relief='groove', command=lambda: solve())
tk_solve_button.place(x = WIDTH  - PADDING , y = PADDING, width = button_width, height = 40, anchor = 'ne')

root.mainloop()