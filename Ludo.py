
import pygame
from   pygame import K_ESCAPE, SCALED, mixer
import random
import time

pygame.init()
pygame.display.set_caption("Ludo  by Mehran")
screen = pygame.display.set_mode((680, 700),SCALED)

#things that I don't do
name = pygame.image.load('Name.png')
board = pygame.image.load('Board.png')
star  = pygame.image.load('star.png')
one   = pygame.image.load('1.png')
two   = pygame.image.load('2.png')
three = pygame.image.load('3.png')
four  = pygame.image.load('4.png')
five  = pygame.image.load('5.png')
six   = pygame.image.load('6.png') 

red    = pygame.image.load('red.png')
blue   = pygame.image.load('blue.png')
green  = pygame.image.load('green.png')
yellow = pygame.image.load('yellow.png')

DICE  = [one, two, three, four, five, six]
color = [red, green, yellow, blue]

killSound   = mixer.Sound("Killed.wav")
tokenSound  = mixer.Sound("Token Movement.wav")
diceSound   = mixer.Sound("Dice Roll.wav")
winnerSound = mixer.Sound("Reached Star.wav")

# Initializing Variables

number        = 1
currentPlayer = 0
playerKilled  = False
diceRolled    = False
winnerRank    = []
start = False

font = pygame.font.Font('freesansbold.ttf', 11)
FONT = pygame.font.Font('freesansbold.ttf', 16)


HOME = [[(110, 58),  (61, 107),  (152, 107), (110, 152)],  # Red
        [(466, 58),  (418, 107), (509, 107), (466, 153)],  # Green
        [(466, 415), (418, 464), (509, 464), (466, 510)],  # Yellow
        [(110, 415), (61, 464),  (152, 464), (110, 510)]]  # Blue

        # R          G          Y          B
SAFE = [(50, 240), (328, 50), (520, 328), (240, 520),
        (88, 328), (240, 88), (482, 240), (328, 482)]
DicePosition=[(175,173),(531,173),(531,375),(173,375)]
position = [[[110, 58],  [61, 107],  [152, 107], [110, 152]],  # Red
            [[466, 58],  [418, 107], [509, 107], [466, 153]],  # Green
            [[466, 415], [418, 464], [509, 464], [466, 510]],  # Yellow
            [[110, 415], [61, 464],  [152, 464], [110, 510]]]  # Blue

jump = {(202, 240): (240, 202),  # Red to Green
        (328, 202): (368, 240),  # Gren to yellow
        (368, 328): (328, 368),  # Yellow to blue
        (240, 368): (202, 328)}  # Blue to red

         # R           G            Y          B
WINNER = [[240, 284], [284, 240], [330, 284], [284, 330]]
pygame.freetype.get_default_font() 
# Movement
def re_initialize():
    global number,currentPlayer,playerKilled,diceRolled,winnerRank,HOME,SAFE,DicePosition,position,jump,WINNER
    number   = 1
    currentPlayer = 0
    playerKilled  = False
    diceRolled    = False
    winnerRank    = []
        
    HOME = [[(110, 58),  (61, 107),  (152, 107), (110, 152)],  # Red
            [(466, 58),  (418, 107), (509, 107), (466, 153)],  # Green
            [(466, 415), (418, 464), (509, 464), (466, 510)],  # Yellow
            [(110, 415), (61, 464),  (152, 464), (110, 510)]]  # Blue

            # R          G          Y          B
    SAFE = [(50, 240), (328, 50), (520, 328), (240, 520),
            (88, 328), (240, 88), (482, 240), (328, 482)]
    DicePosition=[(175,173),(531,173),(531,375),(173,375)]
    position = [[[110, 58],  [61, 107],  [152, 107], [110, 152]],  # Red
                [[466, 58],  [418, 107], [509, 107], [466, 153]],  # Green
                [[466, 415], [418, 464], [509, 464], [466, 510]],  # Yellow
                [[110, 415], [61, 464],  [152, 464], [110, 510]]]  # Blue

    jump = {(202, 240): (240, 202),  # Red to Green
            (328, 202): (368, 240),  # Gren to yellow
            (368, 328): (328, 368),  # Yellow to blue
            (240, 368): (202, 328)}  # Blue to red

            # R           G            Y          B
    WINNER = [[240, 284], [284, 240], [330, 284], [284, 330]]

