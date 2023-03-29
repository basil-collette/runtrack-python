
import random
from enum import Enum

class LocType(Enum):
    EMPTY = '_'
    RED = 'O'
    YELLOW = 'X'
    
def check_win(board, row_pos, col_pos, player_color):
    # Check horizontal
    for r in range(len(board)):
        for c in range(len(board[0]) - 3):
            if board[r][c] == player_color and board[r][c+1] == player_color and board[r][c+2] == player_color and board[r][c+3] == player_color:
                return True

    # Check vertical
    for r in range(len(board) - 3):
        for c in range(len(board[0])):
            if board[r][c] == player_color and board[r+1][c] == player_color and board[r+2][c] == player_color and board[r+3][c] == player_color:
                return True

    # Check diagonal (down-right)
    for r in range(len(board) - 3):
        for c in range(len(board[0]) - 3):
            if board[r][c] == player_color and board[r+1][c+1] == player_color and board[r+2][c+2] == player_color and board[r+3][c+3] == player_color:
                return True

    # Check diagonal (up-right)
    for r in range(3, len(board)):
        for c in range(len(board[0]) - 3):
            if board[r][c] == player_color and board[r-1][c+1] == player_color and board[r-2][c+2] == player_color and board[r-3][c+3] == player_color:
                return True

    return False
    
def get_col_next_free_row_index(board, col_index):
    free = False
    row_index = -1
    
    while free == False:
        if (row_index+1 == len(board) or (board[row_index+1][col_index] != LocType.EMPTY.value)):
            free = True
        else:
            row_index += 1
        
    return row_index
    
def put_token(board, row_index, col_index, player_color):
        if (board[row_index][col_index] == LocType.EMPTY.value):
            board[row_index][col_index] = player_color
        else:
            raise Exception('position déjà occupée!')
    
class AI_One:
    def __init__(self, self_color):
        self.self_color = self_color
        self.enemy_color = LocType.RED if (self_color == LocType.YELLOW) else LocType.YELLOW
        
    def count_nearby_same_color(self, board, row, col):
        count = 0
        for r in range(max(0, row-1), min(len(board), row+2)):
            for c in range(max(0, col-1), min(len(board[0]), col+2)):
                if board[r][c] == self.self_color.value:
                    count += 1
        return count
        
    def get_best_col_index(self, board, locked_columns):
        col_index = [-1]
        col_score = 0
        for i in range(len(board[0])):
            
            if i in locked_columns:
                continue
            
            free_row_index_of_col_i = get_col_next_free_row_index(board, i)
            if(free_row_index_of_col_i == -1):
                continue
            i_score = self.count_nearby_same_color(board, free_row_index_of_col_i, i)
            
            if (i_score == col_score and col_index != [-1]):
                col_index.append(i)
                
            if (i_score > col_score):
                col_index = [i]
                col_score = i_score
                
        if (col_score == 0):
            return -1
                
        if (len(col_index) > 1):
            random_index = col_index[random.randint(0, len(col_index)-1)]
            col_index = [random_index]
        
        return col_index[0]
        
    def get_win_index_by_color(self, board, color):
        for i in range(len(board[0])):
            copy_board = [[i for i in row] for row in board]
            
            free_row_index_of_col_i = get_col_next_free_row_index(copy_board, i)
            if(free_row_index_of_col_i == -1):
                continue
            
            put_token(copy_board, free_row_index_of_col_i, i, color)
            
            if (check_win(copy_board, free_row_index_of_col_i, i, color) == True):
                return i
                
        return -1
        
    def think(self, board):
        #check if has win possibility
        self_win_index = self.get_win_index_by_color(board, self.self_color.value)
        if (self_win_index != -1):
            return self_win_index
        
        #return col of enemy future winning
        enemy_win_index = self.get_win_index_by_color(board, self.enemy_color.value)
        if (enemy_win_index != -1):
            return enemy_win_index
            
        #return col with the best amout of self_color nearby
        best_col_index = self.get_best_col_index(board, [])
        
        if(best_col_index == -1):
            #return random near the middle
            return random.randint(2, len(board[0])-3)
        
        #repeat step untill best_col_index not permit player to win
        locked_columns = []
        unsafe = True
        while (unsafe == True):
            best_col_index = self.get_best_col_index(board, locked_columns)
            copy_board = [[i for i in row] for row in board]
            free_row_index_of_col_i = get_col_next_free_row_index(copy_board, best_col_index)
            if(free_row_index_of_col_i == -1):
                locked_columns.append(best_col_index)
                continue
            put_token(copy_board, free_row_index_of_col_i, best_col_index, self.self_color.value)
            index = self.get_win_index_by_color(copy_board, self.enemy_color.value)
            if (index != -1):
                locked_columns.append(best_col_index)
            else:
                unsafe = False
        
        return best_col_index

