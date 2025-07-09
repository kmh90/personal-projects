import tkinter as tk
from tkinter import messagebox
import logging as log
import os, sys, time
# from pathlib import Path as path
import numpy as np

class TicTacToe:

    # First function to run to initiate game
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        # Start logging function
        self.start_logging()

        self.computer = False
        self.p_turn = "1"
        self.options = ["X", "O"]
        self.selected_option = tk.StringVar(self.master)
        self.selected_option.set(self.options[0])  # Default option
        self.player_symbol = self.selected_option.get()

        # Create map for mapping symbol to player score
        self.map = {
            "1" : {},
            "2" : {}
        }

        # Collate points
        self.p1_score = 0
        self.p2_score = 0

        self.app_logger.info("Setting up TIC TAC TOE game...")
        self.setup_game()
        self.app_logger.info("Completed game set up!")
    
    # Brings player back to main menu
    def main_menu(self):
        self.clear_all()
        self.setup_game()

    # Set up main menu and player selection
    def setup_game(self):

        # Create a main menu frame
        self.debug_logger.info("Creating a frame for the main menu...")
        mm_frame = tk.Frame(self.master)
        mm_frame.grid(row=0, column=0, padx=20, pady=20)
        self.debug_logger.info("Main menu frame creation completed!")

        self.debug_logger.info("Creating a frame for the main menu label...")
        mm_lbl_frame = tk.Frame(mm_frame)
        mm_lbl_frame.grid(row=0, column=0, padx=10, pady=40)
        self.debug_logger.info("Main menu label frame creation completed!")

        self.debug_logger.info("Creating main menu label...")
        mm_name = tk.Label(mm_lbl_frame, text="TIC TAC TOE", font=('Helvetica', 30))
        mm_name.grid(row=0, column=0)
        self.debug_logger.info("Main menu label creation completed!")

        # Create OptionMenu to select player symbol and set it
        self.debug_logger.info("Creating an option menu to choose player symbol for player 1...")
        option_lbl = tk.Label(mm_frame, text="P1 symbol: ", anchor='w')
        option_lbl.grid(row=1, column=0, sticky='w')
        self.option_menu = tk.OptionMenu(mm_frame, self.selected_option, *self.options, command=self.choose_sym)
        self.option_menu.grid(row=1, column=0)
        self.debug_logger.info("Option menu creation completed!")

        # If no options are chosen, set the following default symbols
        self.debug_logger.info("Setting player symbols...")
        self.app_logger.info("Player 1 chose " + self.player_symbol)
        
        self.map["1"]["sym"] = self.player_symbol
        
        p2_symbol = "O" if self.map["1"]["sym"] == "X" else "X"
        self.map["2"]["sym"] = p2_symbol
        self.app_logger.info("Player 2 symbol will be " + p2_symbol)

        # Set score mappings
        self.debug_logger.info("Initiating player scores...")
        self.map["1"]["score"] = self.p1_score
        self.map["2"]["score"] = self.p2_score

        # Add button to start the game
        self.debug_logger.info("Adding a main menu button for pvp game...")
        start_button = tk.Button(mm_frame, text="Start Player vs Player Game", command=self.start_game_pvp)
        start_button.grid(row=2, column=0)

        # Add button to start the game with computer
        self.debug_logger.info("Adding a main mennu button for players vs computer game...")
        start_button = tk.Button(mm_frame, text="Start Player vs Computer Game", command=self.start_game_comp)
        start_button.grid(row=3, column=0)

    # Set up player symbol if player selects the symbol to use
    def choose_sym(self, selected_val):

        self.app_logger.info("Manually choosing player symbol...")

        # Setup player and computer's details
        self.player_symbol = selected_val

        self.app_logger.info("Player 1 chose " + self.player_symbol + "!")
        
        self.map["1"]["sym"] = self.player_symbol
        
        p2_symbol = "O" if self.map["1"]["sym"] == "X" else "X"
        self.map["2"]["sym"] = p2_symbol
        self.app_logger.info("Player 2 symbol will be " + p2_symbol + "!")

    # Clears the board of all widgets
    def clear_all(self):
        # Delete all widgets in the main window
        self.debug_logger.debug("Deleting all widgets...")
        for widget in self.master.winfo_children():
            self.debug_logger.debug("Deleting " + f'{widget}' + "...")
            widget.destroy()

    # Start game with player
    def start_game_pvp(self):
        self.computer = False
        self.app_logger.info("Player vs player game!")
        self.app_logger.info("Player " + f'{self.p_turn}'  + " is starting the game!")
        self.update_label("Player " + f'{self.p_turn}' + "'s turn!")

        # Clear main window's widgets
        self.clear_all()
        self.start_game()

    # Start game with computer (toggle computer flag)
    def start_game_comp(self):
        self.computer = True
        self.app_logger.info("Player vs computer game!")

        # Randomize player's or computer's turn
        self.p_turn = str(np.random.randint(1,3))
        if self.p_turn == "1":
            self.debug_logger.info("Player " + f'{self.p_turn}' + " is starting the game!")
        else:
            self.debug_logger.info("Computer is starting the game!")

        # Clear main window's widgets
        self.clear_all()
        self.start_game()

        # Computer starts if p_turn is rolled to 2 randomly
        if self.p_turn == "2":
            self.computer_move()

    # Continues similar steps to start game
    def start_game(self):

        # Add a main frame once in game so that window resizing does not affect placements of objects
        self.debug_logger.info("Adding a frame for the game to negate window resizing...")
        self.game_main_frame = tk.Frame(self.master)
        self.game_main_frame.grid(row=0, column=0, padx=10, pady=10)

        # Add a button to go back to main menu
        self.debug_logger.info("Adding a back-to-main-menu button...")
        mm_button = tk.Button(self.game_main_frame, text="\u2190", width=2, height=1, command=self.main_menu)
        mm_button.grid(row=0, column=0)

        # Indicate which player's turn
        self.debug_logger.info("Adding a label to indicte which player's or computer's turn...")
        self.top_label = tk.Label(self.game_main_frame, text="Player " + f'{self.p_turn}' + "'s turn!")
        self.top_label.grid(row=0, column=1)

        # Add a button for player to quit game
        self.debug_logger.info("Adding a button to quit game...")
        quit_prompt = tk.Button(self.game_main_frame, text="\u241B", width=2, height=1, command=self.quit_game)
        quit_prompt.grid(row=0, column=2)

        # Set score labels
        self.debug_logger.info("Adding player scores into display...")
        p1_slbl_pos = "w"
        p1_score_label = tk.Label(self.game_main_frame, text="P1: " + f'{self.p1_score}', anchor=f'{p1_slbl_pos}')
        self.map["1"]["s_lbl"] = p1_score_label
        p1_score_label.grid(row=1, column=1, sticky=f'{p1_slbl_pos}')

        p2_slbl_pos = "e"
        if self.computer:
            p2_score_label = tk.Label(self.game_main_frame, text="C: " + f'{self.p2_score}', anchor=f'{p2_slbl_pos}')
        else:
            p2_score_label = tk.Label(self.game_main_frame, text="P2: " + f'{self.p2_score}', anchor=f'{p2_slbl_pos}')
        self.map["2"]["s_lbl"] = p2_score_label
        p2_score_label.grid(row=1, column=1, sticky=f'{p2_slbl_pos}')

        # Make a frame for the grid boxes so that they do not move
        self.debug_logger.info("Creating a minor frame to hold the grids together...")
        game_frame = tk.Frame(self.game_main_frame)
        game_frame.grid(row=2, column=1, padx=10, pady=10)

        # Create the game board
        self.debug_logger.info("Creating game board and buttons...")
        self.board = np.full((3, 3), "", dtype=str)

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(game_frame, text="", font=('Helvetica', 30), width=3, height=1,
                                                command=lambda row=i, col=j: self.make_move(row, col))
                self.buttons[i][j].grid(row=i, column=j)

    # Logging set up
    def start_logging(self):
        ttt_cwd = os.path.join(os.getcwd(), 'python-projects', 'tic_tac_toe')

        # Create logs dir if not there
        os.makedirs(os.path.join(ttt_cwd, "logs"), exist_ok=True)

        # Create app log file
        app_log_name = "ttt.log"
        self.app_log = os.path.join(ttt_cwd, "logs", app_log_name)

        # Create debug log
        debug_log_name = "ttt_debug.log"
        self.debug_log = os.path.join(ttt_cwd, "logs", debug_log_name)

        # Remove any existing log files
        if os.path.exists(self.app_log):
            os.remove(self.app_log)
        if os.path.exists(self.debug_log):
            os.remove(self.debug_log)

        # Create logger objects
        self.app_logger = log.getLogger('app')
        self.debug_logger = log.getLogger('app_debug')

        # Create and configure loggers
        self.app_logger.setLevel(log.INFO)
        self.debug_logger.setLevel(log.DEBUG)

        formatter = log.Formatter('%(asctime)s %(levelname)s - %(message)s')

        file_handler1 = log.FileHandler(self.app_log, mode='a')
        file_handler1.setFormatter(formatter)

        file_handler2 = log.FileHandler(self.debug_log, mode='a')
        file_handler2.setFormatter(formatter)

        # Add file handlers to loggers
        self.app_logger.addHandler(file_handler1)
        self.debug_logger.addHandler(file_handler2)

    # Logic for computer's moves
    def computer_move(self):

        self.app_logger.info("Computer's turn!")
        # Imitate computer's thinking
        self.update_label("Computer's turn!")
        self.master.after(500)  # Schedule the next update after 0.5 second (500 ms)
        
        winning_move = self.make_comp_win()
        if winning_move is not None:
            self.app_logger.info("Computer is making a winning move...")
            c_row = winning_move[0]
            c_col = winning_move[1]
        else:
            block_slot = self.check_near_winning()
            if len(block_slot) == 0:
                self.app_logger.info("Player is not winning so computer is making a random move...")
                # Look into more efficient ways to choose
                emp_slots = list(np.where(self.board == ""))        # Returns a list of two lists
                row_list = emp_slots[0]
                col_list = emp_slots[1]

                ind = np.random.randint(0,len(row_list))
                c_row = row_list[ind]
                c_col = col_list[ind]

                # c_row = np.random.randint(0,3)
                # c_col = np.random.randint(0,3)
            else:
                self.app_logger.info("Player seems to be winning. Computer is making a blocking move...")
                c_row = block_slot[0]
                c_col = block_slot[1]
        
        self.app_logger.info("Computer chose row " + f'{c_row}' + " and column " + f'{c_col}' + "!")

        if self.board[c_row][c_col] == "":

            self.app_logger.info("p_turn: " + f'{self.p_turn}')
            self.board[c_row][c_col] = self.map[f'{self.p_turn}']["sym"]
            self.buttons[c_row][c_col].config(text=self.map[f'{self.p_turn}']["sym"])
            if self.check_winner():
                self.app_logger.info("Computer has won!")
                messagebox.showinfo("Winner", f"Computer wins!")
                self.update_score("C")
                self.reset_board()
            elif self.check_draw():
                self.app_logger.info("It's a draw!")
                messagebox.showinfo("Draw", "It's a draw!")
                self.reset_board()
            else:
                self.app_logger.info("Moving on to the next turn...")
                self.p_turn = "1"
                self.app_logger.info("Player " + f'{self.p_turn}' + "'s turn!")
                self.update_label("Player " + f'{self.p_turn}' + "'s turn!")

        else:
            self.debug_logger.error("Position already filled! Computer choosing another position...")
            return self.computer_move()

    # Update the label to indicate player/computer's turn
    def update_label(self, txt):
        self.top_label.config(text=f'{txt}')
        self.master.update_idletasks() 

    # Update the scores of player/computer after the end of each round
    def update_score(self, pl):
        self.map[self.p_turn]["score"] += 1
        score = self.map[self.p_turn]["score"] 
        self.map[self.p_turn]["s_lbl"].config(text=pl + ": " + f'{score}')
        self.master.update_idletasks() 

    # Updates board after player's move. If computer flag is true, computer's turn automatically comes after player's turn
    def make_move(self, row, col):

        # self.app_logger.info("Player " + f'{self.p_turn}' + "'s turn!")
        # self.update_label("Player " + f'{self.p_turn}' + "'s turn!")
        self.app_logger.info("Player " + f'{self.p_turn}' + " chose row " + f'{row}' + " and column " + f'{col}' + "!")
        
        if self.board[row][col] == "":
            self.board[row][col] = self.map[f'{self.p_turn}']["sym"]
            self.buttons[row][col].config(text=self.map[f'{self.p_turn}']["sym"])
            if self.check_winner():
                self.app_logger.info(f"Player " + f'{self.p_turn}' + " wins!")
                messagebox.showinfo("Winner", f"Player " + f'{self.p_turn}' + " wins!")
                self.update_score("P" + f'{self.p_turn}')
                self.reset_board()
            elif self.check_draw():
                self.app_logger.info("It's a draw!")
                messagebox.showinfo("Draw", "It's a draw!")
                self.reset_board()
            else:
                self.app_logger.info("Moving on to the next turn...")
                
                self.p_turn = "2" if self.p_turn == "1" else "1"

                # Only run this code when User chooses player vs computer game
                if self.computer:
                    self.computer_move()
                else:
                    self.app_logger.info("Player " + f'{self.p_turn}' + "'s turn!")
                    self.update_label("Player " + f'{self.p_turn}' + "'s turn!")

        else:
            messagebox.showerror("Error", f"Position filled! Please choose another!")
            self.app_logger.error("Position already filled!")

    # Logic to make computer win (board is made from numpy)
    def make_comp_win(self):
        com_sym = self.map["2"]["sym"]
        self.app_logger.info("Computer is checking if it can win...")

        for i in range(3):
            if self.board[i].tolist().count(com_sym) == 2 and self.board[i].tolist().count("") == 1:
            # if self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                self.app_logger.info([i, self.board[i].tolist().index("")])
                return [i, self.board[i].tolist().index("")]
            col_list = [self.board[0][i], self.board[1][i], self.board[2][i]]
            if col_list.count(com_sym) == 2 and col_list.count("") == 1:
                self.app_logger.info([col_list.index(""), i])
                return [col_list.index(""), i]
        
        dia_list = [self.board[0][0], self.board[1][1], self.board[2][2]]
        if dia_list.count(com_sym) == 2 and dia_list.count("") == 1:
            self.app_logger.info([dia_list.index(""), dia_list.index("")])
            return [dia_list.index(""), dia_list.index("")]
        
        inv_dia_list = [self.board[0][2], self.board[1][1], self.board[2][0]]
        if inv_dia_list.count(com_sym) == 2 and inv_dia_list.count("") == 1:
            self.app_logger.info([inv_dia_list.index(""), -1*(inv_dia_list.index("")-2)])
            return [inv_dia_list.index(""), -1*(inv_dia_list.index("")-2)]

    # Logic for computer to check if player is winning
    def check_near_winning(self):
        self.app_logger.info("Computer is checking if player is winning...")

        block_pos = []
        # Check rows, columns, and diagonals for a close winner
        for i in range(3):
            # Checking rows
            if self.board[i][0] == self.board[i][1] != "" and self.board[i][2] == "":
                block_pos = [i, 2]
            elif self.board[i][0] == self.board[i][2] != "" and self.board[i][1] == "":
                block_pos = [i, 1]
            elif self.board[i][1] == self.board[i][2] != "" and self.board[i][0] == "":
                block_pos = [i, 0]
            # Checking columns
            if self.board[0][i] == self.board[1][i] != "" and self.board[2][i] == "":
                block_pos = [2, i]
            elif self.board[0][i] == self.board[2][i] != "" and self.board[1][i] == "":
                block_pos = [1, i]
            elif self.board[1][i] == self.board[2][i] != "" and self.board[0][i] == "":
                block_pos = [0, i]
        # Checking diagonal
        if self.board[0][0] == self.board[1][1] != "" and self.board[2][2] == "":
            block_pos = [2, 2]
        elif self.board[0][0] == self.board[2][2] != "" and self.board[1][1] == "":
            block_pos = [1, 1]
        elif self.board[1][1] == self.board[2][2] != "" and self.board[0][0] == "":
            block_pos = [0, 0]
        # Checking inverse diagonal
        if self.board[0][2] == self.board[1][1] != "" and self.board[2][0] == "":
            block_pos = [2, 0]
        elif self.board[0][2] == self.board[2][0] != "" and self.board[1][1] == "":
            block_pos = [1, 1]
        elif self.board[1][1] == self.board[2][0] != "" and self.board[0][2] == "":
            block_pos = [0, 2]
        
        return block_pos

    # Logic that checks if any side is winning after each turn
    def check_winner(self):
        # Check rows, columns, and diagonals for a winner
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != "":
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return True
        return False

    # Logic that checks if the game is a draw after each turn
    def check_draw(self):
        # Check if the board is full
        for row in self.board:
            for cell in row:
                if cell == "":
                    return False
        return True

    # Resets the board and proceeds to next round
    def reset_board(self):
        # Reset the board to its initial state
        for i in range(3):
            for j in range(3):
                self.board[i][j] = ""
                self.buttons[i][j].config(text="")

        # Determines who starts the next round
        self.p_turn = str(np.random.randint(1,3))
        if self.computer:
            if self.p_turn == "2":
                self.update_label("Computer's turn!")
                self.computer_move()
            else:
                self.update_label("Player " + f'{self.p_turn}' + "'s turn!") 

    # Quits the game
    def quit_game(self):
        self.master.quit()
    
if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
    print("Thank you for playing!")
