import tkinter as tk
from tkinter import messagebox
import numpy as np
import random
from time import sleep

# Creates an empty board
def create_board():
    return(np.zeros((3, 3)))

# Check for empty places on board
def possibilities(board):
    l = []
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0:
                l.append((i, j))
    return l

# Select a random place for the player
def random_place(board, player):
    selection = possibilities(board)
    current_loc = random.choice(selection)
    board[current_loc] = player
    return board

# Checks whether the player has three of their marks in a horizontal row
def row_win(board, player):
    for x in range(len(board)):
        win = True
        for y in range(len(board)):
            if board[x, y] != player:
                win = False
                break
        if win == True:
            return win
    return win

# Checks whether the player has three of their marks in a vertical row
def col_win(board, player):
    for x in range(len(board)):
        win = True
        for y in range(len(board)):
            if board[y][x] != player:
                win = False
                break
        if win == True:
            return win
    return win

# Checks whether the player has three of their marks in a diagonal row
def diag_win(board, player):
    win = True
    for x in range(len(board)):
        if board[x, x] != player:
            win = False
    if win:
        return win
    win = True
    if win:
        for x in range(len(board)):
            y = len(board) - 1 - x
            if board[x, y] != player:
                win = False
    return win

# Evaluates whether there is a winner or a tie
def evaluate(board):
    winner = 0
    for player in [1, 2]:
        if (row_win(board, player) or col_win(board, player) or diag_win(board, player)):
            winner = player
    if np.all(board != 0) and winner == 0:
        winner = -1
    return winner

# Recursive function to determine the optimal move for the computer player
def minimax(board, depth, maximizing_player):
    if depth == 0 or evaluate(board) != 0:
        return evaluate(board)

    if maximizing_player:
        max_eval = float('-inf')
        for move in possibilities(board):
            board_copy = board.copy()
            board_copy[move] = 2
            eval = minimax(board_copy, depth - 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in possibilities(board):
            board_copy = board.copy()
            board_copy[move] = 1
            eval = minimax(board_copy, depth - 1, True)
            min_eval = min(min_eval, eval)
        return min_eval

# Main function to start the game
def play_game():
    board, winner, counter = create_board(), 0, 1
    while winner == 0:
        if counter % 2 != 0:
            board = random_place(board, 1)
        else:
            best_score = float('-inf')
            best_move = None
            for move in possibilities(board):
                board_copy = board.copy()
                board_copy[move] = 2
                score = minimax(board_copy, 9, False)
                if score > best_score:
                    best_score = score
                    best_move = move
            board[best_move] = 2
        update_buttons(board)
        winner = evaluate(board)
        if winner != 0:
            break
        counter += 1

    if winner == -1:
        messagebox.showinfo("Game Over", "It's a tie!")
    else:
        messagebox.showinfo("Game Over", f"Player {winner} wins!")

def update_buttons(board):
    for i in range(3):
        for j in range(3):
            button_text = ""
            if board[i][j] == 1:
                button_text = "X"
            elif board[i][j] == 2:
                button_text = "O"
            buttons[i][j].config(text=button_text, state="disabled")

# Create the main window
root = tk.Tk()
root.title("Tic-Tac-Toe")

# Create the buttons for the game board
buttons = []
board = create_board()
for i in range(3):
    row_buttons = []
    for j in range(3):
        button = tk.Button(root, text="", width=10, height=5)
        button.grid(row=i, column=j, padx=5, pady=5)
        row_buttons.append(button)
    buttons.append(row_buttons)

# Bind the button click event
def on_button_click(row, col):
    if board[row][col] == 0:
        board[row][col] = 1
        update_buttons(board)
        winner = evaluate(board)
        if winner == 0:
            play_game()
        elif winner == -1:
            messagebox.showinfo("Game Over", "It's a tie!")
        else:
            messagebox.showinfo("Game Over", f"Player {winner} wins!")
    else:
        messagebox.showinfo("Invalid Move", "Please select an empty cell.")

for i in range(3):
    for j in range(3):
        buttons[i][j].config(command=lambda row=i, col=j: on_button_click(row, col))

# Start the main loop
root.mainloop()