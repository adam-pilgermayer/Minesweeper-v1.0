from random import randint

around_pos = [
    [-1, -1],
    [-1, 0],
    [-1, 1],
    [0, -1],
    [0, 1],
    [1, -1],
    [1, 0],
    [1, 1],
] # This is used to check surrounding cells


def start():
    options = ["S", "E"]
    answer = None
    game_start = False
    print("[S] - Start\n[E] - Exit", end="\n\n")
    while not answer in options:
        answer = input("Type 'S' to start a game or 'E' to exit and press enter: ")
        answer = answer.upper()
    if answer == "S": game_start = True
    elif answer == "E": game_start = False
    return game_start


def table_layer1():
    """Creates a 2D table. This will be the top layer of the game.

    Possible values:

    E - Examine | Available to discover cells with this value\n
    0 - 0 mines around that cell\n
    1-8 - The cell has 1 to 8 neighbors with a mine on it\n
    M - A position with a mine\n
    """

    row = ["E" for elem in range(9)]
    table_l1 = [row[:] for elem in range(9)]
    return table_l1[:]


def table_layer2():
    """Creates a 2D table. This is the bottom layer of the game.
    
    This will be a layer that is hidden from the player.
    Mines and values will be placed here.

    Possible values:

    0 - 0 mines around that cell\n
    1-8 - The cell has 1 to 8 neighbors with a mine on it\n
    M - A position with a mine\n
    """

    row = [0 for elem in range(9)]
    table_l2 = [row[:] for elem in range(9)]
    return table_l2[:]


def console_table(t):
    """
    Prints the current state of the game.
    """

    print( f'''    1  2  3  4  5  6  7  8  9\n\n\
a   {t[0][0]}  {t[0][1]}  {t[0][2]}  {t[0][3]}  {t[0][4]}  {t[0][5]}  {t[0][6]}  {t[0][7]}  {t[0][8]}\n\
b   {t[1][0]}  {t[1][1]}  {t[1][2]}  {t[1][3]}  {t[1][4]}  {t[1][5]}  {t[1][6]}  {t[1][7]}  {t[1][8]}\n\
c   {t[2][0]}  {t[2][1]}  {t[2][2]}  {t[2][3]}  {t[2][4]}  {t[2][5]}  {t[2][6]}  {t[2][7]}  {t[2][8]}\n\
d   {t[3][0]}  {t[3][1]}  {t[3][2]}  {t[3][3]}  {t[3][4]}  {t[3][5]}  {t[3][6]}  {t[3][7]}  {t[3][8]}\n\
e   {t[4][0]}  {t[4][1]}  {t[4][2]}  {t[4][3]}  {t[4][4]}  {t[4][5]}  {t[4][6]}  {t[4][7]}  {t[4][8]}\n\
f   {t[5][0]}  {t[5][1]}  {t[5][2]}  {t[5][3]}  {t[5][4]}  {t[5][5]}  {t[5][6]}  {t[5][7]}  {t[5][8]}\n\
g   {t[6][0]}  {t[6][1]}  {t[6][2]}  {t[6][3]}  {t[6][4]}  {t[6][5]}  {t[6][6]}  {t[6][7]}  {t[6][8]}\n\
h   {t[7][0]}  {t[7][1]}  {t[7][2]}  {t[7][3]}  {t[7][4]}  {t[7][5]}  {t[7][6]}  {t[7][7]}  {t[7][8]}\n\
i   {t[8][0]}  {t[8][1]}  {t[8][2]}  {t[8][3]}  {t[8][4]}  {t[8][5]}  {t[8][6]}  {t[8][7]}  {t[8][8]}\n\n''')

def generate_mine_positions(p_first_step):
    """
    Generates ten unique index combinations for mine positions.

    The position won't be the same as the player's first step.
    """

    mines = 10
    mine_positions = set()
    
    while mines > 0:
        mine_pos = randint(0, 8), randint(0, 8)
        if not ((mine_pos in mine_positions) or (mine_pos[0] == p_first_step[0] and mine_pos[1] == p_first_step[1])):
            mine_positions.add(mine_pos)
            mines -= 1
    mine_positions = list(mine_positions)
    return mine_positions


def set_mines(t, mines):
    """
    This has two functionality.\n
    First, to update layer2 with the mine positions to be able
    to render the full table with mines and numbers.

    The second use is to show the mines to the player
    if stepped on one of the mines.
    """

    for mine in mines:
        t[mine[0]][mine[1]] = "M"

