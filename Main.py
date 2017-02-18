import pygame, sys, random, copy, time, xlsxwriter
from pygame.locals import *

SCREEN_WIDTH = 490
SCREEN_HEIGHT = 380

# colors used
BLUE_WHITE = (240,245,249)
LIGHT_BLUE = (201,214,223)
BLUE = (82,96,106)
BLUE_BLACK = (29,32,33)
BLACK = (0, 0, 0)
DEEP_DARK_BLUE = (35,26,49)
STRAWBERRY_RED = (228,47,69)
DARK_RED = (180,42,63)
ROBINS_EGG_BLUE = (138,238,255)

BACKGROUND_COLOR = BLUE_BLACK
FONT_COLOR = BLUE_WHITE

# game board's cordinates
WINDOW_BOARD_GAP = 20
BOARD_WIDTH = 340
BOARD_HEIGHT = 340
BOARD_X = WINDOW_BOARD_GAP
BOARD_Y = WINDOW_BOARD_GAP
BOARD_RECT = (BOARD_X, BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT)
BOARD_COLOR = BLUE

# tile cordinates
TILE_GAP = 10
TILE_COLOR = LIGHT_BLUE

# cordinates and variables for buttons
BUTTONS_X = 380

MOVES_X = BUTTONS_X
MOVES_Y = BOARD_Y + 130

BUTTON_BOARD_SIZE_FONT_SIZE = 30
BUTTON_BOARD_SIZE_X = MOVES_X
BUTTON_BOARD_SIZE_Y = MOVES_Y + 35
BUTTON_BOARD_SIZE_WIDTH = 40
BUTTON_BOARD_SIZE_HEIGHT = 40
BUTTON_BOARD_SIZE_RECT = pygame.Rect(BUTTON_BOARD_SIZE_X, BUTTON_BOARD_SIZE_Y, BUTTON_BOARD_SIZE_WIDTH, BUTTON_BOARD_SIZE_HEIGHT)

BUTTON_RESET_X = BUTTONS_X
BUTTON_RESET_Y = BUTTON_BOARD_SIZE_Y + BUTTON_BOARD_SIZE_HEIGHT + 10
BUTTON_RESET_WIDTH = 70
BUTTON_RESET_HEIGHT = 35
BUTTON_RESET_RECT = pygame.Rect(BUTTON_RESET_X, BUTTON_RESET_Y, BUTTON_RESET_WIDTH, BUTTON_RESET_HEIGHT)

BUTTON_SOLVE_X = BUTTONS_X
BUTTON_SOLVE_Y = BUTTON_RESET_Y + BUTTON_RESET_HEIGHT + 10
BUTTON_SOLVE_WIDTH = 70
BUTTON_SOLVE_HEIGHT = 35
BUTTON_SOLVE_RECT = pygame.Rect(BUTTON_SOLVE_X, BUTTON_SOLVE_Y, BUTTON_SOLVE_WIDTH, BUTTON_SOLVE_HEIGHT)

BUTTON_QUIT_X = BUTTONS_X
BUTTON_QUIT_Y = BUTTON_SOLVE_Y + BUTTON_SOLVE_HEIGHT + 10
BUTTON_QUIT_WIDTH = 70
BUTTON_QUIT_HEIGHT = 35
BUTTON_QUIT_RECT = pygame.Rect(BUTTON_QUIT_X, BUTTON_QUIT_Y, BUTTON_QUIT_WIDTH, BUTTON_QUIT_HEIGHT)

FONT_VICTORY_SIZE = 16
FONT_VICTORY_X = BUTTONS_X
FONT_VICTORY_Y = BOARD_Y

# game variables
DIFFICULTY = 100
TIME_OUT = 30  # stop after 30 seconds

LEFT = 'a'
RIGHT = 'd'
UP = 'w'
DOWN = 's'

NUM_OF_SOLVING_METHODS = 5

BREADTH_FIRST = 0
BREADTH_FIRST_CLOSED_LIST = 1
DEPTH_FIRST_CLOSED_LIST = 2
A_STAR_MANHATTAN_HEURISTIC = 3
A_STAR_TILES_OUT_OF_ROW_COL = 4

METHOD = A_STAR_MANHATTAN_HEURISTIC

