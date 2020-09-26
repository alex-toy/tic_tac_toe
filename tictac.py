import sys
from copy import deepcopy

cross = ' X '
round = ' O '
empty = '   '

size_game = 3

point_array = [0] * size_game*size_game

game_state = []
for i in range(size_game) :
    game_state += deepcopy([[empty]*size_game])




def display(game_state):
    print('      C1    C2    C3')
    verticalSplit = '    ' + '------'*size_game
    print(verticalSplit)
    for row in game_state:
        print('L'+ str(game_state.index(row)+1) +' | ', end = '')
        for col in row:
            print(col + ' | ', end = '')
        print('')
        print(verticalSplit)



def insert_choice(choice, sign) :
    line = choice[0]
    column = choice[1]
    if line >= 0 and line <= (size_game-1) and column >= 0 and column <= (size_game-1) :
        if game_state[line][column] == empty :
            game_state[line][column] = sign
            return True
    else :
        return False



def player_choice() :
    print('make your choice')

    temp_line = input('Line : ')
    if temp_line == 'x' : sys.exit()
    while not temp_line.isdigit() :
        if temp_line == 'x' : sys.exit()
        print('A number is needed!')
        temp_line = input('Line : ')
    line = int(temp_line)-1

    temp_col = input('Column : ')
    if temp_col == 'x' : sys.exit()
    while not temp_col.isdigit() :
        if temp_col == 'x' : sys.exit()
        print('A number is needed!')
        temp_col = input('Column : ')
    col = int(temp_col)-1

    legal_choice = insert_choice([line, col], cross)
    while not legal_choice :
        print('illegal choice')
        line = int(input('Line : '))-1
        col = int(input('Column : '))-1
        legal_choice = insert_choice([line, col], cross)



def only_one_empty() :
    num_empty_spots = 0
    for row in range(size_game) :
        for col in range(size_game) :
            if game_state[row][col] == empty : num_empty_spots += 1
    return num_empty_spots == 1



def find_empty_spot():
    for line in range(size_game) :
        for col in range(size_game) :
            if game_state[line][col] == empty :
                return line, col



def computer_choice() :
    if only_one_empty() :
        line, col = find_empty_spot()
        insert_choice([line, col], round)
        print(line, col)
    else :
        temp_point_array = deepcopy(point_array)
        for i in range(size_game*size_game) :
            if temp_point_array[i] == 0 : temp_point_array[i] = -10000000000
        max_point = max(temp_point_array)
        max_point_index = temp_point_array.index(max_point)
        line = int(max_point_index/3)
        col = max_point_index%3
        insert_choice([line, col], round)



def line_winner(temp_array, num_line, sign) :
    if temp_array[num_line][0] != sign : return False
    line_winner_test = True
    for col in range(size_game) :
        if temp_array[num_line][0] != temp_array[num_line][col-1] : line_winner_test = False
    return line_winner_test


def column_winner(temp_array, num_col, sign) :
    if temp_array[0][num_col] != sign : return False
    col_winner_test = True
    for line in range(size_game) :
        if temp_array[0][num_col] != temp_array[line-1][num_col] : col_winner_test = False
    return col_winner_test


def first_diagonal_winner(temp_array, sign) :
    if temp_array[0][0] != sign : return False
    first_diagonal_winner_test = True
    for index in range(size_game) :
        if temp_array[0][0] != temp_array[index-1][index-1]  : first_diagonal_winner_test = False
    return first_diagonal_winner_test


def second_diagonal_winner(temp_array, sign) :
    if temp_array[size_game-1][0] != sign : return False
    second_diagonal_winner_test = True
    for index in range(size_game) :
        if temp_array[size_game-1][0] != temp_array[size_game-index-1][index]  : second_diagonal_winner_test = False
    return second_diagonal_winner_test



def player_winner(temp_array) :
    if first_diagonal_winner(temp_array, cross) or second_diagonal_winner(temp_array, cross) : return True
    player_winner_test = False
    for i in range(size_game) :
        if line_winner(temp_array, i, cross) or column_winner(temp_array, i, cross) : player_winner_test = True
    return player_winner_test


def computer_winner(temp_array) :
    if first_diagonal_winner(temp_array, round) or second_diagonal_winner(temp_array, round) : return True
    computer_winner_test = False
    for i in range(size_game) :
        if line_winner(temp_array, i, round) or column_winner(temp_array, i, round) : computer_winner_test = True
    return computer_winner_test



def full_game(temp_array) :
    for row in temp_array:
        for col in row:
            if col == empty : return False
    return True


def end_game(temp_array) :
    if player_winner(temp_array) or computer_winner(temp_array) : return True
    if full_game(temp_array) : return True
    return False


def remaining_empty_spot(current_array) :
    for row in range(size_game) :
        for col in range(size_game) :
            if current_array[row][col] == empty :
                return True
    return False



def compute_points(temp_array, depth_coef) :
    if player_winner(temp_array) :
        return -depth_coef
    if computer_winner(temp_array) :
        return depth_coef
    if full_game(temp_array) :
        return 0.0000001




def list_sons(current_array, sign, index, depth_coef) :
    next_sign = cross
    if sign == cross : next_sign = round

    if not remaining_empty_spot(current_array) or end_game(current_array) :
        point_array[index] += compute_points(current_array, depth_coef)

    else :
        temp_chessboard = []
        for row in range(size_game) :
            for col in range(size_game) :
                if current_array[row][col] == empty :
                    temp_chessboard.append(deepcopy(current_array))
                    temp_chessboard[-1][row][col] = sign

        for son_chessboard in temp_chessboard :
            list_sons(son_chessboard, next_sign, index, depth_coef/100)




def list_legal_computer_choice() :
    for i in range(size_game*size_game):
        point_array[i] = 0
    temp_chessboard = []
    for row in range(size_game) :
        for col in range(size_game) :
            if game_state[row][col] == empty :
                temp_chessboard.append(deepcopy(game_state))
                temp_chessboard[-1][row][col] = round
                list_sons(temp_chessboard[-1], cross, size_game*row+col, 100000000)




def computer_start_game() :
    comp_win = False
    player_win = False
    game_full = False
    print('game begins : ')
    display(game_state)
    while True :
        list_legal_computer_choice()
        computer_choice()
        print('computer has played : ')
        display(game_state)
        if end_game(game_state) : break

        player_choice()
        print('You have played : ')
        display(game_state)
        if end_game(game_state) : break



def player_start_game() :
    comp_win = False
    player_win = False
    game_full = False
    print('game begins : ')
    display(game_state)
    while True :
        player_choice()
        print('You have played : ')
        display(game_state)
        if end_game(game_state) : break

        point_array = [0] * size_game*size_game
        list_legal_computer_choice()
        computer_choice()
        print('computer has played : ')
        display(game_state)
        if end_game(game_state) : break




def start_game() :
    print('Type "x" at any moment to exit the game')
    print('Choose the beginner')
    print('Computer begins : X')
    print('You begin : M')
    beginner = input('Your choice : ')
    while beginner != 'M' and beginner != 'X' :
        beginner = input('Illegal choice : ')

    if beginner == 'X' : computer_start_game()
    if beginner == 'M' : player_start_game()

    if player_winner(game_state) : print('You are the winner !!')
    if computer_winner(game_state) : print('You are the loser !!')
    if not player_winner(game_state) and not computer_winner(game_state) and full_game(game_state) : print('No winner !!')



start_game()







#
