"""
MCTS starter code. This is the only file you'll need to modify, although
you can take a look at game1.py to get a sense of how the game is structured.

@author Bryce Wiedenbeck
@author Anna Rafferty (adapted from original)
@author Dave Musicant (adapted for Python 3 and other changes)
"""

# These imports are used by the starter code.
import random
import argparse
import game1
from game1 import *

# You will want to use this import in your code
import math

# Whether to display the UCB rankings at each turn.
DISPLAY_BOARDS = False 

# UCB_CONST value - you should experiment with different values
UCB_CONST = 0.5


class Node(object):
    """Node used in MCTS"""
    
    def __init__(self, state, parent_node):
        """Constructor for a new node representing game state
        state. parent_node is the Node that is the parent of this
        one in the MCTS tree. """
        self.state = state
        self.parent = parent_node
        self.children = {} # maps moves (keys) to Nodes (values); if you use it differently, you must also change addMove
        self.visits = 0
        self.value = float("nan")
        # Note: you may add additional fields if needed
        self.wins = 0
        
    def addMove(self, move):
        """
        Adds a new node for the child resulting from move if one doesn't already exist.
        Returns true if a new node was added, false otherwise.
        """
        if move not in self.children:
            state = self.state.nextState(move)
            self.children[move] = Node(state, self)
            return True
        return False
    
    def getValue(self):
        """
        Gets the value estimate for the current node. Value estimates should correspond
        to the win percentage for the player at this node (accounting for draws as in 
        the project description).
        """
        return self.value

    def updateValue(self, outcome):
        """Updates the value estimate for the node's state.
        outcome: +1 for 1st player win, -1 for 2nd player win, 0 for draw."""
        "*** YOUR CODE HERE ***"
        # NOTE: which outcome is preferred depends on self.state.turn()

        turn = self.state.getTurn()

        if outcome != turn: 
            self.wins += 1
        self.visits += 1

        self.value = self.wins/self.visits

    def UCBValue(self):
        """Value from the UCB formula used by parent to select a child. """
        "*** YOUR CODE HERE ***"

        return self.value + (UCB_CONST * math.sqrt(math.log((self.parent.visits))/self.visits))

    def maxNode(self):
        max_val = 0
        move = 0

        for child in self.children:
            current_val = self.children[child].UCBValue()
            if current_val > max_val:
                max_val = current_val
                move = child

        return move

def MCTS(root, rollouts):
    """Select a move by Monte Carlo tree search.
    Plays rollouts random games from the root node to a terminal state.
    In each rollout, play proceeds according to UCB while all children have
    been expanded. The first node with unexpanded children has a random child
    expanded. After expansion, play proceeds by selecting uniform random moves.
    Upon reaching a terminal state, values are propagated back along the
    expanded portion of the path. After all rollouts are completed, the move
    generating the highest value child of root is returned.
    Inputs:
        node: the node for which we want to find the optimal move
        rollouts: the number of root-leaf traversals to run
    Return:
        The legal move from node.state with the highest value estimate
    """
    "*** YOUR CODE HERE ***"

    # code is based on AIMA's pseudocode design of MCTS (using leaf to store 
    # selected node, child to store newly expanded node, and result to store
    # the result of simulating a game to a terminal state) pg.163
    for i in range(rollouts):
        leaf_node = selection(root)

        if not leaf_node.state.isTerminal():
            child = expansion(leaf_node)
            result = simulation(child)
        else:
            child = leaf_node.parent
            result = child.state.value()
        
        backpropogate(child, root, result)

    return root.maxNode()

def selection(node):
    """
    Starting at root node, choose a move (via UCB value),
    leading to a new successor node (repeat this) until you
    hit a terminal state. (selection)
    """
    possible_moves = node.state.getMoves()

    # not at a terminal state
    if len(possible_moves) != 0:
        
        # we run into a node we need to expand
        if len(node.children) != len(possible_moves):
            return node
        else:
            max_child = sorted(node.children.values(), key=Node.UCBValue, reverse = True)
            return selection(max_child[0])
    else:
        return node


def expansion(node):
    """
    Grow the tree by generating a new child of
    the selected node. (expansion).
    """

    current_state = node.state
    possible_moves = current_state.getMoves()

    # return first move successfully added
    for move in possible_moves:
        if node.addMove(move):
            return node.children[move]

def simulation(node):
    """"
    Perform a playout from the newly generated node
    choosing random moves until reaching a terminal state - not
    recording moves in tree. Needed to make a new random
    state function to not record moves in tree. (simulation)
    """

    current_state = node.state

    while not current_state.isTerminal():
        current_state = random_state(current_state)

    return current_state.value()