# variables for checking for answer
SOLUTION_STATE = None
SOLUTION_3 = dict()
count = 1
for i in range(3):
    for j in range(3):
        SOLUTION_3[count] = [i, j]
        count += 1

SOLUTION_4 = dict()
count = 1
for i in range(4):
    for j in range(4):
        SOLUTION_4[count] = [i, j]
        count += 1

SOLUTION_5 = dict()
count = 1
for i in range(5):
    for j in range(5):
        SOLUTION_5[count] = [i, j]
        count += 1


class Board:
    def __init__(self, b=None):
        if not b:  # make brand new board
            self.tiles = []
            self.text = ""  # this is used for comparing boards.
            # populate tiles
            count = 1
            for i in range(BOARD_SIZE):
                row = []
                for j in range(BOARD_SIZE):
                    row.append(count)
                    self.text += str(count)
                    count += 1
                    count %= NUM_TILES
                self.tiles.append(row)
            self.blank_x = BOARD_SIZE - 1
            self.blank_y = BOARD_SIZE - 1
            self.moves = []
            self.score = -1  # this is used for a*
        else:  # make a copy
            self.tiles = copy.deepcopy(b.tiles)
            self.blank_x = copy.deepcopy(b.blank_x)
            self.blank_y = copy.deepcopy(b.blank_y)
            self.moves = copy.deepcopy(b.moves[:])
            self.text = copy.deepcopy(b.text)
            self.score = copy.deepcopy(b.score)


# draw game window using Pygame functions
def draw_game(board):

    draw_board(board)
    # draw moves made
    DISPLAY_SURF.blit(BUTTON_FONT.render("MOVES: " + str(NUM_MOVES), 1, FONT_COLOR), (MOVES_X, MOVES_Y))
    # draw board size button
    pygame.draw.rect(DISPLAY_SURF, TILE_COLOR, BUTTON_BOARD_SIZE_RECT)
    DISPLAY_SURF.blit(BOARD_SIZE_FONT.render(str(BOARD_SIZE), 1, BLACK),(BUTTON_BOARD_SIZE_X + 5, BUTTON_BOARD_SIZE_Y + 5))
    # draw reset button
    pygame.draw.rect(DISPLAY_SURF, TILE_COLOR, BUTTON_RESET_RECT)
    DISPLAY_SURF.blit(BUTTON_FONT.render("RESET", 1, BLACK), (BUTTON_RESET_X + 5, BUTTON_RESET_Y + 5))
    # draw solve button
    pygame.draw.rect(DISPLAY_SURF, TILE_COLOR, BUTTON_SOLVE_RECT)
    DISPLAY_SURF.blit(BUTTON_FONT.render("SOLVE", 1, BLACK), (BUTTON_SOLVE_X + 5, BUTTON_SOLVE_Y + 5))
    # draw quit button
    pygame.draw.rect(DISPLAY_SURF, TILE_COLOR, BUTTON_QUIT_RECT)
    DISPLAY_SURF.blit(BUTTON_FONT.render("QUIT", 1, BLACK), (BUTTON_QUIT_X + 5, BUTTON_QUIT_Y + 5))
    pygame.display.update()
    DISPLAY_SURF.fill(BACKGROUND_COLOR)


# check if the given move is possible with the given board
def possible_move(board, dir):
    if dir == LEFT:
        if board.blank_y == BOARD_SIZE-1:
            return False
    elif dir == RIGHT:
        if board.blank_y == 0:
            return False
    elif dir == UP:
        if board.blank_x == BOARD_SIZE-1:
            return False
    elif dir == DOWN:
        if board.blank_x == 0:
            return False
    else:
        # invalid input
        return False
    return True


# given a board, make a tile move, and return the resulting board
def move(board, dir):
    if not board or not possible_move(board, dir):
        return None
    b = Board(board)
    b.moves.insert(0, dir)
    new_blank_x, new_blank_y = b.blank_x, b.blank_y
    if dir == LEFT:
        new_blank_y += 1
    elif dir == RIGHT:
        new_blank_y -= 1
    elif dir == UP:
        new_blank_x += 1
    elif dir == DOWN:
        new_blank_x -= 1
    else:
        print "invalid input"
        return None
    b.tiles[b.blank_x][b.blank_y] = b.tiles[new_blank_x][new_blank_y]
    b.tiles[new_blank_x][new_blank_y] = 0
    b.blank_x, b.blank_y = new_blank_x, new_blank_y
    b.text = tiles_to_string(b)
    return b


