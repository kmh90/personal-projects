import tkinter as tk
from tkinter import messagebox
import logging as log
import os, sys
import numpy as np
# import Player as pl
# import Board as brd

class Game:
    # First function to run to initiate game
    def __init__(self, main):
        self.main = main
        self.main.title("Connect Four")

        # Start logging function
        # self.start_logging()
        log = AppLogger()
        log.start_logging()
        self.app_logger = log.get_app_logger()
        self.debug_logger = log.get_debug_logger()

        self.computer = False
        self.p_turn = "1"

        # Setting how many to connect to win game
        self.connect_opts = ["4", "5", "6", "7"]
        self.selected_cnct_opt = tk.StringVar(self.main)
        self.selected_cnct_opt.set(self.connect_opts[0])  # Default option

        # Setting options for height of board
        self.board_size_opts = ["4", "5", "6", "7"]
        self.selected_size = tk.StringVar(self.main)
        self.selected_size.set(self.board_size_opts[0])  # Default option

        # Setting options for height of board
        # self.height_opts = ["4", "5", "6", "7"]
        # self.selected_height = tk.StringVar(self.main)
        # self.selected_height.set(self.height_opts[1])  # Default option

        # Setting options for width of board
        # self.width_opts = ["4", "5"]
        # self.selected_width = tk.StringVar(self.main)
        # self.selected_width.set(self.width_opts[1])  # Default option

        # Setting options for player 1 symbol
        self.sym_options = ["X", "O"]
        self.selected_sym = tk.StringVar(self.main)
        self.selected_sym.set(self.sym_options[0])   # Default option

        self.app_logger.info("Setting up Connect Four game...")
        self.setup_game()
        self.app_logger.info("Completed Connect Four game set up!")

    # Logging set up
    def start_logging(self):
        cf_cwd = os.path.join(os.getcwd(), 'python-projects', 'connect_four')

        # Create logs dir if not there
        os.makedirs(os.path.join(cf_cwd, "logs"), exist_ok=True)

        # Create app log file
        app_log_name = "connect_four.log"
        self.app_log = os.path.join(cf_cwd, "logs", app_log_name)

        # Create debug log
        debug_log_name = "connect_four_debug.log"
        self.debug_log = os.path.join(cf_cwd, "logs", debug_log_name)

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

    # Set up main menu and player selection
    def setup_game(self):

        # GAME GUI SETUP START

        # Create a main menu frame
        self.debug_logger.info("Creating a frame for the main menu...")
        mm_frame = tk.Frame(self.main)
        mm_frame.grid(row=0, column=0, padx=20, pady=20)
        self.debug_logger.info("Main menu frame creation completed!")

        self.debug_logger.info("Creating a frame for the main menu label...")
        mm_lbl_frame = tk.Frame(mm_frame)
        mm_lbl_frame.grid(row=0, column=0, padx=10, pady=40)
        self.debug_logger.info("Main menu label frame creation completed!")

        self.debug_logger.info("Creating main menu label...")
        mm_name = tk.Label(mm_lbl_frame, text="Connect four", font=('Helvetica, sans serif', 30))
        mm_name.grid(row=0, column=0)
        self.debug_logger.info("Main menu label creation completed!")

        # self.debug_logger.info("Creating start game label...")
        # start_game_lbl = tk.Label(mm_frame, text="Start game:", font=('Helvetica, sans serif', 15), anchor='w')
        # start_game_lbl.grid(row=1, column=0, sticky='w')
        # self.debug_logger.info("Start game label completed!")

        # Add button to start the game
        self.debug_logger.info("Adding a main menu button for pvp game...")
        start_button = tk.Button(mm_frame, text="Start Player vs Player Game", command=self.start_game_pvp)
        start_button.grid(row=1, column=0, pady=5)

        # Add button to start the game with computer
        self.debug_logger.info("Adding a main mennu button for players vs computer game...")
        start_button = tk.Button(mm_frame, text="Start Player vs Computer Game", command=self.start_game_comp)
        start_button.grid(row=2, column=0, pady=5)

        self.debug_logger.info("Creating an Options label...")
        options_lbl = tk.Label(mm_frame, text="Options:", font=('Helvetica, sans serif', 13), anchor='w')
        options_lbl.grid(row=4, column=0, sticky='w', pady=(10, 5))
        self.debug_logger.info("Options label completed!")

        # Create OptionMenu to select player symbol and set it
        player_sym_opt_loc = 5  # Determines which row the button will appear in the GUI
        self.debug_logger.info("Creating an option menu to choose player symbol for player 1...")
        player_sym_opt_lbl = tk.Label(mm_frame, text="P1 symbol: ", anchor='w')
        player_sym_opt_lbl.grid(row=player_sym_opt_loc, column=0, sticky='w')
        self.player_sym_opt_menu = tk.OptionMenu(mm_frame, self.selected_sym, *self.sym_options, command=self.choose_sym)
        self.player_sym_opt_menu.grid(row=player_sym_opt_loc, column=0)
        self.debug_logger.info("Option menu creation completed!")

        # Create OptionMenu to select how many connecting tokens to win
        conn_tokens_opt_loc = 6  # Determines which row the button will appear in the GUI
        self.debug_logger.info("Creating an option menu to choose number of connecting tokens...")
        conn_tokens_opt_lbl = tk.Label(mm_frame, text="No. of connecting tokens: ", anchor='w')
        conn_tokens_opt_lbl.grid(row=conn_tokens_opt_loc, column=0, sticky='w')
        self.conn_tokens_opt_menu = tk.OptionMenu(mm_frame, self.selected_cnct_opt, *self.connect_opts, command=self.choose_num_of_conn_tokens)
        self.conn_tokens_opt_menu.grid(row=conn_tokens_opt_loc, column=0)
        self.debug_logger.info("Number of connecting tokens menu creation completed!")

        # Create OptionMenu to select board size
        size_opt_loc = 7
        self.debug_logger.info("Creating an option menu to choose size of the board...")
        size_option_lbl = tk.Label(mm_frame, text="Board size ", anchor='w')
        size_option_lbl.grid(row=size_opt_loc, column=0, sticky='w')
        self.size_option_menu = tk.OptionMenu(mm_frame, self.selected_size, *self.board_size_opts, command=self.choose_board_size)
        self.size_option_menu.grid(row=size_opt_loc, column=0)

        # Create OptionMenu to select board height
        # self.debug_logger.info("Creating an option menu to choose height of the board...")
        # ht_option_lbl = tk.Label(mm_frame, text="Board height ", anchor='w')
        # ht_option_lbl.grid(row=4, column=0, sticky='w')
        # self.ht_option_menu = tk.OptionMenu(mm_frame, self.selected_height, *self.height_opts, command=self.choose_height)
        # self.ht_option_menu.grid(row=4, column=0)

        # Create OptionMenu to select board width
        # self.debug_logger.info("Creating an option menu to choose width of the board...")
        # wd_option_lbl = tk.Label(mm_frame, text="Board width ", anchor='w')
        # wd_option_lbl.grid(row=5, column=0, sticky='w')
        # self.wd_option_menu = tk.OptionMenu(mm_frame, self.selected_width, *self.width_opts, command=self.choose_width)
        # self.wd_option_menu.grid(row=5, column=0)

        # GAME GUI SETUP END

        # Creating player objects and adding mapping
        self.p1 = Player()
        self.p2 = Player()

        self.map = {
            "1" : self.p1,
            "2" : self.p2
        }

        # Setting player name
        self.p1.set_name("P1")  # Default player 1 name if not chosen
        self.p2.set_name("P2")  # Default player 2 name if not chosen

        # If no options are chosen, set the following default symbols
        self.debug_logger.info("Setting player symbols...")

        p1_symbol = self.selected_sym.get()
        self.p1.set_sym(p1_symbol)
        self.app_logger.info("Player 1 chose " + self.p1.get_sym())
        
        p2_symbol = "O" if self.p1.get_sym() == "X" else "X"
        self.p2.set_sym(p2_symbol)
        self.app_logger.info("Player 2 symbol will be " + self.p2.get_sym())

        # Set score mappings
        self.debug_logger.info("Initiating player scores...")
        self.p1.set_score(0)
        self.p2.set_score(0)

        # Set up backend game board
        self.debug_logger.info("Creating game board and buttons...")
        h = int(self.selected_size.get())  # Height of board
        w = int(self.selected_size.get())   # Width of board
        self.brd1 = Board()
        self.brd1.set_width(w)  # Set width of board
        self.brd1.set_height(h) # Set height of board


    # Set up player symbol if player selects the symbol to use
    def choose_sym(self, selected_val):

        self.app_logger.info("Manually choosing player symbol...")

        # Setup player's/computer's details

        # p1_symbol = self.selected_sym.get()
        p1_symbol = selected_val
        self.p1.set_sym(p1_symbol)
        self.app_logger.info("Player 1 chose " + p1_symbol + "!")
        
        p2_symbol = "O" if self.p1.get_sym() == "X" else "X"
        self.p2.set_sym(p2_symbol)
        self.app_logger.info("Player 2 symbol will be " + p2_symbol + "!")

    # Allows player to choose number of connecting tokens to win
    def choose_num_of_conn_tokens(self, selected_num_of_conn_tokens):

        self.debug_logger.debug("Manually configuring number of connecting tokens to win...")

        self.selected_cnct_opt.set(selected_num_of_conn_tokens)

        self.app_logger.info("Number of connecting tokens to win is set to" + f'{self.selected_cnct_opt}')

        if int(selected_num_of_conn_tokens) > self.brd1.get_height():
            self.debug_logger.debug("Number of connecting tokens is more than board size so setting board size to " + f'{selected_num_of_conn_tokens}')
            self.choose_board_size(int(selected_num_of_conn_tokens))

        self.app_logger.info("Board size set to" + f'{self.selected_cnct_opt}')

    # Allows player to choose board size (height == width)
    def choose_board_size(self, selected_brd_size):
        
        self.app_logger.info("Manually configuring board's size...")

        num_of_conn_tokens = self.selected_cnct_opt.get()

        if int(num_of_conn_tokens) > int(selected_brd_size):
            messagebox.showerror("Error", f"Board size must be more than or equals to {num_of_conn_tokens}!")
            board_size = int(num_of_conn_tokens)

        else:
            board_size = int(selected_brd_size)

        self.selected_size.set(board_size)  # Have to set selected board size as returning back to main menu will read the current option in the optionMenu
        self.brd1.set_height(board_size)
        self.brd1.set_width(board_size)

        self.app_logger.info("Board's height and width set to " + f'{board_size}')

    # Allows player to choose height of the board
    # def choose_height(self, selected_height):

    #     self.app_logger.info("Manually configuring board's height...")

    #     h = int(selected_height)

    #     self.brd1.set_height(h)

    #     self.app_logger.info("Board's height set to " + f'{h}')

    # # Allows player to choose width of the board
    # def choose_width(self, selected_width):

    #     self.app_logger.info("Manually configuring board's width...")

    #     w = int(selected_width)

    #     self.brd1.set_width(w)

    #     self.app_logger.info("Board's width set to " + f'{w}')

    # Start game with player
    def start_game_pvp(self):
        self.computer = False
        self.app_logger.info("Player vs player game!")

        p_name = self.map[f'{self.p_turn}'].get_name()
        self.app_logger.info(f'{p_name}' + " is starting the game!")

        # Clear main window's widgets
        self.clear_all()
        self.start_game()

    # Start game with computer (toggle computer flag)
    def start_game_comp(self):
        self.computer = True
        self.app_logger.info("Player vs computer game!")

        # Set computer as P2 name
        self.p2.set_name("Computer")

        # Randomize player's or computer's turn
        self.p_turn = str(np.random.randint(1,3))
        if self.p_turn == "1":
            p_name = self.p1.get_name()
        else:
            p_name = self.p2.get_name()

        self.app_logger.info(f'{p_name}' + " is starting the game!")

        # Clear main window's widgets
        self.clear_all()
        self.start_game()

        # Computer starts if p_turn is rolled to 2 randomly
        if self.p_turn == "2":
            self.comp_move()

    # Continues similar steps to start game
    def start_game(self):

        # Add a main frame once in game so that window resizing does not affect placements of objects
        self.debug_logger.info("Adding a frame for the game to negate window resizing...")
        self.game_main_frame = tk.Frame(self.main)
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

        # Include text to mention how many consecutive tokens to win a game
        self.debug_logger.info("Adding label to mention how many consecutive tokens to win a game...")
        self.row1_label = tk.Label(self.game_main_frame, text=f"Match {self.selected_cnct_opt.get()} tokens to win!", font=("Helvetica", 8))
        self.row1_label.grid(row=1, column=1)

        # Set score labels
        self.debug_logger.info("Adding player scores into display...")
        p1_slbl_pos = "w"
        p1_score_label = tk.Label(self.game_main_frame, text=f'{self.p1.get_name()}' + ": " + f'{self.p1.get_score()}', anchor=f'{p1_slbl_pos}')
        self.p1.set_score_label(p1_score_label)
        p1_score_label.grid(row=2, column=1, sticky=f'{p1_slbl_pos}')

        p2_slbl_pos = "e"
        p2_score_label = tk.Label(self.game_main_frame, text=f'{self.p2.get_name()}' + ": " + f'{self.p2.get_score()}', anchor=f'{p2_slbl_pos}')
        self.p2.set_score_label(p2_score_label)
        p2_score_label.grid(row=2, column=1, sticky=f'{p2_slbl_pos}')

        # Make a frame for the grid boxes so that they do not move
        self.debug_logger.info("Creating a minor frame to hold the grids together...")
        game_frame = tk.Frame(self.game_main_frame)
        game_frame.grid(row=3, column=1, padx=10, pady=10)

        # Create the game board
        self.debug_logger.info("Creating game board and buttons...")
        self.brd1.create()      # Create board

        # Set up frontend game board
        self.buttons = [[None for _ in range(self.brd1.get_height())] for _ in range(self.brd1.get_width())]
        for i in range(self.brd1.get_width()):
            for j in range(self.brd1.get_height()):
                # self.buttons[i][j] = tk.Button(game_frame, text="", font=('Helvetica', 15), width=3, height=1,
                #                                 command=lambda row=i, col=j: self.make_move(row, col))
                self.buttons[i][j] = tk.Button(game_frame, text="", font=('Helvetica', 15), width=3, height=1,
                                                command=lambda col=j: self.make_move(col))
                self.buttons[i][j].grid(row=i, column=j)

        # Indicate whose turn
        # p_name = self.map[f'{self.p_turn}'].get_name()
        # self.update_label(f'{p_name}' + "'s turn!")

    # Updates board after player's move. If computer flag is true, computer's turn automatically comes after player's turn
    def make_move(self, col):

        p_name = self.map[f'{self.p_turn}'].get_name()

        self.app_logger.info(f'{p_name}' + " chose column " + f'{col}' + "!")
        sym = self.map[f'{self.p_turn}'].get_sym()
        row = self.brd1.update_board(col, sym)   # Update board and returns back the row for the column being updated
        board = self.brd1.get_board()
        # print(row)
        if row is not None:     # Runs this section if row value is an integer

            # sym = self.map[f'{self.p_turn}'].get_sym()
            board[row][col] = f'{sym}'
            self.buttons[row][col].config(text=f'{sym}')

            if self.check_winner():

                self.app_logger.info(f'{p_name}' + " wins!")
                messagebox.showinfo("Winner", f'{p_name}' + " wins!")
                self.update_score(f'{p_name}')
                self.reset_board()

            elif self.check_draw():

                self.app_logger.info("It's a draw!")
                messagebox.showinfo("Draw", "It's a draw!")
                self.reset_board()

            else:

                self.app_logger.info("Moving on to the next turn...")
                self.p_turn = "2" if self.p_turn == "1" else "1"

                if self.computer and self.p_turn == "2":
                    # Only run this code when User chooses player vs computer game
                    self.comp_move()

                else:

                    p_name = self.map[f'{self.p_turn}'].get_name()

                    self.app_logger.info(f'{p_name}' + "'s turn!")
                    self.update_label(f'{p_name}' + "'s turn!")

        elif row is None:       # Runs this section if column is filled and method returns None
            
            if self.computer and self.p_turn == 2:
            
                return False
            
            else:
            
                messagebox.showerror("Error", f"Position filled! Please choose another!")
                self.app_logger.error("Position already filled!")

    # Logic for computer's moves
    def comp_move(self):

        # Get board's width
        brd_width = self.brd1.get_width()

        # Get all symbols
        p1_sym = self.p1.get_sym()
        comp_sym = self.p2.get_sym()

        self.app_logger.info("Computer's turn!")
        # Imitate computer's thinking
        self.update_label("Computer's turn!")
        self.main.after(500)  # Schedule the next update after 0.5 second (500 ms)

        # Check if computer can win. Else check if player is going to win
        self.app_logger.info("Computer is checking for a suitable slot...")
        slot = self.get_slot(comp_sym)

        if type(slot) == list:  # If there are more than 1 slots to choose from, check if player is winning and block
            self.app_logger.info("Too many slots to choose so computer is checking if there is a need to block player from winning...")
            slot1 = self.get_slot(p1_sym)
            if type(slot1) == list: # If there are still too many slots to choose from, choose a random slot
                self.app_logger.info("No slots to win or block so computer is choosing a safe random slot...")
                safe_ind = np.random.randint(0,len(slot1))
                c_col = slot1[safe_ind]
            else:
                c_col = slot1
        else:
            c_col = slot

        self.debug_logger.info("Computer chose column " + f'{c_col}' + "!")

        if self.make_move(c_col) is False:
            self.app_logger.info("Column " + f'{c_col}' + " is full so computer is choosing another position")
            self.comp_move()    # Computer to choose another position if column is already filled up

    # SMALL FUNCTIONS

    # Brings player back to main menu
    def main_menu(self):
        self.clear_all()
        self.setup_game()

    # Clears the board of all widgets
    def clear_all(self):
        # Delete all widgets in the main window
        self.debug_logger.debug("Deleting all widgets...")
        for widget in self.main.winfo_children():
            self.debug_logger.debug("Deleting " + f'{widget}' + "...")
            widget.destroy()

    # Update the label to indicate player/computer's turn
    def update_label(self, txt):
        self.top_label.config(text=f'{txt}')
        self.main.update_idletasks()

    # Update the scores of player/computer after the end of each round
    def update_score(self, player):
        self.map[self.p_turn].add_score()
        score = self.map[self.p_turn].get_score()
        self.map[self.p_turn].get_score_label().config(text=f'{player}' + ": " + f'{score}')
        self.main.update_idletasks()

    # Logic for computer to check if player is winning
    def get_slot(self, sym):
        self.app_logger.info("Computer is choosing a slot...")

        # p1_sym = self.p1.get_sym()
        
        connect_amt = int(self.selected_cnct_opt.get())  # How many tokens to connect to consider a win
        target_num = connect_amt - 1  # Amount of tokens a player align needs before winning
        diff = connect_amt - 1    # Difference in index positions between starting index and last index to check

        board = self.brd1.get_board()
        ht = self.brd1.get_height()
        wd = self.brd1.get_width()

        # List of columns to not add in for 1) player to win 2) player to block comp winning
        no_add_col = set()      
        unf_cols = self.brd1.get_unf_cols().copy()     # Current list of unfilled columns
        # self.debug_logger.debug("Unfiltered unfilled columns: %s", unf_cols)

        # Firstly, check whether there is only 1 column left to choose
        if len(unf_cols) == 1:  # If there is only 1 column left to choose
            last_col = unf_cols[0]
            # self.app_logger.info("Aww no choice but only column %s left to choose!", last_col)
            return last_col
        
        # Check rows, columns, and diagonals

        # Check columns
        self.app_logger.info("Checking if anyone is going to win in a column...")
        board_t = board.T   # Transpose the board so that columns becomes rows
        for col_num, full_col in enumerate(board_t):
            self.app_logger.debug("Checking column %s...", col_num)
            col_tracker = 0
            col_empty_slot = False      # Checking if there is an empty slot right in front of target_num consecutive slots in a column
            for col_ele in full_col:
                if col_ele == sym:
                    col_tracker += 1
                    self.app_logger.debug("There are %s consecutive tokens!", col_tracker)
                    if col_tracker == target_num and col_empty_slot == True:      # To handle cases where an empty slot is in front of target_num consecutive slots in a column
                        break
                elif col_ele == "":
                    col_empty_slot = True
                else:
                    col_empty_slot = False      # Set to False if intended token is not found
                    col_tracker = 0             # Reset column tracker

            
            if col_tracker == target_num and col_empty_slot is True:
                self.app_logger.info("Someone is going to win in column %s!", col_num)
                return col_num

        # Check rows
        self.app_logger.info("Checking if anyone is going to win in a row...")
        for row_num, full_row in enumerate(board):

            self.app_logger.debug("Checking row %s...", row_num)
            
            row_tracker = 0
            # row_empty_slot = "" in full_row     # Returns True if there are empty slots. Else, returns False
            r_empty_slot_ind = None
            r_ins = []    # Columns to insert

            for row_ind in range(len(full_row)):
                row_ele = full_row[row_ind]
                if row_ele == sym:
                    row_tracker += 1
                    self.app_logger.debug("There are %s consecutive tokens!", row_tracker)
                    if row_tracker == target_num and r_empty_slot_ind is not None:  # If there is an empty slot before target_num of consecutive slots, add it to the list of columns to insert
                        r_ins.append(r_empty_slot_ind)
                elif row_ele == "":
                    # r_empty_slot_ind = np.argwhere(full_row == row_ele).tolist()[0][0]       # np.argwhere returns an ndarray e.g. [[2]]. So we need to convert to list and extract. np.where returns a tuple instead so we can also use list(np.where()) to convert to list
                    r_empty_slot_ind = row_ind
                    if row_tracker == target_num:
                        r_ins.append(r_empty_slot_ind)
                        # Reset row tracker to 0 if there is more than 1 set of near-winning windows
                        # E.g. _ X X X _ X X X _
                        row_tracker = 0
                    # row_empty_slot = True
                else:
                    r_empty_slot_ind = None     # Reset to None since empty slot won't be adjacent to target_num of consecutive slots
                    row_tracker = 0
            
            self.app_logger.debug("Columns to insert to win in row %s: %s", row_num, r_ins)

            for ins in r_ins:
                col_vac = self.brd1.get_col_vacancy(ins)
                if row_num + 1 == col_vac:    # Insert to win/block
                    self.app_logger.info("Computer will insert in row %s on column %s!", row_num, ins)
                    return ins
                elif row_num + 2 == col_vac:  # Check if there is an empty slot in the column index below the said row. If there is, DO NOT add it. Else, player will win/block comp winning
                    self.app_logger.debug("Computer will take note not to add in column %s!", ins)
                    no_add_col.add(ins)
        
        # Check diagonals
        min_offset = connect_amt - ht
        max_offset = wd - connect_amt
        
        self.app_logger.info("Checking if anyone is going to win in a diagonal...")
        for off in range(min_offset, max_offset + 1):
            
            d_empty_slot_ind = None
            d_ins = []    # Columns to insert in diagonal

            diag = np.diagonal(board, offset=off).tolist()
            self.app_logger.debug("Checking diagonal with offset %s: %s", off, diag)
            
            diag_tracker = 0
            # diag_empty_slot = False
            for diag_ind in range(len(diag)):
                diag_ele = diag[diag_ind]
                if diag_ele == sym:
                    diag_tracker += 1
                    self.app_logger.debug("There are %s consecutive tokens!", diag_tracker)
                    if diag_tracker == target_num and d_empty_slot_ind is not None:  # If there is an empty slot before target_num of consecutive slots, add it to the list of columns to insert
                        d_ins.append(d_empty_slot_ind)
                elif diag_ele == "":
                    if off > 0:     # To handle diagonals with offset more than 0 since the index will start at 0 but in reality we need to add the offset
                        d_empty_slot_ind = diag_ind + off
                    else:
                        d_empty_slot_ind = diag_ind

                    # self.debug_logger.debug("Empty diagonal slot found at %s", d_empty_slot_ind)
                    if diag_tracker == target_num:
                        d_ins.append(d_empty_slot_ind)
                        diag_tracker= 0
                    # diag_empty_slot = True
                else:
                    d_empty_slot_ind = None     # Reset to None since empty slot won't be adjacent to target_num of consecutive slots
                    diag_tracker = 0

            self.app_logger.debug("Columns to insert to win in diagonal with offset %s: %s", off, d_ins)

            for ins_d in d_ins:
                self.app_logger.info("Someone is going to win in a diagonal of offset %s!", off)
                col_vac_1 = self.brd1.get_col_vacancy(ins_d)
                
                # Example: If I have a winning player slot at offset 1 and index 1, computer should check if at column 1 there is 1 empty slot
                # O _ O O _
                # X O X O _
                # O X X X O
                # O X O O X
                # O X O O O

                if ins_d - off + 1 == col_vac_1:
                    self.app_logger.info("Computer is inserting in column %s", ins_d)
                    return ins_d
                elif ins_d - off + 2 == col_vac_1:  # Check if there is an empty slot in the column index below the said row. If there is, DO NOT add it. Else, player will win/block comp winning
                    self.app_logger.info("Computer is taking note to not add in column %s", ins_d)
                    no_add_col.add(ins_d)

        # Check inverse diagonals
        self.app_logger.info("Checking if anyone is going to win in an inverse diagonal...")
        brd_flip = np.fliplr(board)
        for off_inv in range(min_offset, max_offset + 1):
            
            invd_empty_slot_ind = None
            invd_ins = []    # Columns to insert in inverse diagonal

            invd = np.diagonal(brd_flip, offset=off_inv).tolist()
            self.app_logger.debug("Checking inverse diagonal with offset %s: %s", off_inv, invd)
            
            invd_tracker = 0

            for invd_ind in range(len(invd)):
                invd_ele = invd[invd_ind]
                orig_ind = len(invd) - 1 - invd_ind     # Original index on the board = (Size of inverse diagonal - 1) - Inverse diagonal index
                if invd_ele == sym:
                    invd_tracker += 1
                    self.app_logger.debug("There are %s consecutive tokens!", invd_tracker)
                    if invd_tracker == target_num and invd_empty_slot_ind is not None:  # If there is an empty slot before target_num of consecutive slots, add it to the list of columns to insert
                        invd_ins.append(invd_empty_slot_ind)
                elif invd_ele == "":
                    if off_inv < 0:     # To handle inverse diagonals with offset more than 0 since the index will start at 0 but in reality we need to add the offset
                        invd_empty_slot_ind = orig_ind - off_inv        # In this case is more of a invd_empty_slot_ind = orig_ind + -1*off_inv. We need to add the the offset value if it is a negative offset value
                    else:
                        invd_empty_slot_ind = orig_ind

                    if invd_tracker == target_num:
                        invd_ins.append(invd_empty_slot_ind)
                        invd_tracker= 0
                else:
                    invd_empty_slot_ind = None     # Reset to None since empty slot won't be adjacent to target_num of consecutive slots
                    invd_tracker = 0

            self.app_logger.debug("Columns to insert to win in the inverse diagonal with offset %s: %s", off_inv, invd_ins)

            for ins_invd in invd_ins:
                self.app_logger.info("Someone is going to win in an inverse diagonal of offset %s!", off_inv)
                col_vac_2 = self.brd1.get_col_vacancy(ins_invd)
                self.app_logger.debug("Column %s has %s vacancies(s)!", ins_invd, col_vac_2)

                # Logic:
                
                # We have this board and computer needs to add in 1,4 to win
                # _ _ _ _ _
                # _ O _ _ _
                # O O X X O
                # X O X O X
                # X X O X O

                #  0  1  2  3 4 5
                # -1  0  1  2 3 4
                # -2 -1  0  1 2 3
                # -3 -2 -1  0 1 2
                # -4 -3 -2 -1 0 1

                # ((abs(ins_invd - ((wd - 1) / 2)) * 2) + off_inv = original offset

                if ins_invd - ((abs(ins_invd - ((wd - 1) / 2)) * 2) + off_inv) + 1 == col_vac_2:
                    self.app_logger.info("Computer is going to insert in column %s", ins_invd)
                    return ins_invd
                elif ins_invd - (off_inv + wd - 1) + 2 == col_vac_2:  # Check if there is an empty slot in the column index below the said row. If there is, DO NOT add it. Else, player will win/block comp winning
                    self.app_logger.info("Computer is taking note to not add in column %s", ins_invd)
                    no_add_col.add(ins_invd)

        # Remove column for computer to add in
        for e in no_add_col:
            self.app_logger.debug("Removing " + str(e) + " from list of columns for computer to add token...")
            unf_cols.remove(e)
            if len(unf_cols) == 1:
                self.app_logger.debug("Only one more column left to choose so not removing any more!")
                break

        # Then from this new list choose a random column number that won't give player victory or block comp winning
        # self.app_logger.info("Computer is making a safe random move...")
        self.app_logger.debug("Final unfilled columns: %s", unf_cols)
    
        return unf_cols

    # Logic that checks if any side is winning after each turn
    def check_winner(self):
        
        connect_amt = int(self.selected_cnct_opt.get())  # How many tokens to connect to consider a win
        diff = connect_amt - 1    # Difference in index positions between starting index and last index to check

        # Check rows, columns, and diagonals for a winner
        board = self.brd1.get_board()
        ht = self.brd1.get_height()
        wd = self.brd1.get_width()
        
        # Check rows first
        for row_num, full_row in enumerate(board):
            for i in range(len(full_row) - diff):
                if full_row[i] == full_row[i + 1] == full_row[i + 2] == full_row[i + 3] != "":
                    return True
        
        # Check columns next
        board_t = board.T   # Transpose the board so that columns becomes rows
        for row_num1, full_row1 in enumerate(board_t):
            for i in range(len(full_row1) - diff):
                if full_row1[i] == full_row1[i + 1] == full_row1[i + 2] == full_row1[i + 3] != "":
                    return True
            
        # Check diagonals next
        min_offset = connect_amt - ht
        max_offset = wd - connect_amt
        
        for off in range(min_offset, max_offset + 1):
            diag = np.diagonal(board, offset=off).tolist()
            self.app_logger.debug("Checking diagonal: %s", diag)

            for i in range(len(diag) - diff):
                if diag[i] == diag[i + 1] == diag[i + 2] == diag[i + 3] != "":
                    return True

        # Check inverse diagonals
        flipped_board = np.fliplr(board)

        for off in range(min_offset, max_offset + 1):
            inv_diag = np.diagonal(flipped_board, offset=off).tolist()
            self.app_logger.debug("Checking inverse diagonal: %s", inv_diag)

            for i in range(len(inv_diag) - diff):
                if inv_diag[i] == inv_diag[i + 1] == inv_diag[i + 2] == inv_diag[i + 3] != "":
                    return True
        
        return False

    # Logic that checks if the game is a draw after each turn
    def check_draw(self):
        # Check if the board is full
        for row in self.brd1.get_board():
            for cell in row:
                if cell == "":
                    return False
        return True

    # Resets the board and proceeds to next round
    def reset_board(self):

        # board = self.brd1.get_board()
        height = self.brd1.get_height()
        width = self.brd1.get_width()

        # Reset the board to its initial state
        self.brd1.create()
        
        for i in range(height):
            for j in range(width):
                self.buttons[i][j].config(text="")

        # Determines who starts the next round
        self.p_turn = str(np.random.randint(1,3))
        p_name = self.map[f'{self.p_turn}'].get_name()

        self.app_logger.info(f'{p_name}' + " is starting the game!")
        self.update_label(f'{p_name}' + "'s turn!")

        if self.computer and self.p_turn == "2":
            self.comp_move()

    # Quits the game
    def quit_game(self):
        self.main.quit()

