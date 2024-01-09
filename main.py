import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH,HEIGHT=900,500
WIN=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("First Game")
BLUE=(0,0,255)
BLACK=(0,0,0)
RED=(255,0,0)
WHITE=(255,255,255)
YELLOW=(255,255,0)
FPS=60
VEL=5
BULLET_VEL=7
MAX_BULLETS=3
BORDER=pygame.Rect(WIDTH//2-5,0,10,HEIGHT)

BULLET_HIT_SOUND=pygame.mixer.Sound(os.path.join('Assets','Grenade+1.mp3'))
BULLET_SHOOT_SOUND=pygame.mixer.Sound(os.path.join('Assets','Gun+Silencer.mp3'))

HEALTH_FONT=pygame.font.SysFont('comicsans',40)
WINNER_FONT=pygame.font.SysFont('comicsans',100)

YELLOW_HIT=pygame.USEREVENT+1
RED_HIT=pygame.USEREVENT+2

SPACESHIP_WIDTH,SPACESHIP_HEIGHT=55,40
YELLOW_SPACESHIP_IMG=pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))
YELLOW_SPACESHIP=pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMG,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),90)
RED_SPACESHIP_IMG=pygame.image.load(os.path.join('Assets','spaceship_red.png'))
RED_SPACESHIP=pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMG,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),270)
BACKGROUND=pygame.image.load(os.path.join('Assets','back.jpg'))
BACK=pygame.transform.scale(BACKGROUND,(WIDTH,HEIGHT))
def draw_winner(text):
    draw_text=WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text,(WIDTH/2-draw_text.get_width()/2,HEIGHT/2-draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def draw_window(red,yellow,yellow_bullets,red_bullets,red_health,yellow_health):
    WIN.blit(BACK,(0,0))
    red_health_text=HEALTH_FONT.render("Health: "+str(red_health),1,WHITE)
    yellow_health_text=HEALTH_FONT.render("Health: "+str(yellow_health),1,WHITE)
    WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
    WIN.blit(RED_SPACESHIP,(red.x,red.y))
    WIN.blit(yellow_health_text,(WIDTH-yellow_health_text.get_width()-10,10))
    WIN.blit(red_health_text,(10,10))
    pygame.draw.rect(WIN,BLACK,BORDER)

    for bullet in red_bullets:
        pygame.draw.rect(WIN,RED,bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN,YELLOW,bullet)
    pygame.display.update()
def yellow_movement(keys_pressed,yellow):
    if keys_pressed[pygame.K_a] and yellow.x-VEL>BORDER.x+BORDER.width:
            yellow.x-=VEL
    if keys_pressed[pygame.K_d] and yellow.x+yellow.width-VEL<WIDTH:
            yellow.x+=VEL
    if keys_pressed[pygame.K_w] and yellow.y>=0:
            yellow.y-=VEL
    if keys_pressed[pygame.K_s] and yellow.y+VEL+yellow.height<HEIGHT:
            yellow.y+=VEL
def red_movement(keys_pressed,red):
    if keys_pressed[pygame.K_LEFT] and red.x>=0:
            red.x-=VEL
    if keys_pressed[pygame.K_RIGHT] and red.x+VEL+red.width<BORDER.x:
            red.x+=VEL
    if keys_pressed[pygame.K_UP] and red.y>=0:
            red.y-=VEL
    if keys_pressed[pygame.K_DOWN] and red.y+VEL+red.height<HEIGHT:
            red.y+=VEL
def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    for bullet in yellow_bullets:
        bullet.x-=BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif (bullet.x<0):
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x+=BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x>WIDTH:
            red_bullets.remove(bullet)

   


def main():
    red=pygame.Rect(100,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    yellow=pygame.Rect(700,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    yellow_bullets=[]
    red_bullets=[]
    red_health=10
    yellow_health=10

    clock=pygame.time.Clock()

    run=True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_q and len(yellow_bullets)<MAX_BULLETS:
                    bullet=pygame.Rect(yellow.x,yellow.y+yellow.height//2,10,5)
                    yellow_bullets.append(bullet)
                    BULLET_SHOOT_SOUND.play()
                
                
                if event.key==pygame.K_y and  len(red_bullets)<MAX_BULLETS:
                   bullet=pygame.Rect(red.x+red.width,red.y+red.height//2,10,5)
                   red_bullets.append(bullet)
                   BULLET_SHOOT_SOUND.play()

            if event.type==RED_HIT:
                red_health-=1
                BULLET_HIT_SOUND.play()

            if event.type==YELLOW_HIT:
                yellow_health-=1
                BULLET_HIT_SOUND.play()
        winner_text=""
        if red_health<=0:
            winner_text="YELLOW WINS"
        if yellow_health<=0:
            winner_text="RED WINS"
        if winner_text!="":
            draw_winner(winner_text)



        keys_pressed=pygame.key.get_pressed()
        yellow_movement(keys_pressed,yellow)
        red_movement(keys_pressed,red)
        handle_bullets(yellow_bullets,red_bullets,yellow,red)
        
        draw_window(red,yellow,yellow_bullets,red_bullets,red_health,yellow_health)
    
    

if __name__=="__main__":
    main()