def set_values(t, mines):
    """
    Based on mine positions this will update layer2 cells with values between 1-8,
    which means a cell can be surrounded by eight mines maximum.
    If it's still zero, that means no mines around it.
    
    Example: A cell with value 3 means there are 3 mines around that cell.
    """

    for mine in mines:
        for elem in around_pos:
            row = mine[0] + elem[0]
            col = mine[1] + elem[1]
            if col in range(9) and row in range(9):
                if isinstance(t[row][col], int):
                    t[row][col] += 1


def choose_position():
    """
    The player must select a row and a column to create a position.
    
    Example: row - d, col - 7 means that the player chose a position on the fourth row and the eighth column.
    """

    selectable_rows = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7, "i":8}  # row : index
    selectable_cols = {1:0, 2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:7, 9:8}  # col : index
    choose_row = None
    choose_col = None

    while not choose_row in selectable_rows.keys():
            choose_row = input("Choose a row from 'a' to 'i': ")
            choose_row = choose_row.lower()
            if not choose_row in selectable_rows.keys():
                print("Wrong value. You must have to choose a letter between 'a' and 'i'.")
    while not (choose_col in selectable_cols.keys()):
            try:
                choose_col = int(input("Choose a column from 1 to 9: "))
            except ValueError:
                print("Wrong value. Only integers are allowed here.")
            if not choose_col in selectable_cols.keys():
                print("You must have to choose an integer between 1 and 9.")
    return selectable_rows[choose_row], selectable_cols[choose_col]




def find_zeros(row, col, layer1, layer2):
    """
    Finds every clear node around the player's selected position.

    Only applied when the player stepped on a cell with value 0.
    """

    if row < 0 or col < 0 or row == 9 or col == 9: return
    if layer1[row][col] in range(9): return
    if layer2[row][col] == 0:
        layer1[row][col] = 0
        for r in around_pos:
            for c in around_pos:
                find_zeros(row+r[0], col+c[1], layer1, layer2)
    if layer2[row][col] > 0:
        layer1[row][col] = layer2[row][col]


def update_layer1(pos, layer1, layer2):
    """
    Updates layer1 table based on the player's position.
    """

    if layer2[pos[0]][pos[1]] == 'M':
        layer1[pos[0]][pos[1]] = layer2[pos[0]][pos[1]]
    elif layer2[pos[0]][pos[1]] == 0:
        find_zeros(pos[0], pos[1], layer1, layer2)
    else:
        layer1[pos[0]][pos[1]] = layer2[pos[0]][pos[1]]
    
    return layer1

def collect_discovered_positions(layer1):
    """
    Counts every discovered positions in the layer1 table.
    This is neccessary because we have to know that
    there should be only 10 undiscovered positions left to win the game.
    (These are the mine positions)
    """
    discovered = set()
    for r in range(9):
        for c in range(9):
            if layer1[r][c] != 'E':
                discovered.add((r, c))
    return len(discovered)


def is_it_over(pos, layer2):
    """
    Checks if the player stepped on a mine or not.
    """
    return layer2[pos[0]][pos[1]] == 'M'


# Game loop starts from here.

new_game = start()

while new_game:
    print("Game started\n")

    game_over = False
    win = False
    discovered_clear_positions = 0
    
    covering_layer = table_layer1()
    hidden_layer = table_layer2()
    console_table(covering_layer)

    first_step = choose_position()
    mine_positions = generate_mine_positions(first_step)

    set_mines(hidden_layer, mine_positions)
    set_values(hidden_layer, mine_positions)

    update_layer1(first_step,covering_layer, hidden_layer)
    console_table(covering_layer)

    discovered_clear_positions = collect_discovered_positions(covering_layer)


    while not game_over and not win:
        step = choose_position()

        while covering_layer[step[0]][step[1]] != 'E':
            print('You already discovered this position! Choose again.\n')
            step = choose_position()

        update_layer1(step, covering_layer, hidden_layer)
        console_table(covering_layer)

        game_over = is_it_over(step, hidden_layer)
        discovered_clear_positions = collect_discovered_positions(covering_layer)


        if discovered_clear_positions == 71:
            win = True


        if win: 
            print("Congratulations! You won!")
        if game_over: 
            set_mines(covering_layer, mine_positions)
            console_table(covering_layer)
            print("Game Over! Try again next time.")

    new_game = start()