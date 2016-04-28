board = []
width = 7
height = 6
min_connected = 4
players = [input("Player "+str(i)+", please enter your name: ") for i in range(2)]
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
    # die anzahl der hintereinanderliegenden chips
    connected_count = 0
    connected_player = 0

    test_lines = board[0:]
    # add columns, vertauschung des x und y
    for x in range(0, width):
        test_lines.append([])
        for y in range(0, height):
            test_lines[-1].append(test_lines[y][x])    

    # durchlauf der hintereinanderliegenden
    for line in test_lines:
        for chip in line:
            # in der luft
            if chip == "_":
                connected_count = 0
                continue
            chip_player = chips.index(chip)
            if connected_count == 0 or connected_player != chip_player:
                connected_count = 1
                connected_player = chip_player
            else:
                connected_count += 1
            # erzielte anzahl an hintereinanderliegenden
            if connected_count == min_connected:
                result = True
                break
        if result:
            break
        
    if result:
        print(players[connected_player]+", YOU WON!")
    return result

print("Hello",players[0],"and",players[1],", fight!")

# erstellung des spielfeldes, während das board vertikal orientiert ist
for y in range(height):
    board.append([])
    for x in range(width):
        board[-1].append("_")

# selektion der spalte
while not game_ended():
    print_board()
    print("Player",players[current_player],", your move!")

    col = -1
    while col < 0:
        try:
            col = int(input("Enter column: "))
            print(board[0][col-1])
            # ob die spalte innerhalb der breite sich befindet
            if col not in range(1, width+1):
                col = -1
            # ob die spalte voll ist
            elif board[0][col-1] != "_":
                print("Column is full!")
                col = -1
        except ValueError:
            continue
    col -= 1

    row = 0
    # solange der boden nicht erreicht wird und er sich in der luft befindet
    while (row+1) < height and board[row+1][col] == "_":
        row += 1

    # der chip des zugehörigen spielers ist gefallen
    board[row][col] = chips[current_player]
    # alternation zwischen 0 und 1
    current_player = 1 - current_player