# generate a random board by making a set amount of rabdin nives
def random_board(difficulty):
    board = Board()
    inputs = "asdw"
    for i in range(difficulty):
        dir = inputs[random.randint(0, 3)]
        while not possible_move(board, dir) and not is_loop(board, dir):
            dir = inputs[random.randint(0, 3)]
        board = move(board, dir)
    board.moves = []
    return board


# check if board is in solved state
def is_solved(board):
    if board.text == SOLUTION_STATE.text:
        return True
    else:
        return False


# print board in ASCII to console. For debugging reasons
def print_board(board):
    if not board:
        print "cant print invalid board"
        return
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board.tiles[i][j] == 0:
                sys.stdout.write('%s' % " ")
            else:
                sys.stdout.write('%s' % board.tiles[i][j])
        print ""
    print ""


def get_compliment(dir):
    if dir == LEFT: return RIGHT
    if dir == RIGHT: return LEFT
    if dir == UP: return DOWN
    if dir == DOWN: return UP


# check for loops, such as LEFT then RIGHT then LEFT. Its redundant and slows down the AI
def is_loop(board, dir):
    if len(board.moves) < 2:
        return False
    if board.moves[0] == get_compliment(dir) and board.moves[0] == dir:
        return True
    else:
        return False


# This is for the closed list algorithms
def is_in_closed_list(board, closed_list):
    if board.moves in closed_list:
        return True
    else:
        return False


# turn the tile configuration into a string, so it can be put into a closed list
def tiles_to_string(board):
    text = ""
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            text += str(board.tiles[x][y])
    return text


# depth first with closed list
def solve_board_depth_first(board, method, return_test_data=False):
    use_closed_list = method == DEPTH_FIRST_CLOSED_LIST
    states = [] # queue for states
    dirs = "asdw"
    curr_state = Board(board)
    count = 0

    if use_closed_list:
        closed_set = set(curr_state.text)

    print "Now solving a board of size " + str(BOARD_SIZE) + " with " + get_method_name(method)
    start = time.time()  # count time it takes to finish
    while not is_solved(curr_state):
        if time.time() - start >= TIME_OUT:
            return None
        for i in range(4):
            state = move(curr_state, dirs[i])
            if not state:
                continue
            # check for repeating moves, or states
            if use_closed_list and state.text in closed_set:
                #  print len(closed_set)
                state = None

            if state:
                states.append(Board(state))
                if use_closed_list:
                    closed_set.add(state.text)

        curr_state = states.pop(len(states)-1)
        count += 1

    end = time.time()
    print "SOLVED! Using " + get_method_name(method)
    print "Answer: " + str(curr_state.moves)
    print "States: " + str(count)
    print "Time: " + str(end - start)
    print "Current length of queue: " + str(len(states))
    if return_test_data:
        return [curr_state, count, end-start, len(states)]
    else:
        return curr_state


# breadth first. With or without closed list
def solve_board_breadth_first(board, method, return_test_data=False):
    use_closed_list = method == BREADTH_FIRST_CLOSED_LIST
    states = [] # queue for states
    dirs = "asdw"
    curr_state = Board(board)
    count = 0

    if use_closed_list:
        closed_set = set(curr_state.text)

    print "Now solving a board of size " + str(BOARD_SIZE) + " with " + get_method_name(method)
    start = time.time() # count time it takes to finish
    while not is_solved(curr_state):
        # time out after a minute
        if time.time() - start >= TIME_OUT:
            return None
        for i in range(4):
            state = move(curr_state, dirs[i])
            if not state:
                continue
            # check for repeating moves, or states
            if use_closed_list and state.text in closed_set:
                # print state.text
                state = None

            if state:
                states.append(Board(state))
                if use_closed_list:
                    closed_set.add(state.text)
                # print closed_list

        curr_state = states.pop(0)
        # print_board(curr_state)
        count += 1

    end = time.time()
    print "SOLVED! Using " + get_method_name(method)
    print "Answer: " + str(curr_state.moves)
    print "States: " + str(count)
    print "Time: " + str(end - start)
    print "Current length of queue: " + str(len(states))
    if return_test_data:
        return [curr_state, count, end-start, len(states)]
    else:
        return curr_state


