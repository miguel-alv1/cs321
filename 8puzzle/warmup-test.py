import unittest
import puzzle8
import random
import search

class TestMethods(unittest.TestCase):

    offTwoPuzzle = puzzle8.state([3,4,5,2,0,6,1,8,7])

    gradePuzzle1 = puzzle8.state([8,7,6,5,4,3,2,1,0])
    gradePuzzle2 = puzzle8.state([1,2,3,4,5,6,7,8,0])


    def setUp(self):
        self.gradePuzzles = [247860748,253206748,253780508,152293420,
                             300501380, 108306836]


    def test1NumWrongTilesM(self):
        random.seed(12345)
        self.assertEqual(search.numWrongTiles(puzzle8.solution()),0)
        self.assertEqual(search.numWrongTiles(puzzle8.randomState(1)),1)
        self.assertEqual(search.numWrongTiles(self.offTwoPuzzle),8)

    def test2NumWrongTilesE(self):
        self.assertEqual(search.numWrongTiles(self.gradePuzzle2),4)
        self.assertEqual(search.numWrongTiles(self.gradePuzzle1),8)

    def test3ManhattanDistanceM(self):
        random.seed(12345)
        self.assertEqual(search.manhattanDistance(puzzle8.solution()),0)
        self.assertEqual(search.manhattanDistance(puzzle8.randomState(1)),1)
        self.assertEqual(search.manhattanDistance(self.offTwoPuzzle),16)

    def test4ManhattanDistanceE(self):
        self.assertEqual(search.manhattanDistance(self.gradePuzzle1),18)
        self.assertEqual(search.manhattanDistance(self.gradePuzzle2),8)

if __name__=='__main__':
    unittest.main()