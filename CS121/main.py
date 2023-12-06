import pygame, sys, os, random
from pygame .locals import *
from pygame import mixer 
from button import Button
from quizbee import quiz_data

pygame.init()
pygame.mixer.init()

WIDTH = 900
HEIGHT = 900
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyVenture Game")

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (237,26,26)
GREEN = (57,255,20)
BLUE = (41,182,246)
PINK = (228,66,255)
YELLOW = (238, 255, 65)
DARKBACK = (41, 36, 33)
SIZE_CIRCLE = 13

AVAT_WIDTH = 70
AVAT_HEIGHT = 100

SNAKE_AREA = [4, 10, 13, 20, 26, 29, 38, 46]
QUESTION_AREA = [6, 11, 18, 19, 24, 28, 32, 39, 45, 47]

avatar_position = 0
score = 0  

grid = [7, 7]
board = [100, 0, 700, 700]

dice_sound = pygame.mixer.Sound("assets/dice.mp3")
snake_sound = pygame.mixer.Sound("assets/snake.mp3")
question_sound = pygame.mixer.Sound("assets/question.mp3")
correct_sound = pygame.mixer.Sound("assets/correct.mp3")
incorrect_sound = pygame.mixer.Sound("assets/wrong_answer.mp3")
finished_sound = pygame.mixer.Sound("assets/finished.mp3")

BG = pygame.image.load("assets/mainBG.png")
PLAY_BG = pygame.image.load("assets/SNL_bg.png")
ABOUT_BG = pygame.image.load("assets/aboutBG.png")
ICON_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'PyVENTURE.png')), (300, 300))

