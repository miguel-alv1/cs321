from puzzle8 import *
from queue import PriorityQueue
from queue import Queue
import time

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
                
    # print(total_manhattan_distance)
    return total_manhattan_distance


def astar(state, heuristic):
    # priority queue initially has the start
    priority_Queue = PriorityQueue()
    goal = solution()

    priority_Queue.put([heuristic(state), [state, 0, []]])

    startTime = time.time()
    while not priority_Queue.empty():
        current_state = priority_Queue.get()
        curr_blank_sq = blankSquare(current_state[1][0])

        moves = neighbors(curr_blank_sq)

        if current_state[1][0] == goal:
            break
        
        for move in moves:
            new_leaf_node = []
            new_state = moveBlank(current_state[1][0], move)
            blank_square = blankSquare(new_state)
            depth = current_state[1][1] + 1
            path = current_state[1][2].copy()
            path.append(new_state)
            new_leaf_node.append(new_state)
            new_leaf_node.append(depth)
            new_leaf_node.append(path)
            current_cost =  current_state[1][1] + heuristic(current_state[1][0])
            priority_Queue.put([current_cost, new_leaf_node])

    print(startTime)
    return current_state[1][2]