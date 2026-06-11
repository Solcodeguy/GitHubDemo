from random import randrange

# ------------------------------
# Display the board
# ------------------------------
def display_board(board):
    print("+-------+-------+-------+")
    for row in board:
        print("|       |       |       |")
        print(f"|   {row[0]}   |   {row[1]}   |   {row[2]}   |")
        print("|       |       |       |")
        print("+-------+-------+-------+")

# ------------------------------
# Check if someone has won
# ------------------------------
def victory_for(board, sign):
    # Rows
    for r in range(3):
        if board[r][0] == board[r][1] == board[r][2] == sign:
            return True

    # Columns
    for c in range(3):
        if board[0][c] == board[1][c] == board[2][c] == sign:
            return True

    # Diagonals
    if board[0][0] == board[1][1] == board[2][2] == sign:
        return True
    if board[0][2] == board[1][1] == board[2][0] == sign:
        return True

    return False

# ------------------------------
# Get user's move
# ------------------------------
def enter_move(board):
    while True:
        move = input("Enter your move (1-9): ")

        if not move.isdigit():
            print("Not a number. Try again.")
            continue

        move = int(move)
        if move < 1 or move > 9:
            print("Number must be 1–9.")
            continue

        # Convert move to row/col
        row = (move - 1) // 3
        col = (move - 1) % 3

        if board[row][col] in ['X', 'O']:
            print("That square is already taken.")
            continue

        board[row][col] = 'O'
        break

# ------------------------------
# Computer move (random)
# ------------------------------
def make_list_of_free_fields(board):
    free = []
    for r in range(3):
        for c in range(3):
            if board[r][c] not in ['X', 'O']:
                free.append((r, c))
    return free

def draw_move(board):
    free = make_list_of_free_fields(board)
    if not free:
        return

    r, c = free[randrange(len(free))]
    board[r][c] = 'X'

# ------------------------------
# Main game logic
# ------------------------------
def tic_tac_toe():
    # Initial board with numbers
    board = [
        ['1', '2', '3'],
        ['4', '5', '6'],
        ['7', '8', '9']
    ]

    # Computer starts in the center
    board[1][1] = 'X'

    while True:
        display_board(board)

        # User move
        enter_move(board)
        if victory_for(board, 'O'):
            display_board(board)
            print("You win!")
            break

        if not make_list_of_free_fields(board):
            display_board(board)
            print("It's a tie!")
            break

        # Computer move
        draw_move(board)
        if victory_for(board, 'X'):
            display_board(board)
            print("Computer wins!")
            break

        if not make_list_of_free_fields(board):
            display_board(board)
            print("It's a tie!")
            break

# Run the game
tic_tac_toe()