def one():
	x,y,w,h = 705,740,100,100
	pygame.draw.rect(SCREEN, DARKBACK ,(x,y,w,h))
	pygame.draw.circle(SCREEN, GREEN,((x+(w//2)), (y+(h//2))),SIZE_CIRCLE)
 
def two():
	x,y,w,h = 705,740,100,100
	pygame.draw.rect(SCREEN, DARKBACK ,(x,y,w,h))
	pygame.draw.circle(SCREEN, YELLOW,((x+(w//4)), (y+(h//2))),SIZE_CIRCLE)
	pygame.draw.circle(SCREEN, YELLOW,((x+(3*w//4)), (y+(h//2))),SIZE_CIRCLE)

def three():
	x,y,w,h = 705,740,100,100
	pygame.draw.rect(SCREEN, DARKBACK ,(x,y,w,h))
	pygame.draw.circle(SCREEN, PINK,((x+(w//4)), (y+(3*h//4))),SIZE_CIRCLE)
	pygame.draw.circle(SCREEN, PINK,((x+(w//2)), (y+(h//2))),SIZE_CIRCLE)
	pygame.draw.circle(SCREEN, PINK,((x+(3*w//4)), (y+(h//4))),SIZE_CIRCLE)

def four():
	x,y,w,h = 705,740,100,100
	pygame.draw.rect(SCREEN, DARKBACK ,(x,y,w,h))
	pygame.draw.circle(SCREEN, BLUE,((x+(w//4)), (y+(h//4))),SIZE_CIRCLE)
	pygame.draw.circle(SCREEN, BLUE,((x+(w//4)), (y+(3*h//4))),SIZE_CIRCLE)
	pygame.draw.circle(SCREEN, BLUE,((x+(3*w//4)), (y+(h//4))),SIZE_CIRCLE)
	pygame.draw.circle(SCREEN, BLUE,((x+(3*w//4)), (y+(3*h//4))),SIZE_CIRCLE)	

def five():
	x,y,w,h = 705,740,100,100
	pygame.draw.rect(SCREEN, DARKBACK ,(x,y,w,h))
	pygame.draw.circle(SCREEN, RED,((x+(w//2)), (y+(h//2))),SIZE_CIRCLE)
	pygame.draw.circle(SCREEN, RED,((x+(w//4)), (y+(h//4))),SIZE_CIRCLE)
	pygame.draw.circle(SCREEN, RED,((x+(w//4)), (y+(3*h//4))),SIZE_CIRCLE)
	pygame.draw.circle(SCREEN, RED,((x+(3*w//4)), (y+(h//4))),SIZE_CIRCLE)
	pygame.draw.circle(SCREEN, RED,((x+(3*w//4)), (y+(3*h//4))),SIZE_CIRCLE)

def six():
	x,y,w,h = 705,740,100,100
	pygame.draw.rect(SCREEN, DARKBACK ,(x,y,w,h))
	pygame.draw.circle(SCREEN, PINK,((x+(w//4)), (y+(h//2))),SIZE_CIRCLE)
	pygame.draw.circle(SCREEN, PINK,((x+(3*w//4)), (y+(h//2))),SIZE_CIRCLE)
	pygame.draw.circle(SCREEN, PINK,((x+(w//4)), (y+(h//4))-10),SIZE_CIRCLE)
	pygame.draw.circle(SCREEN, PINK,((x+(w//4)), (y+(3*h//4))+10),SIZE_CIRCLE)
	pygame.draw.circle(SCREEN, PINK,((x+(3*w//4)), (y+(h//4))-10),SIZE_CIRCLE)
	pygame.draw.circle(SCREEN, PINK,((x+(3*w//4)), (y+(3*h//4))+10),SIZE_CIRCLE)

def drawGrid():
    n = 1  # Counter for numbers
    for y in range(grid[1]):
        for x in range(grid[0]):
            mapped_x = x if y % 2 == 0 else (grid[0] - 1 - x)  # Map x coordinate based on row number
            rect = pygame.Rect((mapped_x) * (700/grid[0]) + 100, (grid[1]-1-y) * (700/grid[1]), 700/grid[0], 700/grid[1])
            pygame.draw.rect(SCREEN, WHITE, rect, 1)
            # Create a Surface object with text drawn on it by calling the render method of the font object
            text_surface = get_font2(15).render(str(n), True, WHITE)  # 'True' means anti-aliased text. 'Black' is the color
            # Position the text in the middle of the rectangle
            text_rect = text_surface.get_rect(center=((mapped_x) * (700/grid[0]) + 100 + ((700/grid[0])/2), (grid[1]-1-y) * (700/grid[1]) + ((700/grid[1])/2)))
            SCREEN.blit(text_surface, text_rect)  # Blit the text surface onto the screen at the position of the text rectangle
            n += 1  # Increment the counter

def redrawWindow():
    SCREEN.blit(PLAY_BG, (0,0))
    pygame.draw.rect(SCREEN, WHITE, (board[0], board[1], board[2], board[3]), 2)
    drawGrid()

def display_avatar():
    avatar = pygame.transform.scale(pygame.image.load(os.path.join('assets','avatar.png')), (AVAT_WIDTH, AVAT_HEIGHT))
    
    return avatar

def display_descriptions():
    #gameInfo Caption
        gameInfo = get_font2(15).render("~ DANGER ~", 1, WHITE)
        SCREEN.blit(gameInfo,(75, 725))
        gameInfo = get_font2(11).render(" -3 steps", 1, WHITE)
        SCREEN.blit(gameInfo,(40, 795))  
        gameInfo = get_font2(11).render(" -5 steps", 1, WHITE)
        SCREEN.blit(gameInfo,(160, 795))  
        gameInfo = get_font2(15).render("~ QUIZ BEE ~", 1, WHITE)
        SCREEN.blit(gameInfo,(75, 820))
        gameInfo = get_font2(11).render("Tricky questions you", 1, WHITE)
        SCREEN.blit(gameInfo,(80, 840))
        gameInfo = get_font2(11).render("need to answer to", 1, WHITE)
        SCREEN.blit(gameInfo,(80, 858))  
        gameInfo = get_font2(11).render("earn points!", 1, WHITE)
        SCREEN.blit(gameInfo,(80, 875))  
        
        #Area Status Caption
        playCap = get_font2(15).render("~ AREA STATUS ~", 1, WHITE)
        SCREEN.blit(playCap,(370, 725))  

        #Dice Caption
        diceCap = get_font2(15).render("~ DICE ~", 1, WHITE)
        SCREEN.blit(diceCap,(720, 725))
        diceCap = get_font2(15).render("Press Spacebar", 1, WHITE)
        SCREEN.blit(diceCap,(670, 850))  
        diceCap2 = get_font2(15).render("to roll the dice!", 1, WHITE)
        SCREEN.blit(diceCap2,(660, 870))  

def display_quizbeeArea():
    gameInfo = get_font3(40).render("QUIZBEE AREA", 1, WHITE)
    SCREEN.blit(gameInfo,(340, 800))
    pygame.display.update()

def display_dangerArea1():
    gameInfo = get_font3(40).render("DANGER AREA", 1, WHITE)
    SCREEN.blit(gameInfo,(340, 800))
    gameInfo = get_font2(15).render("-3 steps back", 1, WHITE)
    SCREEN.blit(gameInfo,(390, 850))
    pygame.display.update()
    pygame.time.wait(3000)

def display_dangerArea2():
    gameInfo = get_font3(40).render("DANGER AREA", 1, WHITE)
    SCREEN.blit(gameInfo,(340, 800))
    gameInfo = get_font2(15).render("-5 steps back", 1, WHITE)
    SCREEN.blit(gameInfo,(390, 850))
    pygame.display.update()
    pygame.time.wait(3000)

def display_finishedArea():
    global score
    
    gameInfo = get_font3(40).render("PyVENTURE DONE!", 1, WHITE)
    SCREEN.blit(gameInfo,(310, 800))
    gameInfo = get_font2(20).render("CONGRATULATIONS!", 1, WHITE)
    SCREEN.blit(gameInfo,(340, 850))
    pygame.display.update()
    pygame.time.wait(5000)
   
def get_font2(size):
    return pygame.font.Font("assets/font2.ttf", size)

def get_font3(size):
    return pygame.font.Font("assets/font3.ttf", size)

def dice():
    dice_sound.play()
    roll = random.randint(1,6)
    return roll

def snakes():
    global avatar_position
    global user_position
    
    if avatar_position in SNAKE_AREA:
        snake_sound.play()
        display_dangerArea1()
        avatar_position -= 3
        
        print("="*40)
        print("[!!DANGER AREA!!] -3 steps back")
        user_position = avatar_position + 1 # for display to the user
        print(f"Your current tile position is : {user_position}")
        print()
    elif avatar_position == 34 or avatar_position == 43:
        snake_sound.play()
        display_dangerArea2()
        avatar_position -= 5
        
        print("="*40)
        print("[!!DANGER AREA!!] -5 steps back")
        user_position = avatar_position + 1 # for display to the user
        print(f"Your current tile position is : {user_position}")
        print()
        
def questions():
    global user_position
    global score
    
    if avatar_position in QUESTION_AREA:
        question_sound.play()
        display_quizbeeArea()
        
        print("="*40)
        user_position = avatar_position + 1 # for display to the user
        print(f"Your current tile position is : {user_position}")
        print("[You've landed on QUIZBEE AREA! Here is your question~~]")
        print()
        question = random.choice(quiz_data)  # Select a random question
        print(">> " + question['question'])
        print('Choices:', ', '.join(question['choices'])) # print choices
        print()
        
        user_answer = input("Your answer: ")
        if user_answer.lower() == question['answer'].lower():  # Convert both to lowercase for comparison
                correct_sound.play()
                print("CORRECT!")
                score +=1
                print("~"*3 + "You earned 1pt!"+ "~"*3)
                print()
                print(f"Total points: {score} ")
                print("Roll the dice again! :)")
        else:
            incorrect_sound.play()
            print("Sorry, that's not correct.")
            print("Roll the dice again! :)")

def About():
    SCREEN.blit(ABOUT_BG, (0,0))
    main_title = get_font3(45).render('PyVENTURE', 1, WHITE)
    SCREEN.blit(main_title, (50, 80))
    
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        PLAY_BACK = Button(image=None, pos=(850, 25), 
                            text_input="BACK", font=get_font2(25), base_color="white", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main()
        pygame.display.update()
           
def play():
    mixer.music.load("assets/gameSound.mp3")
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play(-1, 3.0) 
    print("~"*50)
    print("-"*15 +"WELCOME!" + "-"*15)
    print("~"*50)
    
    global avatar_position
    last_roll = None # new variable to store the last roll
    avatar = display_avatar()
    
    while True:
        redrawWindow()
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        display_descriptions()  

        PLAY_BACK = Button(image=None, pos=(850, 25), 
                            text_input="BACK", font=get_font2(25), base_color= WHITE, hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)
        
        x = avatar_position % grid[0]
        y = avatar_position // grid[1]

        if y % 2 != 0:  # If it is an odd row, reverse the direction of X
            x = grid[0] - 1 - x
        SCREEN.blit(avatar, (x * (700 / grid[0]) + 110, (grid[1] - 1 - y) * (700 / grid[1])))  # draw avatar at newly calculated position
        
        # if last_roll is set, draw the appropriate dice face
        if last_roll:
            if last_roll == 1: one()
            elif last_roll == 2: two()
            elif last_roll == 3: three()
            elif last_roll == 4: four()
            elif last_roll == 5: five()
            elif last_roll == 6: six()   
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                        main()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                time = random.randint(5,25)
                for i in range(time):
                    d_no = dice()
                    last_roll = d_no # store the last roll
                    if d_no == 1:
                        one()
                    elif d_no == 2:
                        two()
                    elif d_no == 3:
                        three()
                    elif d_no == 4:
                        four()
                    elif d_no == 5:
                        five()
                    elif d_no == 6:
                        six()      
                    pygame.time.wait(100)
                    pygame.display.update()
                if avatar_position < 48:
                    dice_roll = d_no  # roll the dice
                    avatar_position += dice_roll  # move avatar forward
                    avatar_position = min(avatar_position, 48)  # ensure avatar does not exceed position 48
                    print("="*30)
                    print(f"The roll dice is {dice_roll}")
                    user_position = avatar_position + 1 # for display to the user
                    print(f"Your current tile position is : {user_position}")
                    print()
                    questions()
                    if avatar_position == 48:
                        display_finishedArea()
                        finished_sound.play()
                        print("="*40)
                        print("~"*5 + " CONGRATULATIONS! " + "~"*5)
                        print(f"Total points: {score} ")
                        print("~"*5 + " YOU FINISHED THE PyVENTURE! " + "~"*5)
                        print("~"*10 + "  HAPPY AREA!  " + "~"*10)
                        print()
                else:
                     finished_sound.play()
                     print("The game has ended.")
                     
            snakes()
        pygame.display.update()
                   
def main():
    mixer.music.load("assets/bgMusic.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    
    while True:
        SCREEN.blit(BG, (0, 0))
        SCREEN.blit(ICON_IMAGE, (300, 100))
        main_title = get_font3(85).render('PyVENTURE', 1, WHITE)
        SCREEN.blit(main_title, (250, 420))
        
        gameSlogan = get_font2(30).render("Roll, Step, and CONQUER!", True, WHITE)
        SCREEN.blit(gameSlogan,(220, 500))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(455, 600), 
                            text_input="PLAY", font=get_font2(50), base_color= BLACK, hovering_color="#0000FF")
        
        INFO_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(455, 700), 
                            text_input="ABOUT", font=get_font2(45), base_color= BLACK, hovering_color="#0000FF")
        
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(455, 800), 
                            text_input="QUIT", font=get_font2(45), base_color= BLACK, hovering_color="#0000FF")

        for button in [PLAY_BUTTON, INFO_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if INFO_BUTTON.checkForInput(MENU_MOUSE_POS):
                    About()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
main()