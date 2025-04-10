from grid import *
def setup(gridHeight,gridWidth):
    userGrid = createGrid(gridHeight,gridWidth)
    enemyGrid = createGrid(gridHeight,gridWidth)
    while enemyGrid == createGrid(gridHeight,gridWidth):
        enemyGrid = placeEnemyShips(enemyGrid)
    setupUserGrid(userGrid)
    grids = {"user":userGrid,"enemy":enemyGrid}
    return grids

def enemyTurn(grids):
    valid = False
    while not valid:
        coord = generateCoord(grids["user"])
        if checkValidShot(grids["user"],coord):
            grids["user"], hit = shoot(grids["user"], coord)
            valid = True
    return grids, hit

def userTurn(grids):
    print("YOUR TURN")
    coords = input("Input Coordinate: ").upper()
    try:
        xCoord = int(coords[0])
        yCoord = ALPHA_COORDS[coords[1]]
        valid = checkValidShot(grids["enemy"],(xCoord,yCoord))
    except ValueError:
        yCoord = ALPHA_COORDS[coords[0]]
        xCoord = int(coords[1]) 
        valid = checkValidShot(grids["enemy"],(xCoord,yCoord))
    except:
        valid = False
    while not valid:
        print("Enter a valid or unchecked coordinate from the enemy grid.")
        coords = input("Input Coordinate: ").upper()
        try:
            xCoord = int(coords[0])
            yCoord = ALPHA_COORDS[coords[1]]
            valid = checkValidShot(grids["enemy"],(xCoord,yCoord))
        except ValueError:
            yCoord = ALPHA_COORDS[coords[0]]
            xCoord = int(coords[1])
            valid = checkValidShot(grids["enemy"],(xCoord,yCoord))
        except:
            valid = False

    grids["enemy"],hit = shoot(grids["enemy"],(xCoord,yCoord))
    if hit:
        print("HIT\n")
    else:
        print("MISS\n")
    return grids

def gameTurn(grids):
    grids = userTurn(grids)
    print("ENEMY TURN")
    grids, hit = enemyTurn(grids)
    if hit:
        print("ENEMY HIT YOUR SHIP")
    else:
        print("ENEMY MISSED")
    returnGrids(grids["user"],grids["enemy"])
    return grids

won = False
print("WELCOME TO BATTLESHIPS")
grids = setup(10,10)
returnGrids(grids["user"],grids["enemy"])
while not won:
    grids = gameTurn(grids)
    done = True
    winner = "ENEMY"
    for i in grids["user"]:
        for j in "ABCDS":
            if j in i:
                done = False
                winner = "USER"
    if not done:
        done = True
        for i in grids["enemy"]:
            for j in "ABCDS":
                if j in i:
                    done = False
        if done:
            print(f"{winner} WINS!")
            won = True
    else:
        print(f"{winner} WINS!")
        won = True