class Board:

    map = {}
    # col_list = []   # List of column numbers that are not full; For computer to quickly choose a column that is not filled

    def __init__(self) -> None:
        pass

    def set_height(self, height):
        self.height = height

    def get_height(self):
        return self.height
    
    def set_width(self, width):
        self.width = width

    def get_width(self):
        return self.width
    
    def create(self):
        self.col_list = []  # Adding col_list creation here so that every board creation will reset unfilled columns
        # Create map to track
        for i in range(self.width):
            self.map[i] = self.height
            self.col_list.append(i)         # Add in all columns into list

        # Using numpy to create board
        self.str_board = np.full((self.width, self.height), "", dtype=str)
        # return self.str_board

    def get_board(self):
        return self.str_board
    
    def update_board(self, col, sym):
        if self.map[col] > 0:
            # Update the str_board for tracking
            row = self.map[col] - 1
            self.str_board[row][col] = f'{sym}'

            # Set last empty row for the column
            self.map[col] -= 1

            if self.map[col] == 0:
                self.col_list.remove(col)

            return row

    def get_col_vacancy(self, col):
        return self.map[col]

    def get_unf_cols(self):    # get unfilled columns
        return self.col_list

class Player:
    
    def __init__(self) -> None:
        pass

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name
    
    def set_sym(self, sym):
        self.sym = sym

    def get_sym(self):
        return self.sym

    def set_score(self, score):
        self.score = score

    def get_score(self):
        return self.score

    def add_score(self, score=1):
        self.score += score

    def set_score_label(self, s_label):
        self.s_label = s_label

    def get_score_label(self):
        return self.s_label

