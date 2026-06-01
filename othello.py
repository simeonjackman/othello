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
        



# Zeichnet das Spielbrett
def draw_board():
    cell_size = int(400/size)
    for y, _ in enumerate(board):
        for x, value in enumerate(board[y]):
            setPenColor("black")
            setPos(-400 + (size + 1) * cell_size + x * cell_size, -100 + y * cell_size)
            setFillColor("green")
            startPath()
            repeat 4:
                forward(cell_size)
                right(90)
            fillPath()
            setPos(-400 + (size + 1.5) * cell_size + x * cell_size, -100 + (y + 0.5) * cell_size)
            if value == "WHITE":
                setPenColor("white")
                dot(50)
            if value == "BLACK":
                setPenColor("black")
                dot(cell_size)
            
draw_board()

