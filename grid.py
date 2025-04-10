from random import randint, choice

ALPHA = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
ENEMY_DISPLAY = ["~","*","#"]
ALPHA_COORDS = {"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7,"I":8,"J":9,"K":10,"L":11,"M":12,"N":13,"O":14,"P":15,"Q":16,"R":17,"S":18,"T":19,"U":20,"V":21,"W":22,"X":23,"Y":24,"Z":25}
SHIP_LENGTHS = {"Aircraft Carrier":5,"Battleship":4,"Submarine":3,"Cruiser":3,"Destroyer":2}

def createGrid(height,width):
    grid = [["~" for i in range(width)] for j in range(height)]
    return grid

def returnGrids(yours,enemy):
    print("-"*((len(yours)+4)*2))
    print((" " + "┏"+"-"*(len(yours)//4)+"YOU"+"-"*(len(yours)-len(yours)//4-3)+"┓") + "  " + ("┏"+"-"*(len(yours)//4)+"ENEMY"+"-"*(len(yours)-len(yours)//4-5)+"┓"))
    letters = iter(ALPHA)
    for row in range(len(yours)):
        letter = next(letters)
        output = f"{letter}|"
        for item in yours[row]:
            output += item
        output += f"| {letter}|"
        for item in enemy[row]:
            if item in ENEMY_DISPLAY:
                output += item
            else:
                output += "~"
        print(output + "|")
    print((" " + "┗"+"-"*len(yours)+"┛") + "  " + ("┗"+"-"*len(yours)+"┛"))
    nums = ""
    for i in range(0,len(yours[0])):
        nums += str(i)
    print("  " + nums + "    " + nums)
    print("-"*((len(yours)+4)*2))

#~ is untouched space, * is a miss, # is a hit, letter is unknown ship.
#Ships: (A)ircraft Carrier - A, (B)attleship - B, (S)ubmarine - S, (C)ruiser - C, (D)estroyer - D

def returnUserGrid(grid):
    print("-"*((len(grid)+2)))
    print((" " + "┏"+"-"*(len(grid)//4)+"YOU"+"-"*(len(grid)-len(grid)//4-3)+"┓"))
    letters = iter(ALPHA)
    for row in range(len(grid)):
        letter = next(letters)
        output = f"{letter}|"
        for item in grid[row]:
            output += item
        output += "|"
        print(output)
    print((" " + "┗"+"-"*len(grid)+"┛"))
    nums = ""
    for i in range(0,len(grid[0])):
        nums += str(i)
    print("  " + nums + "    " + nums)
    print("-"*((len(grid)+2)))

def checkFits(shipLen, pos, rotation, grid): #shipLen generally between 2 and 5, pos is tuple (x,y) of index in grid, rotation is in degrees. Choose 0 (right) or 90 (down)
    neededSpaces = []
    for i in range(shipLen):
        if rotation == 0:
            neededSpaces.append((pos[0]+i,pos[1]))
        elif rotation == 90:
            neededSpaces.append((pos[0],pos[1]+i))
    works = True
    for i in neededSpaces:
        try:
            if grid[i[1]][i[0]] != "~":
                works = False
        except IndexError:
            works = False
    return works

def placeShip(shipLen, shipType, pos, rotation, grid): #shipLen generally between 2 and 5, pos is tuple (x,y) of index in grid, rotation is in degrees. Choose 0 (right) or 90 (down)
    neededSpaces = []
    for i in range(shipLen):
        if rotation == 0:
            neededSpaces.append((pos[0]+i,pos[1]))
        elif rotation == 90:
            neededSpaces.append((pos[0],pos[1]+i))
    for i in neededSpaces:
        grid[i[1]][i[0]] = shipType[0]
    return grid

def placeEnemyShips(grid):
    enemyGrid = grid.copy()
    for ship in SHIP_LENGTHS:
        valid = False
        count = 0
        while not valid:
            rotation = choice([0,90])
            if rotation == 0:
                posX = randint(0,len(enemyGrid[0])-SHIP_LENGTHS[ship])
                posY = randint(0,len(enemyGrid)-1)
            else:
                posX = randint(0,len(enemyGrid[0])-1)
                posY = randint(0,len(enemyGrid)-SHIP_LENGTHS[ship])
            if checkFits(SHIP_LENGTHS[ship], (posX,posY), rotation, enemyGrid):
                valid = True
            else:
                count += 1
                if count > 100:
                    return grid
        
        enemyGrid = placeShip(SHIP_LENGTHS[ship], ship, (posX, posY), rotation, enemyGrid)
    return enemyGrid

def setupUserGrid(grid):
    userGrid = grid.copy()
    for ship in SHIP_LENGTHS:
        returnUserGrid(userGrid)
        valid = False
        while not valid:
            pos = ""
            while not(len(pos) == 5 and pos[0].isalpha() and pos[1].isnumeric() and (pos[3:] == "00" or pos[3:] == "90")):
                pos = input(f"Please enter coordinates and direction for your {ship}, in format \"A3 00\" where A3 is the starting (top-left) coordinate of the ship and 00 is the direction. Please only enter 00 (right) or 90 (down) for the direction, and ensure that your ship won't collide with others or the side of the map: ").upper()

            parts = pos.split(" ")
            posX = int(parts[0][1])
            posY = ALPHA_COORDS[parts[0][0]]
            direction = int(parts[1])
            if posY < len(userGrid):
                valid = checkFits(SHIP_LENGTHS[ship], (posX,posY), direction, userGrid)
        userGrid = placeShip(SHIP_LENGTHS[ship],ship,(posX,posY),direction,userGrid)
    
    return userGrid

def checkValidShot(enemyGrid,pos):
    try:
        valid = enemyGrid[pos[1]][pos[0]] in "~ABCDS"
        return valid
    except IndexError:
        return False

def shoot(enemyGrid,pos):
    current = enemyGrid[pos[1]][pos[0]]
    if current in "ABCDS":
        enemyGrid[pos[1]][pos[0]] = "#"
        return enemyGrid, True
    elif current == "~":
        enemyGrid[pos[1]][pos[0]] = "*"
        return enemyGrid, False
    return enemyGrid, False

def generateCoord(grid):
    yCoord = randint(0,len(grid))
    xCoord = randint(0,len(grid[0]))
    return (xCoord, yCoord)