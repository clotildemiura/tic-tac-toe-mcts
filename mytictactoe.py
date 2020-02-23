import numpy as np
import random

from mctspy.tree.nodes import TwoPlayersGameMonteCarloTreeSearchNode
from mctspy.tree.search import MonteCarloTreeSearch
from mctspy.games.examples.tictactoe import TicTacToeGameState, TicTacToeMove




#Class to run an interactive game 
class MyTicTacToe():
    
    def __init__(self, interactive=True, n_sim = 1000, policy = 'mcts', verbose=True):
        self.board = [i for i in range(0,9)]
        self.moves=[[1,7,3,9],[5],[2,4,6,8]] # Corners, Center and Others, respectively
        self.winners = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)) #winner combination
        self.tab= range(1,10) # Table
        self.chars = ('X','O') #player is 'X', computer is 'O'
        self.interactive = interactive #wether or not the game is interactive
        self.n_sim = n_sim # the number of simulations to perform with Monte Carlo tree search algorithm if the game is not interactive
        self.policy = policy #if not interactive, policy of agent 
        #either mcts or the same basic policy as the 'computer' ie the opponent
        self.verbose = verbose #if True display the board evolution
        self.final_result = None #1 for victory, 0 for draw and -1 for loss
        
    def print_verbose(self, x, end=''):
        if self.verbose:
            print(x, end=end)
    
   
    def print_board(self):
        if self.verbose:
            '''print the board after each move'''
            x=1
            for i in self.board:
                end = ' | '
                if x%3 == 0:
                    end = ' \n'
                    if i != 1: end+='---------\n';
                char=' '
                if i in ('X','O'): char=i;
                x+=1
                print(char,end=end)
            
    def space_exist(self):
        #check for existing space in the board
        return self.board.count('X') + self.board.count('O') != 9
    
    def can_move(self,  move):
        '''
        Check for valid move
        
        parameter: move is a number in 1-9
        '''
        if move in self.tab and self.board[move-1] == move-1: #board is from 0 to 8
            return True
        return False
    
    def can_win(self, player, move):
        """
        Return if the move of player is a winner one.
        """
        
        places=[]
        x=0
        for i in self.board:
            if i == player: places.append(x);
            x+=1
        win=True
        for tup in self.winners:
            win=True
            for ix in tup:
                if self.board[ix] != player:
                    win=False
                    break
            if win == True:
                break
        return win
        
    
    def make_move(self, player, move, undo=False):
        '''
        Return a tuple of boolean. Fisrt one : True if we made a valid move
        Second one: True if it's a winner one
        '''
        if self.can_move(move): #check the validity of the move
            self.board[move-1] = player # we make the move
            win=self.can_win(player, move) #check if the move is a winner one
            if undo:
                self.board[move-1] = move-1
            return (True, win)
        return (False, False)
    
    def computer_move(self):
        '''
        Define the policy of the computer
        If it can win it plays the winner move
        If player can win it blocks him
        Otherwise it just takes a random place in the board
        '''
        move=-1
        # If I can win, others don't matter.
        for i in range(1,10):
            if self.make_move(self.computer, i, True)[1]: #the second element of the tuple returned by make_move is a boolean win
                move=i
                break
        if move == -1:
            # If player can win, block him.
            for i in range(1,10):
                if self.make_move(self.player, i, True)[1]:
                    move=i
                    break
        if move == -1:
            # Otherwise, try to take one of desired places.
            copy_moves = self.moves.copy()
            random.shuffle(copy_moves) #introduce randomization
            for liste in copy_moves:
                random.shuffle(liste)
                for mv in liste:
                    if move == -1 and self.can_move(mv):
                        move=mv
                        break
        return self.make_move(self.computer, move)
    
    
    def basic_move(self):
        '''
        Exact  same policy as the computer but played by the agent
        '''
        move=-1
        # If I can win, others don't matter.
        for i in range(1,10):
            if self.make_move(self.player, i, True)[1]: #the second element of the tuple returned by make_move is a boolean win
                move=i
                break
        if move == -1:
            # If player can win, block him.
            for i in range(1,10):
                if self.make_move(self.computer, i, True)[1]:
                    move=i
                    break
        if move == -1:
            # Otherwise, try to take one of desired places.
            copy_moves = self.moves.copy()
            random.shuffle(copy_moves) #introduce randomization
            for liste in copy_moves:
                random.shuffle(liste)
                for mv in liste:
                    if move == -1 and self.can_move(mv):
                        move=mv
                        break
        return self.make_move(self.player, move)
    
    
    
    
    
    def board_transformation(self):
        '''
        return the board but in the format understood by mcts package
        ie a 2D array with 1 for the player and -1 for the computer
        Remind that the board is a list of len 9 with marked moved = 'X' for the player and 'O' for the computer
        '''
        b=self.board.copy()
        b = [0 if type(i) == int else i for i in b] # all the digits are replaced with 0 (the empty cases)
        b = [1 if i=='X' else -1 if i=='O' else i for i in b] #replace X by 1 and '0' by -1
        return np.array(b).reshape(3,3) #reshape in a two day array
    
        
    def best_move_mcts(self):
    
        '''
        used if the game is not interactive.
        return the best move to play according to a monte carlo tree search 
        parameters: n_sim is the number of simulation runed by the MCTS algorithm
        '''
        #need to transform the current board in a 2D numpy array
        current_state = self.board_transformation()
        initial_board_state = TicTacToeGameState(state = current_state, next_to_move=1)
        
        #define the root of the monte carlo tree search ie the current state
        root = TwoPlayersGameMonteCarloTreeSearchNode(state = initial_board_state)
        
        #perform mcts 
        mcts = MonteCarloTreeSearch(root)
        new_state = mcts.best_action(self.n_sim).state.board #give the new 2D array corresponding to new state after optimal move
        #new_state and current_state only differ at one element
        
        #need to extract the position of this element and to convert it into a number between 1-9
        new_move = np.argmax((new_state-current_state).reshape(1,9))+1
        assert new_move in np.arange(1,10)
        return new_move
        
            
            
    def play(self):
        self.player, self.computer = self.chars
        self.print_verbose('Player is [%s] and computer is [%s]' % (self.player, self.computer), end='\n')
        result='%%% Draw! %%%'
        self.final_result = 0
        
        #who starts? 
        start = np.random.choice([1,-1])
        if start ==-1: #the computer starts
            self.print_verbose('Computer starts', end='\n')
            self.computer_move()
        else:
            self.print_verbose('Player starts', end='\n')
        
        while self.space_exist():
            
            self.print_board()
            self.print_verbose('# Make your move ! [1-9] : ', end='\n')
            
            if self.interactive:
                move = int(input()) #ask the player to enter a move
                moved, won = self.make_move(self.player, move)
            else:
                if self.policy =='mcts':
                    move = self.best_move_mcts() #best move according to mcts algorithm
                    moved, won = self.make_move(self.player, move)
                else:
                    moved, won = self.basic_move()
            if not moved:
                self.print_verbose(' >> Invalid number ! Try again !')
                continue
            #
            if won:
                result='*** Congratulations ! You won ! ***'
                self.final_result = 1
                break
            elif self.computer_move()[1]:
                result='=== You lose ! =='
                self.final_result = -1
                break;
        
        self.print_board()
        self.print_verbose(result)
        
        
    
    