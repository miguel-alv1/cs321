import unittest
import puzzle8
import search
import random
import time

class TestMethods(unittest.TestCase):

    offTwoPuzzle = puzzle8.state([3,4,5,2,0,6,1,8,7])

    gradePuzzle1 = puzzle8.state([8,7,6,5,4,3,2,1,0])
    gradePuzzle2 = puzzle8.state([1,2,3,4,5,6,7,8,0])
    

    def setUp(self):
        self.gradePuzzles = [247860748,253206748,253780508,152293420,
                             300501380, 108306836]
        self.pathLengths = [2,4,8,10,12,16]

    def testAstarGradingNumWrongTiles(self):
        print("A* num wrong tiles")
        startTime = time.time()
        for i in range(len(self.gradePuzzles)):
            print("\nTrying to find a solution for puzzle with solution of depth",
                  self.pathLengths[i])
            print("Starting puzzle:")
            puzzle8.display(self.gradePuzzles[i])
            solnPath = search.astar(self.gradePuzzles[i],
                                    search.numWrongTiles)
            print("Found a solution, of depth", len(solnPath))
            print("Solution path:", solnPath)
            self.assertEqual(len(solnPath),self.pathLengths[i])
        print('A* num time',time.time()-startTime)
        print('\n')

    def testAstarGradingManhattan(self):
        print("A* Manhattan distance")
        startTime = time.time()
        for i in range(len(self.gradePuzzles)):
            print("\nTrying to find a solution for puzzle with solution of depth",
                  self.pathLengths[i])
            print("Starting puzzle:")
            puzzle8.display(self.gradePuzzles[i])
            solnPath = search.astar(self.gradePuzzles[i],
                                    search.manhattanDistance)
            print("Found a solution, of depth", len(solnPath))
            print("Solution path:", solnPath)
            self.assertEqual(len(solnPath),self.pathLengths[i])
        print('A* Manhattan time',time.time()-startTime)
        print('\n')



if __name__=='__main__':
    unittest.main()