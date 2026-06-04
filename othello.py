import random
from gturtle import *

# Turtle zum Zeichnen verstecken
makeTurtle()
hideTurtle()

##
# Konfiguration
##

# Brettgrösse
size = 8 # Hier kann das Brett grösser gemacht werden
# Wer darf beginnen
player_turn = "BLACK"
# Wie lange zwischen zügen pausiert wird in ms
turn_delay_timer = 0
# legale Züge anzeigen
show_legal_moves = True
# Zwischenstand nach möglichem Zug anzeigen
show_potential_score = False
# Für jeden Zug den Score ausgeben
show_move_score = True
# Verschieben des Spielfeldes auf der X-Achse
x_offset = 0 
# Verschieben des Spielfeldes auf der Y-Achse
y_offset = -200
# Grösse einer Zelle definieren
cell_size = int(400/size)


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

def score(board):
    white = 0
    black = 0
    for y in board:
        for x in y:
            if x == "WHITE":
                white +=1
            elif x == "BLACK":
                black +=1
                
    return (white,black)

def stone_count(player, game_board=board):
    white, black = score(game_board)
    if player == "WHITE":
        return white
    return black

# Wie sieht das Spielbrett nach einem Zug aus?
def board_after_move(player, move, game_board=board):
    global player_turn
    copied_board = []
    for y in game_board:
        copied_row = []
        for x in y:
            copied_row.append(x)
        copied_board.append(copied_row)

    previous_turn = player_turn
    apply_move(player, move, copied_board)
    player_turn = previous_turn
    return copied_board

# Was ist die Differenz der Steine nach meinem Zug?
# > 0 gut für weiss, < 0 gut für schwarz
def score_after_move(player, move, game_board=board):
    white, black = score(board_after_move(player, move, game_board))
    return white - black

# Wieviele Züge hat der Gegner nach meinem Zug?
def next_player_move_count_after_move(player, move, game_board=board):
    next_board = board_after_move(player, move, game_board)
    next_player = opponent(player)
    return len(get_legal_moves(next_player, next_board))

# Wieviele sichere Steine hat ein Spieler auf einem Brett?
def safestones(player, game_board=board):
    safe_positions = set()

    corners = [
        (0, 0, 1, 0, 0, 1),
        (size - 1, 0, -1, 0, 0, 1),
        (0, size - 1, 1, 0, 0, -1),
        (size - 1, size - 1, -1, 0, 0, -1),
    ]

    for corner_x, corner_y, edge_dx, edge_dy, edge2_dx, edge2_dy in corners:
        if game_board[corner_y][corner_x] != player:
            continue

        safe_positions.add((corner_x, corner_y))

        current_x = corner_x + edge_dx
        current_y = corner_y + edge_dy
        while 0 <= current_x < size and 0 <= current_y < size:
            if game_board[current_y][current_x] != player:
                break
            safe_positions.add((current_x, current_y))
            current_x += edge_dx
            current_y += edge_dy

        current_x = corner_x + edge2_dx
        current_y = corner_y + edge2_dy
        while 0 <= current_x < size and 0 <= current_y < size:
            if game_board[current_y][current_x] != player:
                break
            safe_positions.add((current_x, current_y))
            current_x += edge2_dx
            current_y += edge2_dy

    return len(safe_positions)

# Wieviele sichere Steine hat ein Spieler nach einem möglichen Zug?
def safestones_after_move(player, move, game_board=board):
    next_board = board_after_move(player, move, game_board)
    return safestones(player, next_board)

# Liegt ein möglicher Zug in einer Ecke, am Rand oder in der Mitte?
def move_position(move, game_board=board):
    if move == None:
        return "pass"

    x, y = move

    if (x == 0 or x == size - 1) and (y == 0 or y == size - 1):
        return "corner"

    if (x == 1 and (y == 0 or y == size - 1)) or (x == size - 2 and (y == 0 or y == size - 1)):
        return "c_field"

    if (y == 1 and (x == 0 or x == size - 1)) or (y == size - 2 and (x == 0 or x == size - 1)):
        return "c_field"

    if (x == 1 or x == size - 2) and (y == 1 or y == size - 2):
        return "x_field"

    if x == 0 or x == size - 1 or y == 0 or y == size - 1:
        return "edge"

    return "middle"

