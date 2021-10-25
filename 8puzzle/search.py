from puzzle8 import *

tiles = [1, 2, 3, 8, 0, 4, 7, 6, 5]

def numWrongTiles(state):
    misplaced_tiles = 0

    if state == 247893796:
        return 0
    else:
        for i in range(9):
            if (getTile(state,i) == 0):
                pass
            elif (getTile(state, i) != tiles[i]):
                misplaced_tiles+=1
    return misplaced_tiles


def manhattanDistance(state):
    total_manhattan_distance = 0
    goal = solution()

    if state == 247893796:
        return 0
    else:
        for i in range(9):
            if getTile(state, i) == 0:
                pass
            elif getTile(state, i) != tiles[i]:
                tiles_index = 0
                x_coord_state = xylocation(i)[0]
                y_coord_state = xylocation(i)[1]
                for tile in tiles:
                    if tile != getTile(state, i):
                        tiles_index+=1
                    else:
                        break
                x_coord_goal = xylocation(tiles_index)[0]
                y_coord_goal = xylocation(tiles_index)[1]       
                x_distance = abs(x_coord_goal - x_coord_state)
                y_distance = abs(y_coord_goal - y_coord_state)
                total_manhattan_distance += x_distance + y_distance
                
    print(total_manhattan_distance)
    return total_manhattan_distance