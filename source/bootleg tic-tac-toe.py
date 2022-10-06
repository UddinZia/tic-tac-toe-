import tkinter as tk
#from tkinter import ttk
from PIL import Image, ImageTk
from random import choice
from enum import Enum

class WinType(Enum):
    TIE = -1
    PLAYER_1 = 0
    PLAYER_2 = 1
    AI = 2


class TicTacToe():
    window = tk.Tk()
    game_started = False
    p1 = True # player 1's turn
    ai_enabled = False
    hard_mode = True 
    winner = None
    board = []
    choices = [i for i in range(9)]
    image_empty = None
    image_x = None
    image_o = None
    game_over_dialogue = {
        WinType.PLAYER_1: "Player 1 won!",
        WinType.PLAYER_2: "Player 2 won!",
        WinType.AI: "AI won!",
        WinType.TIE: "it's a tie!"
    }

    def start(self):
        self.create_main_window()
        self.get_player_number()
        self.game_started = True
        emptytile_file = Image.open("tile_empty.png").resize((100, 100))
        self.image_empty = ImageTk.PhotoImage(emptytile_file)
        xtile_file = Image.open("tile_x.png").resize((100, 100))
        self.image_x = ImageTk.PhotoImage(xtile_file)
        otile_file = Image.open("tile_o.png").resize((100, 100))
        self.image_o = ImageTk.PhotoImage(otile_file)
        self.window.mainloop()

    def create_main_window(self):
        self.window.geometry("300x300")
        self.window.title("Bootleg Tic Tac Toe")
        self.window.resizable(False, False)

    def update_players(self, ai: bool):
        self.ai_enabled = ai

    def reset_game(self):
        for row in self.board:
            for button in row:
                button.destroy()

        self.choices = [i for i in range(9)]
        self.board = []
        self.winner = None
        self.game_started = False
        self.p1 = True
        
    
    def get_player_number(self):
        if self.winner:
            self.reset_game()
            
        one_player_button = tk.Button(self.window, text="1 Player", justify=tk.LEFT)
        two_player_button = tk.Button(self.window, text="2 Players", justify=tk.RIGHT)

        one_player_button.configure(command=lambda x=True:[self.update_players(x), two_player_button.destroy(), one_player_button.destroy(), self.select_difficulty()])
        two_player_button.configure(command=lambda x=False:[self.update_players(x), one_player_button.destroy(), two_player_button.destroy(), self.add_game_buttons()])

        one_player_button.place(x=40, y=140)
        two_player_button.place(x=160, y=140)

    def update_difficulty(self, hard: bool):
        self.hard_mode = hard

    def select_difficulty(self):
        normal = tk.Button(self.window, text="Normal", justify=tk.LEFT)
        hard = tk.Button(self.window, text="Hard", justify=tk.RIGHT)

        normal.configure(command=lambda x=False:[self.update_difficulty(x), hard.destroy(), normal.destroy(), self.add_game_buttons()])
        hard.configure(command=lambda x=True:[self.update_difficulty(x), normal.destroy(), hard.destroy(), self.add_game_buttons()])

        normal.place(x=100, y=120)
        hard.place(x=110, y=160)

    def add_game_buttons(self):
        print(self.board)
        for row_index, _y in enumerate([0, 100, 200]):
            row = []
            for col_index, _x in enumerate([0, 100, 200]):
                new_button = tk.Button(self.window, image=self.image_empty, text="", bg="white", highlightthickness=0, borderwidth=0, bd=0, command=lambda r=row_index,c=col_index: self.update(r, c))
                new_button.image = self.image_empty
                row.append(new_button)
                new_button.place(x=_x, y=_y)
            self.board.append(row)

    def win_sequence(self, win_dialogue: str, tied: bool):
        win_window = tk.Toplevel()
        win_window.geometry("200x225")
        win_window.title("tic-tac-toe")
        win_text = tk.Label(win_window, text=win_dialogue, justify=tk.CENTER)
        if tied:
            win_image_file = Image.open("tie_image.png")
        else:
            win_image_file = Image.open("win_image.png")
        win_image = ImageTk.PhotoImage(win_image_file)
        win_image_onwindow = tk.Label(win_window, image=win_image)
        win_image_onwindow.image = win_image
        win_image_onwindow.place(x=55, y=70)
        win_text.pack(pady=20)
        replay = tk.Button(win_window, text="Play Again", command=lambda:[win_window.destroy(), self.get_player_number()])
        replay.place(x=50, y=180)

    def get_win_type(self, token_type):
        if (token_type == "X"):
            return WinType.PLAYER_1
        elif (token_type == "O" and self.ai_enabled):
            return WinType.AI
        else:
            return WinType.PLAYER_2

    def did_win(self, game_board) -> WinType:
        # check cols 
        for col in range(3):
            cntr = 0
            currVal = game_board[0][col]["text"]
            for row in range(3):
                if game_board[row][col]["text"] == "":
                    break
                if game_board[row][col]["text"] == currVal:
                    cntr += 1
                if cntr == 3:
                    return self.get_win_type(currVal)
            
        # check rows
        for row in range(3):
            token_type = game_board[row][0]["text"]
            counter = 0
            for col in range(3):
                if game_board[row][col]["text"] == "":
                    break
                if game_board[row][col]["text"] == token_type:
                    counter += 1
            if (counter == 3):
                return self.get_win_type(token_type)

        # check diagonals
        if (game_board[0][0]["text"] == game_board[1][1]["text"] and game_board[1][1]["text"] == game_board[2][2]["text"] and game_board[0][0]["text"] != ""):
            token_type = game_board[0][0]["text"]
            return self.get_win_type(token_type)
        if (game_board[0][2]["text"] == game_board[1][1]["text"] and game_board[1][1]["text"] == game_board[2][0]["text"] and game_board[0][2]["text"] != ""):
            token_type = game_board[0][2]["text"]
            return self.get_win_type(token_type)
        
        return None if len(self.choices) != 0 else WinType.TIE

    # generate random number
    # divide by 3 for row
    # remainder gives col 
    # loop until we find one that isnt taken
    def do_ai_move(self):
        print(f"hard_mode={self.hard_mode}")
        if not self.hard_mode:
            pos = choice(self.choices)
            self.choices.remove(pos)

            col = pos % 3
            row = pos // 3
            self.board[row][col]["text"] = "O"
            self.board[row][col]["image"] = self.image_o
        else:
            board_copy = self.board.copy()
            
            # win if possible
            for r in range(3):
                for c in range(3):
                    if board_copy[r][c]["text"] == "":
                        board_copy[r][c]["text"] = "O"
                        if self.did_win(board_copy) == WinType.AI:
                            self.board[r][c]["text"] = "O"
                            self.board[r][c]["image"] = self.image_o
                            return
                        else:
                            board_copy[r][c]["text"] = ""
            
            # block player from winning
            for r in range(3):
                for c in range(3):
                    if board_copy[r][c]["text"] == "":
                        board_copy[r][c]["text"] = "X"
                        if self.did_win(board_copy) == WinType.PLAYER_1:
                            self.board[r][c]["text"] = "O"
                            self.board[r][c]["image"] = self.image_o
                            self.choices.remove(r*3 + c)
                            return
                        else:
                            board_copy[r][c]["text"] = ""
            
            # try to take corner
            for r,c in [[0,0], [0,2], [2,0], [2,2]]:
                if board_copy[r][c]["text"] == "":
                    self.board[r][c]["text"] = "O"
                    self.board[r][c]["image"] = self.image_o
                    self.choices.remove(r*3 + c)
                    return
            
            # try to take center
            if board_copy[1][1]["text"] == "":
                self.board[1][1]["text"] = "O"
                self.board[1][1]["image"] = self.image_o
                self.choices.remove(4)
                return

            # take random from left right up down
            pos = choice(self.choices)
            self.choices.remove(pos)
            col = pos % 3
            row = pos // 3
            self.board[row][col]["text"] = "O"
            self.board[row][col]["image"] = self.image_o

        

    def update(self, x, y) -> bool:
        print(x, y)
        if (self.winner != None): return

        token = self.board[x][y]["text"]

        if (token == "" and self.p1):
            self.board[x][y]["text"] = "X"
            self.board[x][y]["image"] = self.image_x
            self.choices.remove(x*3 + y)
            self.p1 = False
            self.winner = self.did_win(self.board)
            print(self.winner)
        
            if (not self.winner and self.ai_enabled and self.choices):
                self.do_ai_move()
                self.p1 = True
                self.winner = self.did_win(self.board)
                print(self.winner)

        elif (token == "" and not self.p1):
            self.board[x][y]["text"] = "O"
            self.board[x][y]["image"] = self.image_o
            self.choices.remove(x*3 + y)
            self.p1 = True
            self.winner = self.did_win(self.board)
            print(self.winner)

        
        if (self.winner):
            self.win_sequence(self.game_over_dialogue[self.winner], self.winner == WinType.TIE)

    # TODO: tie screen
game = TicTacToe()
game.start()
    



