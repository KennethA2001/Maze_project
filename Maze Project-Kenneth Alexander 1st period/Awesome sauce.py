
# Imports
import pygame
import intersects

# Initialize game engine
pygame.init()


# Window
WIDTH = 800
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)
TITLE = "The koolest maze"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60

# Sounds
wah = pygame.mixer.Sound("cooper.ogg")
pygame.mixer.music.load("asmr.ogg")
splash = pygame.image.load("splash.jpg")

pygame.mixer.music.play(-1)

 #Fonts
MY_FONT = pygame.font.Font(None, 50)

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)


def setup():
    global block, vel1, block_speed, score1, ticks, stage, time_remaining, coins, walls, win
    
    block =  [200, 150, 25, 25]
    vel1 = [0, 0]
    block_speed = 5
    score1 = 0

    stage = START
    time_remaining = 10
    ticks = 0

    # make walls
    wall1 =  [300, 275, 200, 25]
    wall2 =  [400, 450, 200, 25]
    wall3 =  [100, 100, 25, 200]
    wall4 =  [350, 200, 200, 25]
    wall5 =  [250, 300, 25, 200]
    wall6 =  [600, 200, 200, 25]
    wall7 =  [75, 500, 200, 25]
    wall8 =  [700, 550, 200, 25]
    
  
    walls = [wall1, wall2, wall3, wall4, wall5, wall6, wall7, wall8]

    # Make coins
    coin1 = [300, 500, 25, 25]
    coin2 = [100, 450, 25, 25]
    coin3 = [300, 150, 25, 25]
    coin4 = [100, 550, 25, 25]
    coin5 = [700, 525, 25, 25]

    coins = [coin1, coin2, coin3, coin4, coin5]

    win = False
# stages
START = 0
PLAYING = 1
END = 2

# Game loop
setup()
win = False
done = False

while not done:
      # Event processing (React to key presses, mouse clicks, etc.)
    ''' for now, we'll just check to see if the X is clicked '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
        elif event.type == pygame.KEYDOWN:
            
            if stage == START:
                screen.blit(splash, [0,0])
                if event.key == pygame.K_SPACE:
                    stage = PLAYING
                    
            elif stage == PLAYING:
                if event.key == pygame.K_LEFT:
                    vel1[0] -= 2
                elif event.key == pygame.K_RIGHT:
                    vel1[0] += 2
                elif event.key == pygame.K_UP:
                    vel1[1] -= 2
                elif event.key == pygame.K_DOWN:
                    vel1[1] += 2
                    
            elif stage == END:
                if event.key == pygame.K_SPACE:
                    setup()

        
        
    # Game logic (Check for collisions, update points, etc.)
    ''' move the player in horizontal direction '''
    block[0] += vel1[0]

    ''' timer stuff '''
    if stage == PLAYING:
        ticks += 1

        if ticks % refresh_rate == 0:
            time_remaining -= 1

    if time_remaining == 0:
        stage = END

    ''' get block edges (makes collision resolution easier to read) '''
    left = block[0]
    right = block[0] + block[2]
    top = block[1]
    bottom = block[1] +block[3]

    ''' resolve collisions horizontally '''
    for w in walls:
        if intersects.rect_rect(block, w):        
            if vel1[0] > 0:
                block[0] = w[0] - block[2]
            elif vel1[0] < 0:
                block[0] = w[0] + w[2]

    ''' move the player in vertical direction '''
    block[1] += vel1[1]
    
    ''' resolve collisions vertically '''
    for w in walls:
        if intersects.rect_rect(block, w):                    
            if vel1[1] > 0:
                block[1] = w[1] - block[3]
            if vel1[1]< 0:
                block[1] = w[1] + w[3]




    ''' here is where you should resolve player collisions with screen edges '''
    if left < 0:
        block[0] = 0
        stage = END
    elif right > WIDTH:
        block[0] = WIDTH - block[2]
        stage = END

    if top < 0:
        block[1] = 0
        stage = END
    elif bottom > HEIGHT:
        block[1] = HEIGHT - block[3]
        stage = END




    ''' get the coins '''
    hit_list = []

    for c in coins:
        if intersects.rect_rect(block, c):
            hit_list.append(c)
     
    hit_list = [c for c in coins if intersects.rect_rect(block, c)]
    
    for hit in hit_list:
        coins.remove(hit)
        score1 += 1
        wah.play()
        
        
    if len(coins) == 0:
        win = True

        
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.fill(BLACK)
 
    pygame.draw.rect(screen, WHITE, block)
    
    for w in walls:
        pygame.draw.rect(screen, RED, w)

    for c in coins:
        pygame.draw.rect(screen, YELLOW, c)
        
    if win:
        font = pygame.font.Font(None, 48)
        text = font.render("You Win!", 1, GREEN)
        screen.blit(text, [400, 200])

    ''' timer text '''
    timer_text = MY_FONT.render(str(time_remaining), True, WHITE)
    screen.blit(timer_text, [50, 50])

    ''' begin/end game text '''
    if stage == START:
        splash = pygame.image.load("splash.jpg")
        screen.blit(splash, [0, 0])
        text1 = MY_FONT.render("Block", True, WHITE)
        text2 = MY_FONT.render("(Press SPACE to play.)", True, WHITE)
        screen.blit(text1, [350, 150])
        screen.blit(text2, [225, 200])
    elif stage == END:
        text1 = MY_FONT.render("Game Over", True, WHITE)
        text2 = MY_FONT.render("(Press SPACE to restart.)", True, WHITE)
        screen.blit(text1, [310, 150])
        screen.blit(text2, [210, 200])


    
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
