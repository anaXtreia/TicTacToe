#/usr/bin/python3
import pygame
import math

WINDOW_WIDTH = 720
WINDOW_HEIGHT = 720
BUTTON_RADIUS = WINDOW_HEIGHT/6-20


"""
Analyzes the board to check if there are places left to play (Draw)
If no one wins returns True, otherwise, returns False
"""
def noOneWins(board):
    
    for i in range(1,10):
        if board[i] in range (1,10):
            return False
        
    return True

def printEndMenu_gui(window, winner):

    window.fill((255,255,255))
    if winner == 0:
        result = pygame.image.load("assets/drawMenu.png").convert()
    elif winner == 1:
        result = pygame.image.load("assets/winMenu1.png").convert()
    elif winner == 2: 
        result = pygame.image.load("assets/winMenu2.png").convert()
    window.blit(result, (0,0))
    pygame.display.update()

def playerPlay_gui(board, player, events, window):
    """Gets player input (mouse click) from the GUI"""
    button_positions = getGameButtonPositions(window)

    for event in events:
        if event.type == pygame.MOUSEBUTTONUP:
            button_idx = getPressedButton(button_positions)
            if validPlay(board, button_idx+1):
                board[button_idx+1] = player
                return True, board
    
    return False, board

def printBoard_gui(board, window, players, playerSymbols):

    window.fill((255,255,255))
    board_art = pygame.image.load("assets/grid.png").convert()
    window.blit(board_art, (0,0))
    button_positions = getGameButtonPositions(window)
    for i in range(1,10):
        for player in players:
            if board[i] == player:
                position = (button_positions[i-1][0]-playerSymbols[player].get_rect().width/2,button_positions[i-1][1]-playerSymbols[player].get_rect().height/2)
                window.blit(playerSymbols[player], position)
    
    pygame.display.update()


def getGameButtonPositions(window):
    """ Gets list of grid button positions"""
    window_width, window_height = window.get_size()
    return [(x,y) for y in range(int(window_height/6),int(window_height),int(window_height/3)) for x in range(int(window_width/6),int(window_width),int(window_width/3))]


def loadSymbolDictionary_gui(players):

    cross = pygame.image.load("assets/cross.png").convert()
    circle = pygame.image.load("assets/circle.png").convert()
    return {players[0]:cross,players[1]: circle}


def getMenuInput_gui(window):
    """Gets player input from the menu"""
    window_width, window_height = window.get_size()
    button_positions = [(200,window_height/2),(505,window_width/2)]

    for event in events:
        if event.type == pygame.MOUSEBUTTONUP:
            button_idx = getPressedButton(button_positions)
            if button_idx == 0:
                return True, "S"
            elif button_idx == 1:
                return True, "Q"
    
    return False, ""

"""Prints the menu in the pygame window"""
def printMenu_gui(board, window):
    board = pygame.image.load("assets/startMenu.png").convert()
    window.blit(board, (0,0))
    pygame.display.update()


def getPressedButton(button_positions):

    coordinates = pygame.mouse.get_pos()
    print("Mouse click on coordinates ",coordinates)
    for idx, position in enumerate(button_positions):
        if euclideanDistance(coordinates, position) < BUTTON_RADIUS:
            print("You have pressed button number ", idx+1)
            return idx
    return -1


def euclideanDistance(pointA, pointB):
    """sqrt((x1-x2)**2+(y1-y2)**2)"""
    dist = math.sqrt((pointA[0]-pointB[0])**2+(pointA[1]-pointB[1])**2)
    #print(dist)
    return dist


def initPygameWindow(width, height):

    window = pygame.display.set_mode((width, height))
    return window

def handleGeneralEvents(events):

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    return events

"""
Analyzes the board to check if any player has won the game. 
If a player has won returns True. If not, returns False
"""
def winnerFound(board):

    for i in range(1,10,3):
        if board[i] == board[i+1] == board[i+2] and board[i] not in range(1,10):
            print("Winner found!, Row ",i)
            return True
    for i in range(1,4):    
        if board[i] == board[i+3] == board[i+6] and board[i] not in range(1,10):
            print("Winner found, Column ",i)
            return True
    if (board[1] == board[5] == board[9] or board[3] == board[5] == board[7]) and board[5] not in range(1,10):
        print("Winner found!, diagonal")
        return True
    return False

"""Switches between the two players """
def switchPlayer(players, current_player):
    
    if current_player == players[0]:
        current_player = players[1]
    else:
        current_player = players[0]

    return current_player

"""
Checks if the play was valid.
Takes the current play and checks in the board if it is already checked or not.
If it is not checked, returns True, otherwise, returns False
"""
def validPlay(board, play):

    if play in range(1,10) and board[play] in range(1,10):
        return True
    
    return False

"""Gets input from the player in the CLI"""
def playerPlay_cli(board, player):
    play=-1
    while not validPlay(board, play):
        play = int(input("Player " + player + ", choose position to play from 1 to 9 "))
    board[play] = player
    return board

"""Prints the board in the command line"""
def printBoard_cli(board):
    for i in range(3):
        for j in range(1,4):
            print(str(board[i*3+j])+" ",end="")
        print("\n")

"""Setup board and first player"""
def setupGame(board, current_player, players):
    board = dict(zip(range(1, 10), range(1, 10)))
    current_player = players[0]
    return board, current_player


if __name__ == "__main__":
    print("Welcome to AnaX's TicTacToe")

    # Initialize pygame
    pygame.init()
    clock = pygame.time.Clock()
    window = initPygameWindow(WINDOW_WIDTH,WINDOW_HEIGHT)

    # setup section
    previous_state = "SETUP"
    current_state = "MENU"
    board = None
    players = ['A', 'X']
    playerSymbols = loadSymbolDictionary_gui(players)

    current_player = None

    board, current_player = setupGame(board, current_player, players)

    while(True):
        events = pygame.event.get()
        handleGeneralEvents(events)

        # while in the menu display
        if current_state == "MENU":
            printMenu_gui(board, window)
            valid_input = False
            valid_input, option = getMenuInput_gui(window)
            if valid_input:
                if option == "S":
                    printBoard_cli(board)
                    printBoard_gui(board, window, players, playerSymbols)
                    current_state = "GAME"
                else:
                    exit()

        # while playing
        elif current_state == "GAME":
            valid_play = False
            valid_play, board = playerPlay_gui(board, current_player, events, window)
            if valid_play:
                printBoard_cli(board)
                printBoard_gui(board, window, players, playerSymbols)

                if winnerFound(board):
                        print("Player " + current_player + " won!")
                        current_state = "GAMEOVER"
                        printEndMenu_gui(window, players.index(current_player)+1)
                elif noOneWins(board):
                    print("It's a draw!")
                    current_state = "GAMEOVER"
                    printEndMenu_gui(window, 0)

                current_player = switchPlayer(players, current_player)

        # when game is over, in end display
        elif current_state == "GAMEOVER":
            valid_input = False
            valid_input, option = getMenuInput_gui(window)
            if valid_input:
                if option == "S":
                    print("Cool! Starting a new game!")
                    board, current_player = setupGame(board, current_player, players)
                    printBoard_gui(board, window, players, playerSymbols)
                    printBoard_cli(board)
                    current_state = "GAME"
                else:
                    exit()
        
        # switching players
        if current_state != previous_state:
            print("Switching from state "+ previous_state + " to " + current_state)
            previous_state = current_state