class AppLogger:
    
    cf_cwd = os.path.join(os.getcwd(), 'python-projects', 'connect_four')

    # Create logs dir if not there
    os.makedirs(os.path.join(cf_cwd, "logs"), exist_ok=True)

    # Create app log file
    app_log_name = "connect_four.log"
    app_log = os.path.join(cf_cwd, "logs", app_log_name)

    # Create debug log
    debug_log_name = "connect_four_debug.log"
    debug_log = os.path.join(cf_cwd, "logs", debug_log_name)

    # Remove any existing log files
    if os.path.exists(app_log):
        os.remove(app_log)
    if os.path.exists(debug_log):
        os.remove(debug_log)

    # Create logger objects
    app_logger = log.getLogger('app')
    debug_logger = log.getLogger('app_debug')

    # Logging set up
    def start_logging(self):
        # cf_cwd = os.path.join(os.getcwd(), 'python-projects', 'connect_four')

        # # Create logs dir if not there
        # os.makedirs(os.path.join(cf_cwd, "logs"), exist_ok=True)

        # # Create app log file
        # app_log_name = "connect_four.log"
        # self.app_log = os.path.join(cf_cwd, "logs", app_log_name)

        # # Create debug log
        # debug_log_name = "connect_four_debug.log"
        # self.debug_log = os.path.join(cf_cwd, "logs", debug_log_name)

        # # Remove any existing log files
        # if os.path.exists(self.app_log):
        #     os.remove(self.app_log)
        # if os.path.exists(self.debug_log):
        #     os.remove(self.debug_log)

        # Create logger objects
        # self.app_logger = log.getLogger('app')
        # self.debug_logger = log.getLogger('app_debug')

        # Create and configure loggers
        self.app_logger.setLevel(log.DEBUG)
        self.debug_logger.setLevel(log.DEBUG)

        formatter = log.Formatter('%(asctime)s %(levelname)s - %(message)s')

        file_handler1 = log.FileHandler(self.app_log, mode='a')
        file_handler1.setFormatter(formatter)

        file_handler2 = log.FileHandler(self.debug_log, mode='a')
        file_handler2.setFormatter(formatter)

        # Add file handlers to loggers
        self.app_logger.addHandler(file_handler1)
        self.debug_logger.addHandler(file_handler2)

    def get_app_logger(self):
        return self.app_logger
    
    def get_debug_logger(self):
        return self.debug_logger
    
if __name__ == "__main__":
    root = tk.Tk()
    Game(root)
    root.mainloop()
    print("Thank you for playing Connect Four!")