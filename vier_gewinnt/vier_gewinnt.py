board = []
width = 7
height = 6
min_connected_for_win = 4
players = [input("Player "+str(i+1)+", please enter your name: ") for i in range(2)]
current_player = 0
chips = ["X", "O"]

def print_board():
    # die erste zeile
    print(" ".join([str(x) for x in range(1, width+1)]))
    # die folgenden zeilen
    for line in board:
        # join fügt das zwischen den elementen ein
        print("|".join(line))

# vier gewinnt
def game_ended():
    result = False

    # this variable store all the chains of chips that we want to test
    # first, this includes all horizontal lines (a copy of the board)
    test_lines = board[0:] # this creates a shallow copy of the board
    # add columns, (swap x and y)
    for x in range(0, width):
        test_lines.append([])
        for y in range(0, height):
            test_lines[-1].append(test_lines[y][x])
    # add diagonals
    top_down = [0, 0]
    bottom_up = [0, height-1]
    for i in range(0, height):
        test_lines.append([]) # new top down diagonal, links entlang
        j = 0
        while top_down[1] + j < height and top_down[0] + j < width:
            # y läuft entlang des boards, welches vertikal orientiert ist
            test_lines[-1].append(board[top_down[1] + j][top_down[0] + j])
            j += 1
        test_lines.append([]) # new bottom up diagonal, links entlang
        j = 0
        while bottom_up[1] - j >= 0 and bottom_up[0] + j < width:
            test_lines[-1].append(board[bottom_up[1] - j][bottom_up[0] + j])
            j += 1
        top_down[1] += 1
        bottom_up[1] -= 1
    top_down = [0, 0]
    bottom_up = [0, height-1]
    for i in range(0, width-1):
        top_down[0] += 1
        bottom_up[0] += 1
        test_lines.append([]) # new top down diagonal, oben entlang
        j = 0
        while top_down[1] + j < height and top_down[0] + j < width:
            test_lines[-1].append(board[top_down[1] + j][top_down[0] + j])
            j += 1
        test_lines.append([]) # new bottom up diagonal, unten entlang
        j = 0
        while bottom_up[1] - j >= 0 and bottom_up[0] + j < width:
            test_lines[-1].append(board[bottom_up[1] - j][bottom_up[0] + j])
            j += 1

    # durchlauf der zusammengefügten test_lines
    for line in test_lines:
        # count of successively placed chips
        connected_count = 0
        connected_player = 0
        for chip in line:
            # in der luft
            if chip == "_":
                connected_count = 0
                continue
            # zuweisung des indexes
            chip_player = chips.index(chip)
            if connected_count == 0 or connected_player != chip_player:
                connected_count = 1
                connected_player = chip_player
            else:
                connected_count += 1
            # erzielte anzahl an hintereinanderliegenden
            if connected_count == min_connected_for_win:
                result = True
                break
        if result:
            break

    if result:
        print_board()
        print("\n***************************")
        print(players[connected_player]+", YOU WON!")
        print("***************************")
    return result

print("Hello",players[0],"and",players[1],", fight!")

# erstellung des spielfeldes, während das board vertikal orientiert ist
for y in range(height):
    board.append([])
    for x in range(width):
        board[-1].append("_")

# main loop
while not game_ended():
    print("=" * (width * 4))
    print_board()
    print("\nPlayer",players[current_player],", your move!")

    # selection of column
    col = -1
    while col < 0:
        try:
            col = int(input("Enter column: "))
            # ob die spalte innerhalb der breite sich befindet
            if col not in range(1, width+1):
                col = -1
            # ob die spalte voll ist
            elif board[0][col-1] != "_":
                print("Column is full!")
                col = -1
        except ValueError:
            continue
    col -= 1 # make column-index 0 based

    row = 0
    # solange der boden nicht erreicht wird und er sich in der luft befindet
    while (row+1) < height and board[row+1][col] == "_":
        row += 1

    # der chip des zugehörigen spielers ist gefallen
    board[row][col] = chips[current_player]
    # alternation zwischen 0 und 1
    current_player = 1 - current_player