class Board:
    def __init__(self, cols_amount, rows_amount, enemyAI, playerAI):
        if (cols_amount < 4 or rows_amount < 4):
            raise Exception('les valeures doivent être d\'au moins 4!')
        self.cols = cols_amount #width
        self.rows = rows_amount #height
        self.boardstate = [['_' for i in range(self.cols)] for j in range(self.rows)]
        self.tour = 0
        
        self.enemyAI = enemyAI
        #if (self.enemyAI == True):
            #self.enemyAI
        
        self.current_player = None
        #if (playerAI == True):
            #self.current_player = None
        
        self.is_running = False
        self.board_print()

    def board_print(self):
        col_indexes = [str(i) for i in range(self.cols)]
        print('TOUR ' + str(self.tour) + " _________________________________________________________________________")
        print(' ' + ' '.join(col_indexes))
        for i in range(self.rows):
            print('|' + '|'.join(self.boardstate[i]) + '|')
        print(' ' + ' '.join(col_indexes))
            
    def set_player_turn(self):
        self.current_player = LocType.RED if (self.current_player == LocType.YELLOW) else LocType.YELLOW
        
    def end_game(self):
        self.is_running = False
        print(self.current_player.name + '(' + str(self.current_player.value) + ') a gagné !')
        
    def let_player_play(self):
        col_index = None
        inserted = False
        response = input('Joueur ' + str(self.current_player.name) + '(' + str(self.current_player.value) + '), choisissez un numéro de colonne:')
        
        while (inserted == False):
            if (response.isdigit() == False or (int(response) < 0) or (int(response) > self.cols-1)):
                response = input("Erreur: inscrivez un chiffre, de 0 à " + str(self.cols-1) + " compris:")
            else:
                col_index = int(response)
                insert_row_index = get_col_next_free_row_index(self.boardstate, col_index)
                
                if (insert_row_index == -1):
                    reponse = input("Erreur: la colonne est remplie! Selectionnez un autre numéro de colone:")
                else:
                    inserted = True
        
        return col_index
    
    def start(self):
        self.current_player = LocType.RED if (random.randint(0, 1) == 1) else LocType.YELLOW
        self.is_running = True
        
        enemyAiInstance = None
        if (self.enemyAI == True):
            enemy_color = LocType.RED if (random.randint(0, 1) == 1) else LocType.YELLOW
            enemyAiInstance = AI_One(enemy_color)
        
        while self.is_running == True:
            col_index = None
            
            if LocType.EMPTY.value in (item for sublist in self.boardstate for item in sublist) == False:
                print("Match nul!")
                self.is_running = False
            
            if (self.enemyAI == True and self.current_player == enemyAiInstance.self_color):
                col_index = enemyAiInstance.think(self.boardstate)
            else:
                col_index = self.let_player_play()
            
            row_index = get_col_next_free_row_index(self.boardstate, col_index)
            put_token(self.boardstate, row_index, col_index, self.current_player.value)
            self.board_print()
            
            if (check_win(self.boardstate, row_index, col_index, self.current_player.value)):
                self.end_game()
                return
            
            self.set_player_turn()
            self.tour += 1

game = Board(7, 6, True, False)
game.start()
