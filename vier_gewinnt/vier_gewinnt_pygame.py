# !/usr/local/bin/python3

import pygame

board = []
board_width = 7
board_height = 6
min_connected_for_win = 4
current_player = 0
colors = [
    pygame.Color(0x5e, 0x56, 0x5a),
    pygame.Color(0xa9, 0xcb, 0xb7),
    pygame.Color(0xf7, 0xff, 0x58),
    pygame.Color(0xff, 0x93, 0x4f)
]

def draw_board(surface, width, height, sel_col):
    cell_width = int(width/board_width)
    cell_height = int(height/board_height)
    y = 0
    for line in board:
        x = 0
        for cell in line:
            color = colors[0]
            if cell == 0:
                color = colors[1]
            elif cell == 1:
                color = colors[2]
            pygame.draw.rect(surface, color, pygame.Rect(x+1, y+1, cell_width-1, cell_height-1))
            x += cell_width
        y += cell_height
    if sel_col >= 0:
        pygame.draw.rect(surface, colors[3], pygame.Rect(sel_col*cell_width, 0, cell_width, height), 1)

# vier gewinnt
def game_ended():
    result = False

    # this variable store all the chains of chips that we want to test
    # first, this includes all horizontal lines (a copy of the board)
    test_lines = []

    # add rows
    for y in range(0, board_height):
        test_lines.append([])
        for x in range(0, board_width):
            test_lines[-1].append((y, x))

    # add columns, (swap x and y)
    for x in range(0, board_width):
        test_lines.append([])
        for y in range(0, board_height):
            test_lines[-1].append((y, x))

    # add diagonals
    top_down = [0, 0]
    bottom_up = [0, board_height - 1]
    for i in range(0, board_height):
        # new top down diagonal, links entlang
        test_lines.append([])
        j = 0
        while top_down[1] + j < board_height and top_down[0] + j < board_width:
            # y läuft entlang des boards, welches vertikal orientiert ist
            test_lines[-1].append((top_down[1] + j, top_down[0] + j))
            j += 1
        # new bottom up diagonal, links entlang
        test_lines.append([])
        j = 0
        while bottom_up[1] - j >= 0 and bottom_up[0] + j < board_width:
            test_lines[-1].append((bottom_up[1] - j, bottom_up[0] + j))
            j += 1
        top_down[1] += 1
        bottom_up[1] -= 1
    top_down = [0, 0]
    bottom_up = [0, board_height - 1]
    for i in range(0, board_width-1):
        top_down[0] += 1
        bottom_up[0] += 1
        # new top down diagonal, oben entlang
        test_lines.append([])
        j = 0
        while top_down[1] + j < board_height and top_down[0] + j < board_width:
            test_lines[-1].append((top_down[1] + j, top_down[0] + j))
            j += 1
        # new bottom up diagonal, unten entlang
        test_lines.append([])
        j = 0
        while bottom_up[1] - j >= 0 and bottom_up[0] + j < board_width:
            test_lines[-1].append((bottom_up[1] - j, bottom_up[0] + j))
            j += 1

    # index des spielers der gewonnen hat
    connected_player = 0
    connected = []

    # durchlauf der zusammengefügten test_lines
    for line in test_lines:
        # count of successively placed chips
        connected.clear()
        for coords in line:
            # in der luft
            chip = board[coords[0]][coords[1]]
            if chip == -1:
                connected.clear()
                continue
            # zuweisung des indexes
            if len(connected) == 0 or connected_player != chip:
                connected = [coords]
                connected_player = chip
            else:
                connected.append(coords)
            # erzielte anzahl an hintereinanderliegenden
            if len(connected) == min_connected_for_win:
                result = True
                break
        if result:
            break

    if result:
        # alles außer gewinn vom board entfernen
        for y in range(0, board_height):
            for x in range(0, board_width):
                if (y, x) not in connected:
                    board[y][x] = -1

    return result

pygame.init()

screen_size = (board_width*40, board_height*40)
window = pygame.display.set_mode(screen_size)
screen = pygame.display.get_surface()
pygame.display.set_caption("4 gewinnen!")

# Fill background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))

heartbeat = pygame.time.Clock()
selected_col = 0

# erstellung des spielfeldes, während das board vertikal orientiert ist
for y in range(board_height):
    board.append([])
    for x in range(board_width):
        board[-1].append(-1)

winner_emerged = False
game_quit = False

while not game_quit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and not winner_emerged:
                selected_col += 1
            elif event.key == pygame.K_LEFT and not winner_emerged:
                selected_col -= 1
            elif (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE) and not winner_emerged:
                row = 0
                # solange der boden nicht erreicht wird und er sich in der luft befindet
                while (row + 1) < board_height and board[row + 1][selected_col] == -1:
                    row += 1
                # der chip des zugehörigen spielers ist gefallen
                board[row][selected_col] = current_player
                # alternation zwischen 0 und 1
                current_player = 1 - current_player
                winner_emerged = game_ended()
                if winner_emerged:
                    selected_col = -1
            elif event.key == pygame.K_ESCAPE:
                game_quit = True

    if not winner_emerged:
        if selected_col < 0:
            selected_col = 0
        elif selected_col >= len(board[0]):
            selected_col = len(board[0]) - 1

    screen.blit(background, (0, 0))
    draw_board(screen, screen_size[0], screen_size[1], selected_col)

    pygame.display.update()
    heartbeat.tick(60)

pygame.display.quit()