# A*, with NOTO or Manhattan heuristic
def solve_board_A_star(board, heuristic, return_test_data=False):
    states = [] # queue for states
    dirs = "asdw"
    curr_state = Board(board)

    assign_score(curr_state, heuristic)
    closed_set = set(curr_state.text)
    print "Now solving a board of size " + str(BOARD_SIZE) + " with " + get_method_name(heuristic)
    count = 0
    start = time.time()  # count time it takes to finish
    while not is_solved(curr_state):
        if time.time() - start >= TIME_OUT:
            return None
        for i in range(4):
            state = move(curr_state, dirs[i])
            if not state:
                continue
            # check for repeating moves, or states
            if state.text in closed_set:
                # print state.text
                state = None

            if state:
                assign_score(state, heuristic) # assign a score based on the heuristic passed by argument
                states.append(Board(state))    # So far: its either, manhatten distance or tiles out of row/col
                closed_set.add(state.text)
                # print closed_list

        # sort list by their scores
        states.sort(key = lambda new_list: new_list.score)
        curr_state = states.pop(0)
        # print_board(curr_state)
        count += 1

    end = time.time()
    print "SOLVED! Using " + get_method_name(heuristic)
    print "Answer: " + str(curr_state.moves)
    print "States: " + str(count)
    print "Time: " + str(end - start)
    print "Current length of queue: " + str(len(states))
    if return_test_data:
        return [curr_state, count, end-start, len(states)]
    else:
        return curr_state


# calculate manhattan distance for one tile
def get_manhattan_distance(board, x, y):
    val = board.tiles[x][y]
    if val == 0:
        return 0
    else:
        correct_x, correct_y = get_correct_tile_cords(val)
        return abs(x - correct_x) + abs(y - correct_y)


# get where tile should be
def get_correct_tile_cords(val):
    if BOARD_SIZE == 3:
        return SOLUTION_3[val]
    elif BOARD_SIZE == 4:
        return SOLUTION_4[val]
    elif BOARD_SIZE == 5:
        return SOLUTION_5[val]


# score whole board
def manhattan_score(board):
    sum = 0
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            sum += get_manhattan_distance(board, x, y)
    return sum


# heuristic NOTO
def tiles_out_of_row_col(board):
    score = 0
    # check rows
    for i in range(3):
        row = board.tiles[i]
        correct_row = SOLUTION_STATE.tiles[i]
        for x in row:
            if x not in correct_row:
                score += 1

    # check cols
    for j in range(3):
        col = [row[j] for row in board.tiles] # this is confusing but row[] is getting me the col
        correct_row = [row[j] for row in SOLUTION_STATE.tiles]
        for y in col:
            if y not in correct_row:
                score += 1

    return score

# this is used for A star
# the two heuristics are: manhattan distance, and number of tiles out of rows/cols
def assign_score(board, heuristic):
    if heuristic == A_STAR_MANHATTAN_HEURISTIC:
        board.score = manhattan_score(board)
        board.score += len(board.moves)
    elif heuristic == A_STAR_TILES_OUT_OF_ROW_COL:
        board.score = tiles_out_of_row_col(board)
        board.score += len(board.moves)


# draw a tile using Pygame functions
def draw_tile(x, y, val):
    # check for blank tile
    if val == 0:
        return
    else:
        pygame.draw.rect(DISPLAY_SURF, TILE_COLOR, (x, y, TILE_SIZE, TILE_SIZE))
        text = TILE_FONT.render(str(val), 1, BLACK)
        text_x = x + TILE_SIZE/NUM_TILES
        text_y = y + TILE_SIZE/BOARD_SIZE
        DISPLAY_SURF.blit(text, (text_x, text_y))


# draw the board using Pygame functions
def draw_board(board):
    pygame.draw.rect(DISPLAY_SURF, BOARD_COLOR, BOARD_RECT)
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            x_cord = BOARD_X + (x+1)*TILE_GAP + x*TILE_SIZE
            y_cord = BOARD_Y + (y+1)*TILE_GAP + y*TILE_SIZE
            draw_tile(x_cord, y_cord, board.tiles[y][x])


