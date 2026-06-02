import random
from gturtle import *

# Turtle zum Zeichnen verstecken
makeTurtle()
hideTurtle()

# Konfiguration

# Brettgrösse
size = 8 # Hier kann das Brett grösser gemacht werden

# Wer darf beginnen
player_turn = "BLACK"

# Startposition definieren
board = []
for i, y in enumerate(range(size)):
    board.append([])
    for x in range(size):
        board[i].append("EMPTY")
# Startsteine legen
board[int(size/2)][int(size/2)] = "WHITE"
board[int(size/2)-1][int(size/2)-1] = "WHITE"
board[int(size/2)][int(size/2)-1] = "BLACK"
board[int(size/2)-1][int(size/2)] = "BLACK"

def opponent(player):
    if player == "BLACK":
        return "WHITE"
    return "BLACK"


def get_legal_moves(player, game_board=board):
    legal_moves = []
    other = opponent(player)
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1),
    ]

    for y in range(size):
        for x in range(size):
            if game_board[y][x] != "EMPTY":
                continue

            for dx, dy in directions:
                current_x = x + dx
                current_y = y + dy
                seen_other = False

                while 0 <= current_x < size and 0 <= current_y < size:
                    current_value = game_board[current_y][current_x]
                    if current_value == other:
                        seen_other = True
                    elif current_value == player and seen_other:
                        legal_moves.append((x, y))
                        break
                    else:
                        break

                    current_x += dx
                    current_y += dy

                if (x, y) in legal_moves:
                    break

    return legal_moves


def apply_move(player, move, game_board=board):
    global player_turn
    other = opponent(player)
    x, y = move
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1),
    ]

    game_board[y][x] = player

    for dx, dy in directions:
        current_x = x + dx
        current_y = y + dy
        stones_to_flip = []

        while 0 <= current_x < size and 0 <= current_y < size:
            current_value = game_board[current_y][current_x]
            if current_value == other:
                stones_to_flip.append((current_x, current_y))
            elif current_value == player:
                for flip_x, flip_y in stones_to_flip:
                    game_board[flip_y][flip_x] = player
                break
            else:
                break

            current_x += dx
            current_y += dy
    player_turn = other

def random_play(player, game_board=board):
    legal_moves = get_legal_moves(player, game_board)
    if len(legal_moves) == 0:
        return None

    move = random.choice(legal_moves)
    apply_move(player, move, game_board)
    return move


def manual_play(player, game_board=board):
    legal_moves = get_legal_moves(player, game_board)
    if len(legal_moves) == 0:
        print player + " has to pass"
        return None

    print player + " legal moves:"
    print legal_moves

    while True:
        user_input = input("Choose move as x,y: ")
        try:
            parts = user_input.replace(",", " ").split()
        except AttributeError:
            print "Invalid input. Enter two numbers separated by a comma."
            continue

        if len(parts) != 2:
            print "Invalid input. Enter two numbers, for example: 2 3"
            continue

        try:
            x = int(parts[0])
            y = int(parts[1])
        except ValueError:
            print "Invalid input. Enter numbers only."
            continue

        move = (x, y)
        if move not in legal_moves:
            print "Illegal move. Choose one of:", legal_moves
            continue

        apply_move(player, move, game_board)
        return move
        
# Zeichnet das Spielbrett
def draw_board():
    cell_size = int(400/size)
    setFontSize(20)
    x_offset = 0 # Verschieben auf der X-Achse
    y_offset = 0 # Verschieben auf der Y-Achse
    
    legal_moves = get_legal_moves(player_turn)
    
    for y, _ in enumerate(board):
        # x-Achse beschriften
        setPos(x_offset + (y+0.35) * cell_size, y_offset - 0.5*cell_size)
        setFillColor("black")
        label(y)
        # y-Achse beschriften
        setPos(x_offset - 0.5*cell_size, y_offset + (y+0.35) * cell_size)
        setFillColor("black")
        label(y)
        
        for x, value in enumerate(board[y]):
            setPenColor("black")
            setPos(x_offset + x * cell_size, y_offset + y * cell_size)
            setFillColor("green")
            startPath()
            repeat 4:
                forward(cell_size)
                right(90)
            fillPath()
            setPos(x_offset + (x+0.5) * cell_size, y_offset + (y + 0.5) * cell_size)
            if value == "WHITE":
                setPenColor("white")
                dot(50)
            if value == "BLACK":
                setPenColor("black")
                dot(cell_size)
            if (x,y) in legal_moves:
                setPenColor("gray")
                dot(50)
            
            
            
draw_board()
for i in range(61):
    print(player_turn + " plays:")
    print(manual_play(player_turn))
    draw_board()
    delay(1000)
    print(player_turn + " plays:")
    print(random_play(player_turn))
    draw_board()
    delay(1000)
