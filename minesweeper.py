
import random
import re
class MBoard:
    def __init__(self, board_sz, bombs):
        self.board_sz = board_sz
        self.bombs = bombs

        self.board = self.create_new_board()
        self.neighbour_value()

        self.uncovered = set()
    
    def create_new_board(self):
        board = [[None for _ in range(self.board_sz)] for _ in range(self.board_sz)]

        bombs_placed = 0
        while bombs_placed < self.bombs:
            location = random.randint(0, self.board_sz**2 - 1)
            row = location//self.board_sz
            col = location % self.board_sz

            if board[row][col] != '*':
                board[row][col] = '*'
                bombs_placed += 1
        
        return board

    def neighbour_value(self):
        for r in range(self.board_sz):
            for c in range(self.board_sz):
                if self.board[r][c] != '*':
                    self.board[r][c] = self.get_neighbour_bombs(r,c)
        
        print(self.board)
    
    def get_neighbour_bombs(self, r, c):

        n_bombs = 0
        for row in range(max(0, r-1), min(self.board_sz-1, r+1)+1):
            for col in range(max(0, c-1), min(self.board_sz-1, c+1)+1):
                if (row == r and col == c):
                    continue
                if(self.board[row][col] == "*"):
                    n_bombs += 1

        return n_bombs
    
    def uncover(self, r, c):

        self.uncovered.add((r,c))

        if self.board[r][c] == '*':
            return False
        elif self.board[r][c] > 0:
            return True
        
        for row in range(max(0, r-1), min(self.board_sz-1, r+1)+1):
            for col in range(max(0, c-1), min(self.board_sz-1, c+1)+1):
                if (row, col) not in self.uncovered:
                    self.uncover(row, col)

        return True
    
    def __str__(self):
        #prints the board when calling print
        output_board = [[None for _ in range(self.board_sz)] for _ in range(self.board_sz)]

        for r in range(self.board_sz):
            for c in range(self.board_sz):
                if (r,c) in self.uncovered:
                    output_board[r][c] = str(self.board[r][c])
                else:
                    output_board[r][c] = ' '
        
        output_str = '   0   1   2   3   4   5   6   7   8   9\n_________________________________________\n'

        for r in range(self.board_sz):
            output_str = output_str + str(r) + "| "
            for c in range(self.board_sz):
                output_str = output_str + output_board[r][c] + " | "

            output_str = output_str + "\n"
        
        output_str = output_str + '_________________________________________\n'
        return output_str

def play(board_sz = 10, bombs = 10):
    board = MBoard(board_sz, bombs)

    unexploded = True
    while len(board.uncovered) < board.board_sz ** 2 - bombs:
        print(board)
        user_in = re.split(',(\\s)*', input("Which cell do you want to uncover? Input as row,col: "))
        row, col = int(user_in[0]), int(user_in[-1])
        if(row < 0 or row >= board.board_sz or col < 0 or col >= board.board_sz):
            #add dynamic size to tell user
            print("Invalid location. Out of bounds of board. Try again.")
            continue

        unexploded = board.uncover(row, col)
        if not unexploded:
            break
    
    if unexploded:
        print("Congratulations!!! you won")
    else:
        print("GAME OVER!!! :(")
        board.uncovered = [(r,c) for r in range(board.board_sz) for c in range(board.board_sz)]
        print(board)

if __name__ == "__main__":
    play()