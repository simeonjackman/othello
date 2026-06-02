import random
from gturtle import *

# Turtle zum Zeichnen verstecken
makeTurtle()
hideTurtle()

# Konfiguration

# Brettgrösse
size = 8 # Hier kann das Brett grösser gemacht werden

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
print board
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
        
# Zeichnet das Spielbrett
def draw_board():
    cell_size = int(400/size)
    setFontSize(20)
    x_offset = 0 # Verschieben auf der X-Achse
    y_offset = 0 # Verschieben auf der Y-Achse
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
            
            
draw_board()