def show_token(x, y):
    screen.fill((0, 0, 0))
    screen.blit(board, (0, 0))
    screen.blit(name,(0,600))
    for i in SAFE[4:]:
        screen.blit(star, i)

    for i in range(len(position)):
        for j in position[i]:
            screen.blit(color[i], j)

    screen.blit(DICE[number-1], DicePosition[currentPlayer])

    if position[x][y] in WINNER:
        winnerSound.play()
    else:
        tokenSound.play()


    for i in range(len(winnerRank)):
        rank = FONT.render(f'Position :{i+1}.', True, (0, 0, 0))
        screen.blit(rank, (600, 85 + (40*i)))
        screen.blit(color[winnerRank[i]], (620, 75 + (40*i)))

    pygame.display.update()
    time.sleep(0.5)


def show_all():

    for i in SAFE[4:]:
        screen.blit(star, i)

    for i in range(len(position)):
        for j in position[i]:
            screen.blit(color[i], j)

    screen.blit(DICE[number-1], DicePosition[currentPlayer])



    for i in range(len(winnerRank)):
        rank = FONT.render(f'{i+1}.', True, (0, 0, 0))
        screen.blit(rank, (600, 85 + (40*i)))
        screen.blit(color[winnerRank[i]], (620, 75 + (40*i)))
    screen.blit(name,(0,600))


def is_possible(x, y):
    #  R2
    if (position[x][y][1] == 284 and position[x][y][0] <= 202 and x == 0) \
            and (position[x][y][0] + 38*number > WINNER[x][0]):
        return False

    #  Y2
    elif (position[x][y][1] == 284 and 368 < position[x][y][0] and x == 2) \
            and (position[x][y][0] - 38*number < WINNER[x][0]):
        return False
    #  G2
    elif (position[x][y][0] == 284 and position[x][y][1] <= 202 and x == 1) \
            and (position[x][y][1] + 38*number > WINNER[x][1]):
        return False
    #  B2
    elif (position[x][y][0] == 284 and position[x][y][1] >= 368 and x == 3) \
            and (position[x][y][1] - 38*number < WINNER[x][1]):
        return False
    return True

# Moving the token