# call the correct search algorithm to solve the board
def get_solution(board, method, return_test_data=False):
    if method == A_STAR_MANHATTAN_HEURISTIC or A_STAR_TILES_OUT_OF_ROW_COL:
        return solve_board_A_star(board, method,return_test_data)
    elif method == BREADTH_FIRST_CLOSED_LIST or method == BREADTH_FIRST:
        return solve_board_breadth_first(board, method,return_test_data)
    elif method == DEPTH_FIRST_CLOSED_LIST:
        return solve_board_depth_first(board, method,return_test_data)
    else:
        print "Invalid method."
        return None


# show the solution to the user. When they press space, the correct moves are made until its finished
def show_solution(board, method):
    solved_state = get_solution(board, method)

    correct_moves = list(reversed(solved_state.moves))
    index = 0
    key_down = False
    while True:

        if is_solved(board):
            DISPLAY_SURF.blit(BUTTON_FONT.render("SOLVED!!!!", 1, FONT_COLOR), (370, 10))
        # check for quit
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                # get position of mouse
                x_mouse, y_mouse = pygame.mouse.get_pos()
                if BUTTON_QUIT_RECT.collidepoint(x_mouse, y_mouse):
                    pygame.quit()
                    sys.exit()
                elif BUTTON_RESET_RECT.collidepoint(x_mouse, y_mouse):
                    board = random_board(DIFFICULTY)
                    user_solve(board)
                    return

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        elif keys_pressed[pygame.K_SPACE] and not key_down and not is_solved(board):
            key_down = True
            board = move(board, correct_moves[index])
            index += 1
        elif not keys_pressed[pygame.K_SPACE] and key_down:
            key_down = False
        draw_game(board)
    user_solve(board)
    return


# user tries to solve board with AWSD keys
def user_solve(board):
    original_board = copy.deepcopy(board) # incase user presses solve
    global NUM_MOVES
    NUM_MOVES = 0
    move_made = False
    while True:
        if is_solved(board):
            DISPLAY_SURF.blit(BUTTON_FONT.render("YOU WIN!", 1, FONT_COLOR), (FONT_VICTORY_X, FONT_VICTORY_Y))

        # check for quit
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                # get position of mouse
                x_mouse, y_mouse = pygame.mouse.get_pos()
                if BUTTON_QUIT_RECT.collidepoint(x_mouse, y_mouse):
                    pygame.quit()
                    sys.exit()
                elif BUTTON_RESET_RECT.collidepoint(x_mouse, y_mouse):
                    board = random_board(DIFFICULTY)
                    NUM_MOVES = 0
                    continue
                elif BUTTON_SOLVE_RECT.collidepoint(x_mouse, y_mouse):
                    show_solution(original_board, METHOD)
                    return
                elif BUTTON_BOARD_SIZE_RECT.collidepoint(x_mouse, y_mouse):
                    change_board_size()
                    start_new_game()
                    return
        # check for input

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        elif keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
            if not move_made and possible_move(board, UP):
                move_made = True
                board = move(board, UP)
        elif keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
            if not move_made and possible_move(board, DOWN):
                move_made = True
                board = move(board, DOWN)
        elif keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            if not move_made and possible_move(board, LEFT):
                move_made = True
                board = move(board, LEFT)
        elif keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            if not move_made and possible_move(board, RIGHT):
                move_made = True
                board = move(board, RIGHT)
        elif move_made:
            NUM_MOVES += 1
            move_made = False
        draw_game(board)


# begin new game for user
def start_new_game():
    user_solve(random_board(DIFFICULTY))


# change from 3X3 to 4X4, 4X4 to 5X5, or 5X5 to 3X3
def change_board_size():
    global BOARD_SIZE, NUM_TILES, TILE_SIZE, TILE_FONT, SOLUTION_STATE
    BOARD_SIZE += 1
    if BOARD_SIZE == 6:
        BOARD_SIZE = 3
    NUM_TILES = BOARD_SIZE*BOARD_SIZE
    # change solution state
    SOLUTION_STATE = Board()
    TILE_SIZE = 100
    TILE_SIZE = (BOARD_WIDTH - 10*(BOARD_SIZE+1))/BOARD_SIZE
    TILE_FONT = pygame.font.SysFont("calibri", TILE_SIZE/2)