def backpropogate(node, root, result):
    """
    Update all values of visited nodes all the way back
    to the root node. (backpropogation)
    """

    while node != root:
        node.updateValue(result)
        node = node.parent
    
    root.updateValue(result)

def parse_args():
    """
    Parse command line arguments.
    """
    p = argparse.ArgumentParser()
    p.add_argument("--rollouts", type=int, default=0, help="Number of root-to-leaf "+\
                    "play-throughs that MCTS should run). Default=0 (random moves)")
    p.add_argument("--numGames", type=int, default=0, help="Number of games "+\
                    "to play). Default=1")
    p.add_argument("--second", action="store_true", help="Set this flag to "+\
                    "make your agent move second.")
    p.add_argument("--displayBoard", action="store_true", help="Set this flag to "+\
                    "make display the board at each MCTS turn with MCTS's rankings of moves.")
    p.add_argument("--rolloutsSecondMCTSAgent", type=int, default=0, help="If non-0, other player "+\
                    "will also be an MCTS agent and will use the number of rollouts set with this "+\
                    "argument. Default=0 (other player is random)")   
    p.add_argument("--ucbConst", type=float, default=.5, help="Value for the UCB exploration "+\
                    "constant. Default=.5") 
    args = p.parse_args()
    if args.displayBoard:
        global DISPLAY_BOARDS
        DISPLAY_BOARDS = True
    global UCB_CONST
    UCB_CONST = args.ucbConst
    return args


def random_move(node):
    """
    Choose a valid move uniformly at random.
    """
    move = random.choice(node.state.getMoves())
    node.addMove(move)
    return move

def random_state(state):
    """
    Chooose a valid move uniformly at random (without
    adding to the tree since this is required for 
    simulation).
    """
    random_move = random.choice(state.getMoves())
    new_state = state.nextState(random_move)

    return new_state

def run_multiple_games(num_games, args):
    """
    Runs num_games games, with no printing except for a report on which game 
    number is currently being played, and reports final number
    of games won by player 1 and draws. args specifies whether player 1 or
    player 2 is MCTS and how many rollouts to use. For multiple games, you
    probably do not want to include the --displayBoard option in args, as
    this will do lots of printing and make running relatively slow.
    """
    player1GamesWon = 0
    draws = 0
    for i in range(num_games):
        print("Game " + str(i))
        node = play_game(args)
        winner = node.state.value()
        if winner == 1:
            player1GamesWon += 1
        elif winner == 0:
            draws += 1
    print("Player 1 games won: " + str(player1GamesWon) + "/" + str(num_games))
    print("Draws: " + str(draws) + "/" + str(num_games))

def play_game(args):
    """
    Play one game against another player.
    args specifies whether player 1 or player 2 is MCTS (
    or both if rolloutsSecondMCTSAgent is non-zero)
    and how many rollouts to use.
    Returns the final terminal node for the game.
    """
    # Make start state and root of MCTS tree
    start_state = game1.new_game()
    root1 = Node(start_state, None)
    if args.rolloutsSecondMCTSAgent != 0:
        root2 = Node(start_state, None)

    # Run MCTS
    node = root1
    if args.rolloutsSecondMCTSAgent != 0:
        node2 = root2
    while not node.state.isTerminal():
        if (not args.second and node.state.turn == 1) or \
                (args.second and node.state.turn == -1):
            move = MCTS(node, args.rollouts)
            if DISPLAY_BOARDS:
                print(game1.show_values(node))
        else:
            if args.rolloutsSecondMCTSAgent == 0:
                move = random_move(node)
            else:
                move = MCTS(node2, args.rolloutsSecondMCTSAgent)
                if DISPLAY_BOARDS:
                    print(game1.show_values(node2))
        node.addMove(move)
        node = node.children[move]
        if args.rolloutsSecondMCTSAgent != 0:
            node2.addMove(move)
            node2 = node2.children[move]
    return node

            
    

def main():
    """
    Play a game of connect 4, using MCTS to choose the moves for one of the players.
    args on command line set properties; see parse_args() for details.
    """
    # Get commandline arguments
    args = parse_args()

    if args.numGames > 1:
        run_multiple_games(args.numGames, args)
    else:
        # Play the game
        node = play_game(args)
    
        # Print result
        winner = node.state.value()
        print(game1.print_board(node.state))
        if winner == 1:
            print("Player 1 wins")
        elif winner == -1:
            print("Player 2 wins")
        else:
            print("It's a draw")
            
            
if __name__ == "__main__":
    main()