def move_token(x, y):
    global currentPlayer, diceRolled

    # Taking Token out of HOME
    if tuple(position[x][y]) in HOME[currentPlayer] and number == 6:
        position[x][y] = list(SAFE[currentPlayer])
        tokenSound.play()
        diceRolled = False

    # Moving token which is not in HOME
    elif tuple(position[x][y]) not in HOME[currentPlayer]:
        diceRolled = False
        if not number == 6:
            currentPlayer = (currentPlayer+1) % 4

        # Way to WINNER position

        #  R2
        if (position[x][y][1] == 284 and position[x][y][0] <= 202 and x == 0) \
                and (position[x][y][0] + 38*number <= WINNER[x][0]):
            for i in range(number):
                position[x][y][0] += 38
                show_token(x, y)

        #  Y2
        elif (position[x][y][1] == 284 and 368 < position[x][y][0] and x == 2) \
                and (position[x][y][0] - 38*number >= WINNER[x][0]):
            for i in range(number):
                position[x][y][0] -= 38
                show_token()

        #  G2
        elif (position[x][y][0] == 284 and position[x][y][1] <= 202 and x == 1) \
                and (position[x][y][1] + 38*number <= WINNER[x][1]):
            for i in range(number):
                position[x][y][1] += 38
                show_token()
        #  B2
        elif (position[x][y][0] == 284 and position[x][y][1] >= 368 and x == 3) \
                and (position[x][y][1] - 38*number >= WINNER[x][1]):
            for i in range(number):
                position[x][y][1] -= 38
                show_token()

        # Other Paths
        else:
            for _ in range(number):

                #  R1, Y3
                if (position[x][y][1] == 240 and position[x][y][0] < 202) \
                        or (position[x][y][1] == 240 and 368 <= position[x][y][0] < 558):
                    position[x][y][0] += 38
                # R3 -> R2 -> R1
                elif (position[x][y][0] == 12 and position[x][y][1] > 240):
                    position[x][y][1] -= 44

                #  R3, Y1
                elif (position[x][y][1] == 328 and 12 < position[x][y][0] <= 202) \
                        or (position[x][y][1] == 328 and 368 < position[x][y][0]):
                    position[x][y][0] -= 38
                #  Y3 -> Y2 -> Y1
                elif (position[x][y][0] == 558 and position[x][y][1] < 328):
                    position[x][y][1] += 44

                #  G3, B1
                elif (position[x][y][0] == 240 and 12 < position[x][y][1] <= 202) \
                        or (position[x][y][0] == 240 and 368 < position[x][y][1]):
                    position[x][y][1] -= 38
                # G3 -> G2 -> G1
                elif (position[x][y][1] == 12 and 240 <= position[x][y][0] < 328):
                    position[x][y][0] += 44

                #  B3, G1
                elif (position[x][y][0] == 328 and position[x][y][1] < 202) \
                        or (position[x][y][0] == 328 and 368 <= position[x][y][1] < 558):
                    position[x][y][1] += 38
                #  B3 -> B2 -> B1
                elif (position[x][y][1] == 558 and position[x][y][0] > 240):
                    position[x][y][0] -= 44
                
                else:
                    for i in jump:
                        if position[x][y] == list(i):
                            position[x][y] = list(jump[i])
                            break

                show_token(x, y)

        # Ki Player
        if tuple(position[x][y]) not in SAFE:
            for i in range(len(position)):
                for j in range(len(position[i])):
                    if position[i][j] == position[x][y] and i != x:
                        position[i][j] = list(HOME[i][j])
                        killSound.play()
                        currentPlayer = x # (currentPlayer+3) % 4


# Checking Winner
def check_winner():
    global currentPlayer
    if currentPlayer not in winnerRank:
        for i in position[currentPlayer]:
            if i not in WINNER:
                return
        winnerRank.append(currentPlayer)
    else:
        currentPlayer = (currentPlayer + 1) % 4


    
    # Main LOOP
running = True
while(running):

   
        
    screen.fill((0, 0, 0))
    screen.blit(board, (0, 0)) # Bliting Board

    check_winner()

    for event in pygame.event.get():

        # Event QUIT
        if event.type == pygame.QUIT or (event.type== pygame.KEYUP and event.key==K_ESCAPE):
            running = False

        # When MOUSEBUTTON is clicked
        if event.type == pygame.MOUSEBUTTONUP:
            coordinate = pygame.mouse.get_pos()

            # Rolling Dice
            if not diceRolled and (DicePosition[currentPlayer][1] <= coordinate[1] <= DicePosition[currentPlayer][1]+49) and (DicePosition[currentPlayer][0] <= coordinate[0] <= DicePosition[currentPlayer][0]+49):
                number = random.randint(1, 6)
                diceSound.play()
                flag = True
                for i in range(len(position[currentPlayer])):
                    if tuple(position[currentPlayer][i]) not in HOME[currentPlayer] and is_possible(currentPlayer, i):
                        flag = False
                if (flag and number == 6) or not flag:
                    diceRolled = True

                else:
                    currentPlayer = (currentPlayer+1) % 4

            # Moving Player
            elif diceRolled:
                for j in range(len(position[currentPlayer])):
                    if position[currentPlayer][j][0] <= coordinate[0] <= position[currentPlayer][j][0]+31 \
                            and position[currentPlayer][j][1] <= coordinate[1] <= position[currentPlayer][j][1]+31:
                        move_token(currentPlayer, j)
                        break
        
            
    show_all()

    pygame.display.update()