def get_method_name(method):
    if method == BREADTH_FIRST:
        return "Breadth 1st"
    elif method == BREADTH_FIRST_CLOSED_LIST:
        return "Breadth 1st w/ CL"
    elif method == DEPTH_FIRST_CLOSED_LIST:
        return "Depth 1st w/ CL"
    elif method == A_STAR_MANHATTAN_HEURISTIC:
        return "A* w/ Manhattan"
    elif method == A_STAR_TILES_OUT_OF_ROW_COL:
        return "A* w/ # Tiles Out Of Row/Col"
    else:
        return "Unknown method"


# this function solves a new board n times for each solving method, and records the results into an excel file
def get_stats_for_solving(n):
    workbook = xlsxwriter.Workbook('C:\Users\ericm\PycharmProjects\SliderPuzzle\NPuzzle.xlsx')
    worksheet = workbook.add_worksheet()
    row, col = 0, 0
    # print collumn information
    title_info = ["Method", "Size", "Difficulty", "Moves", "Total States", "Time(sec)", "Sol. Size", "Solution"]
    for title in title_info:
        worksheet.write(row, col, str(title))
        col += 1
    col = 0
    row += 1

    # now solve puzzle using each method, n times, storing each result into the array solving_data
    solving_data = []
    # do thtis for every board size
    for i in range(3):
        for count in range(NUM_OF_SOLVING_METHODS):
            print count
            method = count
            num_time_outs = 0
            for i in range(n):
                board = random_board(DIFFICULTY)
                board_difficulty = manhattan_score(board)
                data = get_solution(board, method, True)
                # get_solution returns None if it takes longer than TIME_OUT
                if data is None:
                    solving_data.append([get_method_name(method), BOARD_SIZE, board_difficulty, "1E+99", "1E+99", TIME_OUT, "NA", "NA"])
                else:
                    # Method Size	Difficulty	Moves	Total States	Time	Solution size	solution
                    formatted_data = [get_method_name(method), BOARD_SIZE, board_difficulty, data[1], data[3] + data[1], data[2], len(data[0].moves), data[0].moves]
                    solving_data.append(formatted_data)
            # [curr_state, count, end-start, len(states)]
            solving_data.append([" "]) # newline for excel
            print solving_data
        change_board_size()

    # now, print alll this data to the excel document
    if solving_data is not None:
        for solve in solving_data:
            for item in solve:
                print item
                worksheet.write(row, col, str(item))
                col += 1
            col = 0
            row += 1
    else:
        print "Formatted data error"
    worksheet.set_column(0, 0, 30) # widen A collumn so the method name can be seen
    workbook.close()
    return 1


# start of program
def main():
    # declare globals
    global DISPLAY_SURF, TILE_FONT, BUTTON_FONT, BOARD_SIZE_FONT, SOLUTION_STATE, METHOD
    global NUM_TILES, TILE_SIZE, BOARD_SIZE, BUTTON_BOARD_SIZE
    global NUM_MOVES

    # default board
    BOARD_SIZE = 3
    NUM_TILES = BOARD_SIZE*BOARD_SIZE
    TILE_SIZE = 100
    TILE_SIZE = (BOARD_WIDTH - 10*(BOARD_SIZE+1))/BOARD_SIZE
    SOLUTION_STATE = Board()

    pygame.init()
    DISPLAY_SURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    TILE_FONT = pygame.font.SysFont("calibri", TILE_SIZE/2)
    BUTTON_FONT = pygame.font.SysFont("calibri", 22)
    BOARD_SIZE_FONT = pygame.font.SysFont("calibri", BUTTON_BOARD_SIZE_FONT_SIZE)
    pygame.display.set_caption('Slider Puzzle')
    DISPLAY_SURF.fill(BACKGROUND_COLOR)

    testing = False
    if testing:
        get_stats_for_solving(25)
    else:
        start_new_game()


if __name__ == "__main__":
    main()
