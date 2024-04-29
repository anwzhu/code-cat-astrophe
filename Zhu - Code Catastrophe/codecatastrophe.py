import pygame
import sys
import random

pygame.init()
pygame.key.set_repeat(500, 18)

width = 800
height = 600

display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Code Catastrophe')
text_font = pygame.font.SysFont(None, 60)
text_font2 = pygame.font.SysFont(None, 100)
text_font3 = pygame.font.SysFont(None, 25)
end_font = pygame.font.SysFont(None, 100)
clock = pygame.time.Clock()

count, time = 10, '10'.rjust(3)
pygame.time.set_timer(pygame.USEREVENT, 1000)

base_font = pygame.font.Font(None, 55)
user_rect = pygame.Rect(width/18, 7*height/9, 100, 40)
color_act = pygame.Color('aliceblue')
color_pas = pygame.Color('whitesmoke')
color = color_pas
active = False

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    display.blit(img, (x, y))

lvl1 = open("levels/lvl1.csv", 'r')
rows1 = lvl1.readlines()
L1 = []
for i in rows1:
    seq = i.strip()
    L1.append(seq)
lvl2 = open("levels/lvl2.csv", 'r')
rows2 = lvl2.readlines()
L2 = []
for i in rows2:
    seq = i.strip()
    L2.append(seq)

allwords = open("newall.txt", 'r')
allw = allwords.readlines()
AW = []
for i in allw:
    word = i.strip()
    AW.append(word)

used = []
guess = ""
score = 0
turn = 0

choose_prompt2 = False
choose_prompt1 = True

gameover= False
running = True
while running:
    
    display.fill((255, 255, 255))

    if choose_prompt1:
        prompt = random.choice(L1)
        choose_prompt1 = False
    draw_text(prompt, text_font2, (100, 100, 100), 42*width/96, 2*height/5)
    
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:
            count -= 1
            if count > 0:
                time = str(count).rjust(3)
            else:
                time = '  0'
                gameover = True
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if user_rect.collidepoint(event.pos):
                active = True
            else:
                active = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if prompt in guess and guess.lower() in AW and guess.lower() not in used:
                    score += len(guess)
                    used.append(guess.lower())
                    guess = ""
                    turn += 1
                    if turn < 5:
                        prompt = random.choice(L1)
                        count = 11
                    elif turn >= 5 and turn < 10:
                        prompt = random.choice(L1)
                        count = 9
                    elif turn >= 10 and turn < 15:
                        prompt = random.choice(L2)
                        count = 7
                    else:
                        prompt = random.choice(L2)
                        count = 5
                else:
                    draw_text(prompt, text_font2, (200, 0, 0), 42*width/96, 2*height/5)
            elif event.key == pygame.K_BACKSPACE:
                if len(guess) > 0:
                    guess = guess[:-1]
            else:
                guess += event.unicode.lower()

    if active:
        color = color_act
    else:
        color = color_pas

    display.blit(text_font.render(time, True, (0, 0, 0)), (11*width/24, 48))
    draw_text("Score: " + str(score), text_font3, (0, 0, 0), 32, 30)

    pygame.draw.rect(display, color, user_rect)
    surface = base_font.render(guess, True, (70, 130, 180))
    display.blit(surface, (width/18, 7*height/9))
    user_rect.w = max(700, surface.get_width()+10)

    if gameover:
        end_rect = pygame.Rect(0, 0, 1000, 750)
        pygame.draw.rect(display, (200, 0, 0), end_rect)
        draw_text("GAME OVER", end_font, (250, 250, 250), 2*width/9, 7*height/15)
        draw_text("You scored " + str(score) + " points", text_font3, (250, 250, 250), 6*width/11, 3*height/5)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
