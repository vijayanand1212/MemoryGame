import pygame
from Tile import Tile
import random
import os

# Screen
SCREEN_SIZE = 600 + 35
SELECTED_TILE_POS_I = []
SELECTED_TILE_I = None;

SELECTED_TILE_POS_F = []
SELECTED_TILE_F = None;
COMPLETED_PAIR = 0
PAIRS_CLICKED = 0

PAUSE = True
WON =False
PAUSE_FIRST = True
GAMEOVER = False
HINTS = 3
HINT = False
# Board
BOARD = []
for i in range(0,6):
    for j in range(0,6):
        BOARD.append((i, j))

# Files Images

path = './images'
Images_List = os.listdir(path)
print(Images_List)
print(BOARD)
# Pygame
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE + 100))
pygame.display.set_caption("Test your Memory")
icon = pygame.image.load(r'./icon.png')
pygame.display.set_icon(icon)



def make_board():
    new_BOARD = []
    for i in range(0, 6):
        for j in range(0, 6):
            new_BOARD.append((i,j))
    for ii,i in enumerate(Images_List):

        random_item = random.choice(new_BOARD)

        # Making Tiles
        image_from_path = image = pygame.image.load(os.path.join('./images',i))
        image_resized = pygame.transform.scale(image_from_path,(100,100))
        x = random_item[0] * 100 + 5 * random_item[0] + 5
        y = random_item[1] * 100 + 5 * random_item[1] + 5
        rect = pygame.Rect(x,y,100,100)
        tile = Tile(random_item,rect,image_resized,False,ii)
        BOARD[BOARD.index(random_item)] = tile
        new_BOARD.remove(random_item)


        random_item = random.choice(new_BOARD)

        # Making Tiles
        image_from_path = image = pygame.image.load(os.path.join('./images',i))
        image_resized = pygame.transform.scale(image_from_path,(100,100))
        x = random_item[0] * 100 + 5 * random_item[0] +5
        y = random_item[1] * 100 + 5 * random_item[1]+5
        rect = pygame.Rect(x,y,100,100)
        tile = Tile(random_item,rect,image_resized,False,ii)
        BOARD[BOARD.index(random_item)] = tile
        new_BOARD.remove(random_item)

    print(BOARD)

def click_process(pos):
    global SELECTED_TILE_I,SELECTED_TILE_POS_I,SELECTED_TILE_F,SELECTED_TILE_POS_F,PAUSE,WON,PAIRS_CLICKED,running
    for i in BOARD:
        if i.rectangle.collidepoint(pos) ==True:
            i.hidden = False
            if SELECTED_TILE_POS_I == [] and SELECTED_TILE_POS_F==[]:
                SELECTED_TILE_POS_I = i.pos
                SELECTED_TILE_I = i
            elif SELECTED_TILE_POS_F == [] and SELECTED_TILE_POS_I !=[] and SELECTED_TILE_POS_I != i.pos:
                SELECTED_TILE_POS_F = i.pos
                SELECTED_TILE_F = i
                PAIRS_CLICKED +=1
                PAUSE = True
            elif SELECTED_TILE_POS_I != [] and SELECTED_TILE_POS_F!=[] and SELECTED_TILE_POS_I != i.pos:
                SELECTED_TILE_POS_I = i.pos
                SELECTED_TILE_I = i
                SELECTED_TILE_POS_F =[]
                SELECTED_TILE_F = None
            if PAIRS_CLICKED >= 50:
                GAME_OVER = True
                running = False
                print("Game Over")
    if SELECTED_TILE_POS_I != [] and SELECTED_TILE_POS_F !=[]:
        if SELECTED_TILE_I.id == SELECTED_TILE_F.id:
            WON = True
            PAUSE = True
            print("WON!!!!!!")
    return SELECTED_TILE_POS_I,SELECTED_TILE_POS_F

make_board()
def blit_text():
    font = pygame.font.SysFont(None, 50)
    img = font.render(f'Completed-Pairs{COMPLETED_PAIR}/18', True, (255,255,255))
    screen.blit(img, (10, 660))

    # font = pygame.font.SysFont(None, 50)
    img2 = font.render(f'Tries {PAIRS_CLICKED}/50', True, (255, 255, 255))
    screen.blit(img2, (10, 700))
running = True
while running:
    if GAMEOVER == True:
        pygame.quit()
        running = False

    clock.tick(60)
    screen.fill((255, 200, 87))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            posI,posF = click_process(event.pos)
            print(posI,posF)

    for i in BOARD:
        if i.hidden == True:
            s = pygame.Surface((100, 100))  # the size of your rect
            s.set_alpha(128)  # alpha level
            s.fill((217, 7, 24))
            screen.blit(s, i.rectangle)
        else:
            screen.blit(i.image, i.rectangle)

    blit_text()
    pygame.display.update()
    if PAUSE == True:
        if PAUSE_FIRST == True:
            pygame.time.delay(8200)
            PAUSE_FIRST = False
        elif WON == True:
            pygame.time.delay(1000)
        else:
            pygame.time.delay(700)
        for i in BOARD:
            i.hidden = True
        if WON == True:
            COMPLETED_PAIR +=1
            PAIRS_CLICKED -= 1
            BOARD.remove(SELECTED_TILE_I)
            BOARD.remove(SELECTED_TILE_F)
            if BOARD == []:
                print("You WON THE GAME!!!!!")
                pygame.quit()
            WON =False
        SELECTED_TILE_F = None
        SELECTED_TILE_I = None
        SELECTED_TILE_POS_F = []
        SELECTED_TILE_POS_I = []
        PAUSE = False
        print("COMPLETED PAIRS: ", COMPLETED_PAIR)
        print("PAIRS TRIED: ", PAIRS_CLICKED)


