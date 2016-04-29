
board = []
width = 7
height = 6
min_connected_for_win = 4

chips = ["X", "O"]
players = [input("Player "+str(i)+", please enter your name: ") for i in range(2)]

print("Hello",players[0],"and",players[1],", fight!")

for y in range(height):
    board.append([])
    for x in range(width):
        board[-1].append("_")

def print_board():
    print(" ".join([str(x) for x in range(1, width+1)]))
    for line in board:
        print("|".join(line))

def game_ended():
    result = False

    connected_count = 0
    connected_player = 0

    test_lines = board[0:]
    # add columns
    for x in range(0, width):
        test_lines.append([])
        for y in range(0, height):
            test_lines[-1].append(test_lines[y][x])

    for line in test_lines:
        for chip in line:
            if chip == "_":
                connected_count = 0
                continue

            chip_player = chips.index(chip)
            if connected_count == 0 or connected_player != chip_player:
                connected_count = 1
                connected_player = chip_player
            else:
                connected_count += 1

            if connected_count == min_connected_for_win:
                result = True
                break

        if result:
            break

    if result:
        print(players[connected_player]+", YOU WON!")

    return result

current_player = 0

while not game_ended():
    print_board()
    print("Player",players[current_player],", your move!")
    col = -1
    while col < 0:
        try:
            col = int(input("Enter column: "))
            if col not in range(1, width+1):
                col = -1
            elif board[0][col-1] != "_":
                print("Column is full!")
                col = -1
        except ValueError:
            continue
    col -= 1
    row = 0
    while (row+1) < height and board[row+1][col] == "_":
        row += 1
    board[row][col] = chips[current_player]
    current_player = 1 - current_player
