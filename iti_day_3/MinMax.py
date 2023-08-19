import tkinter as tk
from tkinter import messagebox

HUMAN = -1
COMP = 1

# Create the game board
board = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]


def empty_cells(board):
    # Find all empty cells in the board
    cells = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                cells.append((i, j))
    return cells


def set_move(x, y, player):
    # Set the move for the specified player
    if valid_move(x, y):
        board[x][y] = player
        return True
    return False


def valid_move(x, y):
    # Check if the move is valid
    if (x, y) in empty_cells(board):
        return True
    return False


def wins(board, player):
    # Check if the player has won
    win_states = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[2][0], board[1][1], board[0][2]],
    ]
    if [player, player, player] in win_states:
        return True
    return False


def minimax(board, depth, player):
    # Minimax algorithm implementation
    if player == COMP:
        best = [-1, -1, -float("inf")]
    else:
        best = [-1, -1, float("inf")]

    if depth == 0 or game_over(board):
        score = evaluate(board)
        return [-1, -1, score]

    for cell in empty_cells(board):
        x, y = cell[0], cell[1]
        board[x][y] = player
        score = minimax(board, depth - 1, -player)
        board[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score
        else:
            if score[2] < best[2]:
                best = score

    return best


def evaluate(board):
    # Evaluate the board and return a score
    if wins(board, COMP):
        score = 1
    elif wins(board, HUMAN):
        score = -1
    else:
        score = 0
    return score


def game_over(board):
    # Check if the game is over
    if wins(board, HUMAN) or wins(board, COMP):
        return True
    for row in board:
        for cell in row:
            if cell == 0:
                return False
    return True


# Create the GUI using Tkinter
class TicTacToeGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.buttons = []
        self.create_board()
        self.is_game_over = False
        self.current_player = HUMAN
        self.h_choice = "X"
        self.c_choice = "O"
        self.first = True

    def create_board(self):
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(
                    self.window,
                    text="",
                    font=("Helvetica", 20),
                    width=6,
                    height=3,
                    command=lambda x=i, y=j: self.make_move(x, y),
                )
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)

    def make_move(self, x, y):
        if self.buttons[x][y]["text"] == "" and not self.is_game_over:
            if self.current_player == HUMAN:
                self.buttons[x][y]["text"] = self.h_choice
                set_move(x, y, HUMAN)
                self.current_player = COMP
                if not game_over(board):
                    self.ai_turn()
                if game_over(board):
                    self.end_game()
                    return

   
    def ai_turn(self):
        depth = len(empty_cells(board))
        if depth == 0 or game_over(board):
            return

        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]

        set_move(x, y, COMP)

        self.buttons[x][y]["text"] = self.c_choice

        if wins(board, COMP):
            self.end_game()
        elif len(empty_cells(board)) == 0 or game_over(board):
            self.end_game()

    def end_game(self):
        self.is_game_over = True
        if wins(board, HUMAN):
            messagebox.showinfo("Game Over", "You win!")
        elif wins(board, COMP):
            messagebox.showinfo("Game Over", "Computer wins!")
        else:
            messagebox.showinfo("Game Over", "It's a draw!")

# Create an instance of the TicTacToeGUI class
gui = TicTacToeGUI()

# Start the main event loop
gui.window.mainloop()