def get_legal_moves(player, game_board=board):
    legal_moves = []
    other = opponent(player)
    directions = [
        (-1, 1),  (0, 1),  (1, 1),
        (-1, 0),           (1, 0),
        (-1, -1), (0, -1), (1, -1),
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

# Wie viele mögliche Züge hat ein Spieler?
def possible_move_count(player, game_board=board):
    return len(get_legal_moves(player, game_board))

# Zeichnet Achsen
def draw_axis():
    setFontSize(20)
    for y, _ in enumerate(board):
        # x-Achse beschriften
        setPos(x_offset + (y+0.35) * cell_size, y_offset - 0.5*cell_size)
        setFillColor("black")
        label(y)
        # y-Achse beschriften
        setPos(x_offset - 0.5*cell_size, y_offset + (y+0.35) * cell_size)
        setFillColor("black")
        label(y)
            
    
# Zeichnet das Spielbrett
def draw_board():
    legal_moves = get_legal_moves(player_turn)
    for y, _ in enumerate(board):
        
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
                dot(cell_size)
            if value == "BLACK":
                setPenColor("black")
                dot(cell_size)
            if show_legal_moves and (x,y) in legal_moves:
                setPenColor("gray")
                dot(cell_size)
                if show_potential_score:
                    potential_score = score_after_move(player_turn, (x, y), board)
                    setFontSize(int(cell_size / 2))
                    setFillColor("black")
                    setPos(x_offset + (x + 0.25) * cell_size, y_offset + (y + 0.25) * cell_size)
                    setPenColor("black")
                    label(potential_score)

def apply_move(player, move, game_board=board):
    global player_turn
    other = opponent(player)
    player_turn = other
    if move == None:
        return
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

###
#  Manual Play
###
def manual_play(player, game_board=board):
    legal_moves = get_legal_moves(player, game_board)
    print player + " has " + str(safestones(player,board)) + " Safestones"
    if len(legal_moves) == 0:
        print player + " has to pass"
        apply_move(player, None, game_board)
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

###
#  Random Bot
###
def random_bot(player, game_board=board):
    legal_moves = get_legal_moves(player, game_board)
    if len(legal_moves) == 0:
        apply_move(player, None, game_board)
        return "Pass"

    move = random.choice(legal_moves)
    apply_move(player, move, game_board)
    return move

###
#  Mystery Bot
###
def mystery_bot(player, game_board=board):
    legal_moves = get_legal_moves(player, game_board)
    if len(legal_moves) == 0:
        apply_move(player, None, game_board)
        return "Pass"
    move = legal_moves[0]
    apply_move(player, move, game_board)
    return move
    
###
#  Genius Bot
###
def genius_bot(player, game_board=board):
    legal_moves = get_legal_moves(player, game_board)
    if len(legal_moves) == 0:
        apply_move(player, None, game_board)
        return "Pass"
    best_move = None
    best_score = -1000

    for move in legal_moves:
        move_score = score_after_move(player, move, game_board)
        if show_move_score:
            print("("+str(move[0])+","+str(move[1])+"):" + str(move_score))
        if player == "WHITE":
            if move_score > best_score:
                best_score = move_score
                best_move = move
        if player == "BLACK":
            if -move_score > best_score:
                best_score = -move_score
                best_move = move

    apply_move(player, best_move, game_board)
    return best_move

###
#  Bot Bot
###
def bot_bot(player, game_board=board):
    legal_moves = get_legal_moves(player, game_board)
    # Wenn wir keine Züge haben, müssen wir passen
    if len(legal_moves) == 0:
        apply_move(player, None, game_board)
        return "Pass"
    for move in legal_moves:
        # Wir prüfen, ob wir in einer Ecke spielen können
        if move_position(move) == "corner":
            apply_move(player, move, game_board)
            return move
        
    # Wir können nicht in die Ecken ziehen, deshalb prüfen wir, wieviele Steine wir umdrehen könnnen.
    # Wir nehmen den Zug, bei dem dies maximal ist.
    best_move = None
    best_score = -1000

    for move in legal_moves:
        move_score = score_after_move(player, move, game_board)
        if player == "WHITE":
            if move_score > best_score:
                best_score = move_score
                best_move = move
        if player == "BLACK":
            if -move_score > best_score:
                best_score = -move_score
                best_move = move
        
        if show_move_score:
            print("("+str(move[0])+","+str(move[1])+"):" + str(move_score))

    apply_move(player, best_move, game_board)
    return best_move

###
#  Tensai Bot
###
def tensai_bot(player, game_board=board):
    legal_moves = get_legal_moves(player, game_board)
    # Wenn wir keine Züge haben, müssen wir passen
    if len(legal_moves) == 0:
        apply_move(player, None, game_board)
        return "Pass"
    
    # Wir nehmen den Zug, bei dem der score maximal ist.
    best_move = None
    best_score = -1000

    for move in legal_moves:
        move_score = 0
        board_after_potential_move = board_after_move(player, move, game_board=board)

        # Wir berechnen, wieviele Safestones dazubekommen sind
        safestones_added = safestones(player, board_after_potential_move) - safestones(player, board)
        move_score += safestones_added * 4

        if move_position(move) == "corner":
            move_score += 10
        if move_position(move) == "edge":
            move_score += 7
        if move_position(move) == "middle":
            move_score += 0
        if move_position(move) == "c_field" or move_position(move) == "x_field":
            move_score += -10
        
        if show_move_score:
            print("("+str(move[0])+","+str(move[1])+"):" + str(move_score))
            
        # Ist der aktuelle Zug der Beste?
        if move_score > best_score:
            best_score = move_score
            best_move = move
        
    apply_move(player, best_move, game_board)
    return best_move

###
#  The Big Uttige Bot
###
def the_big_uttige_bot(player, game_board=board):
    legal_moves = get_legal_moves(player, game_board)
    # Wenn wir keine Züge haben, müssen wir passen
    if len(legal_moves) == 0:
        apply_move(player, None, game_board)
        return "Pass"
    for move in legal_moves:
        # Wir prüfen, ob wir in einer Ecke spielen können
        if move_position(move) == "corner":
            apply_move(player, move, game_board)
            return move
        # Wir prüfen, ob wir am Rand spielen können
        if move_position(move) == "edge":
            apply_move(player, move, game_board)
            return move
    
    # Sonst spielen wir einen random Zug
    move = random.choice(legal_moves)
    apply_move(player, move, game_board)
    return move

###
#  I-Ah Bot
###
def i_ah_bot(player, game_board=board):
    legal_moves = get_legal_moves(player, game_board)
    # Wenn wir keine Züge haben, müssen wir passen
    if len(legal_moves) == 0:
        apply_move(player, None, game_board)
        return "Pass"
        
    # Wir nehmen den Zug, bei dem der score maximal ist.
    best_move = None
    best_score = -1000

    # Wir prüfen jeden legalen Zug und bewerten ihn
    for move in legal_moves:
        move_score = 0
        board_after_potential_move = board_after_move(player, move, game_board=board)
        # Wir berechnen, wieviele Steine wir gedreht haben
        stones_turned = stone_count(opponent(player), board_after_potential_move) - stone_count(opponent(player), board)
        move_score += stones_turned
        # Wir berechnen, wieviele Safestones dazubekommen sind
        safestones_added = safestones(player, board_after_potential_move) - safestones(player, board)
        move_score += safestones_added * 2
        # Wir berechnen, wieviele Züge der Gegner nach einem potentiellen Zug hat
        options_after_move = possible_move_count(opponent(player), game_board=board_after_potential_move)
        move_score -= options_after_move
        # Wir evalieren wo wir unseren Stein hinsetzen
        if move_position(move) == "corner":
            move_score += 3
        if move_position(move) == "edge":
            move_score += 1
        if move_position(move) == "middle":
            move_score += 0
            
        if show_move_score:
            print("("+str(move[0])+","+str(move[1])+"):" + str(move_score))
        
        # Ist der aktuelle Zug der Beste?
        if move_score > best_score:
            best_score = move_score
            best_move = move
        
    apply_move(player, best_move, game_board)
    return best_move

###
#  Der Fels Bot
###
def der_fels_bot(player, game_board=board):
    legal_moves = get_legal_moves(player, game_board)
    # Wenn wir keine Züge haben, müssen wir passen
    if len(legal_moves) == 0:
        apply_move(player, None, game_board)
        return "Pass"
        
    # Wir nehmen den Zug, bei dem der score maximal ist.
    best_move = None
    best_score = -1000

    # Wir prüfen jeden legalen Zug und bewerten ihn
    for move in legal_moves:
        move_score = 0
        board_after_potential_move = board_after_move(player, move, game_board=board)
        # Wir berechnen, ob Safestones dazubekommen sind
        if safestones(player, board_after_potential_move) > safestones(player, board):
            move_score += 100
        # Wir evalieren wo wir unseren Stein hinsetzen
        if move_position(move) == "corner":
            move_score += 100
        if move_position(move) == "edge":
            move_score += 80
        if move_position(move) == "middle":
            move_score += 2

        # Wir berechnen, wieviele Steine wir gedreht haben
        stones_turned = stone_count(opponent(player), board_after_potential_move) - stone_count(opponent(player), board)
        move_score += stones_turned * 5

        if show_move_score:
            print("("+str(move[0])+","+str(move[1])+"):" + str(move_score))

        # Ist der aktuelle Zug der Beste?
        if move_score > best_score:
            best_score = move_score
            best_move = move
        
    apply_move(player, best_move, game_board)
    return best_move

###
#  King Silas Bot
###
def king_silas_bot(player, game_board=board):
    legal_moves = get_legal_moves(player, game_board)
    # Wenn wir keine Züge haben, müssen wir passen
    if len(legal_moves) == 0:
        apply_move(player, None, game_board)
        return "Pass"
        
    # Wir nehmen den Zug, bei dem der score maximal ist.
    best_move = None
    best_score = -1000

    # Wir prüfen jeden legalen Zug und bewerten ihn
    for move in legal_moves:
        move_score = 0
        board_after_potential_move = board_after_move(player, move, game_board=board)

        # Wir berechnen, wieviele Steine wir gedreht haben
        stones_turned = stone_count(opponent(player), board_after_potential_move) - stone_count(opponent(player), board)
        move_score += stones_turned * 2

        # Wir berechnen, ob Safestones dazubekommen sind
        if safestones(player, board_after_potential_move) > safestones(player, board):
            move_score += 10
        # Wir evalieren wo wir unseren Stein hinsetzen
        if move_position(move) == "corner":
            move_score += 15
        if move_position(move) == "edge":
            move_score += 6

        if show_move_score:
            print("("+str(move[0])+","+str(move[1])+"):" + str(move_score))

        # Ist der aktuelle Zug der Beste?
        if move_score > best_score:
            best_score = move_score
            best_move = move
        
    apply_move(player, best_move, game_board)
    return best_move

###
#  Chef Abi Bot
###
def chef_abi_bot(player, game_board=board):
    legal_moves = get_legal_moves(player, game_board)
    # Wenn wir keine Züge haben, müssen wir passen
    if len(legal_moves) == 0:
        apply_move(player, None, game_board)
        return "Pass"
        
    # Wir nehmen den Zug, bei dem der score maximal ist.
    best_move = None
    best_score = -1000

    # Wir prüfen jeden legalen Zug und bewerten ihn
    for move in legal_moves:
        move_score = 0
        board_after_potential_move = board_after_move(player, move, game_board=board)

        # Wir berechnen, wieviele Steine wir gedreht haben
        stones_turned = stone_count(opponent(player), board_after_potential_move) - stone_count(opponent(player), board)
        move_score += stones_turned * 5

        # Wir berechnen, ob Safestones dazubekommen sind
        if safestones(player, board_after_potential_move) > safestones(player, board):
            move_score += 50
        # Wir evalieren wo wir unseren Stein hinsetzen
        if move_position(move) == "corner":
            move_score += 100
        if move_position(move) == "edge":
            move_score += 15
            
        if show_move_score:
            print("("+str(move[0])+","+str(move[1])+"):" + str(move_score))

        # Ist der aktuelle Zug der Beste?
        if move_score > best_score:
            best_score = move_score
            best_move = move
        
    apply_move(player, best_move, game_board)
    return best_move

###
#  Sigma Bot
###
def sigma_bot(player, game_board=board):
    legal_moves = get_legal_moves(player, game_board)
    # Wenn wir keine Züge haben, müssen wir passen
    if len(legal_moves) == 0:
        apply_move(player, None, game_board)
        return "Pass"
        
    # Wir nehmen den Zug, bei dem der score maximal ist.
    best_move = None
    best_score = -1000

    # Wir prüfen jeden legalen Zug und bewerten ihn
    for move in legal_moves:
        move_score = 0
        board_after_potential_move = board_after_move(player, move, game_board=board)

        # Wir berechnen, wieviele Steine wir gedreht haben
        stones_turned = stone_count(opponent(player), board_after_potential_move) - stone_count(opponent(player), board)
        move_score += stones_turned / 4

        # Wir evalieren wo wir unseren Stein hinsetzen
        if move_position(move) == "corner":
            move_score += 5
        if move_position(move) == "edge":
            move_score += 2

        # Liegt ein möglicher Zug im inneren Ring um die Startpositionen?

        x, y = move
        center_left = int(size / 2) - 1
        center_right = int(size / 2)

        # Ist der Stein auf der linken Seite des inneren Rings?
        if x == center_left - 1 and y > 1 and  y < size - 2:
            move_score += 1
        # Ist der Stein auf der rechten Seite des inneren Rings?
        if x == center_right + 1 and y > 1 and  y < size - 2:
            move_score += 1
        # Ist der Stein auf der oberen Seite des inneren Rings?
        if y == center_right + 1 and x > 1 and  x < size - 2:
            move_score += 1
        # Ist der Stein auf der unteren Seite des inneren Rings?
        if y == center_left - 1 and x > 1 and  x < size - 2:
            move_score += 1

        if center_left <= x <= center_right and center_left <= y <= center_right:
            return False

        if show_move_score:
            print("("+str(move[0])+","+str(move[1])+"):" + str(move_score))

        # Ist der aktuelle Zug der Beste?
        if move_score > best_score:
            best_score = move_score
            best_move = move
        
    apply_move(player, best_move, game_board)
    return best_move

###
# Hier können Bots zum spielen gewählt werden
# Zur Auswahl stehen alle, welche im Code definiert wurden
# 1.  manual_play: Manuell spielen
# 2.  random_bot: Zufälligen Zug wählen
# 3.  mystery_bot: ?
# 4.  genius_bot: ?
# 5.  bot_bot
# 6.  tensai_bot
# 7.  the_big_uttige_bot
# 8.  i_ah_bot
# 9.  der_fels_bot
# 10. king_silas_bot
# 11. chef_abi_bot
# 12. sigma_bot
###


# Bot für schwarz wählen
player_1 = genius_bot
# Bot für weiss wählen
player_2 = random_bot

draw_axis()        
draw_board()
for i in range(32):
    print(player_turn + " plays:")
    print(player_1(player_turn))
    draw_board()
    delay(turn_delay_timer)
    print(player_turn + " plays:")
    print(player_2(player_turn))
    draw_board()
    delay(turn_delay_timer)

# Evaluieren wer gewonnen hat
end_result = score(board)
print("Result:" + str(end_result))
if end_result[0] > end_result[1]:
    print("White wins")
elif end_result[0] < end_result[1]:
    print("Black wins")
else:
    print("Its a draw")
