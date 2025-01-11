import pygame
import pygame.locals
import random

image_path = '' #/data/data/org.test.klaxxongame/files/app/

clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Klaxxon Game") #название игры 
icon = pygame.image.load(image_path+'image/icon.png').convert_alpha()
pygame.display.set_icon(icon) #иконка


# square = pygame.Surface((50, 170))
# square.fill('Blue')

# myfont = pygame.font.Font('Righteous/Righteous-Regular.ttf', 40)
# text_surface = myfont.render('Klaxxon', True, (252, 252, 252))

bg = pygame.image.load(image_path+'image/background.jpg').convert_alpha()
ghost = pygame.image.load(image_path+'image/ghost.png').convert_alpha()
ghost = pygame.transform.smoothscale(ghost, (77, 77))

ghost_list_in_game = []

down1 = pygame.image.load(image_path+'Sprite\down\image_0-0.png').convert_alpha()
down1 = pygame.transform.smoothscale(down1, (88, 88))
down2 = pygame.image.load(image_path+'Sprite\down\image_0-1.png').convert_alpha()
down2 = pygame.transform.smoothscale(down1, (88, 88))
down3 = pygame.image.load(image_path+'Sprite\down\image_0-2.png').convert_alpha()
down3 = pygame.transform.smoothscale(down1, (88, 88))
down4 = pygame.image.load(image_path+'Sprite\down\image_0-3.png').convert_alpha()
down4= pygame.transform.smoothscale(down1, (88, 88))

walk_down = [
    pygame.transform.smoothscale(pygame.image.load(image_path+'Sprite\down\image_0-0.png').convert_alpha(), (88,88)),
    pygame.transform.smoothscale(pygame.image.load(image_path+'Sprite\down\image_0-1.png').convert_alpha(), (88,88)),
    pygame.transform.smoothscale(pygame.image.load(image_path+'Sprite\down\image_0-2.png').convert_alpha(), (88,88)),
    pygame.transform.smoothscale(pygame.image.load(image_path+'Sprite\down\image_0-3.png').convert_alpha(), (88,88)),
]

walk_right = [
    pygame.transform.smoothscale(pygame.image.load(image_path+'Sprite\Right\image_2-0.png').convert_alpha(), (88,88)),
    pygame.transform.smoothscale(pygame.image.load(image_path+'Sprite\Right\image_2-1.png').convert_alpha(), (88,88)),
    pygame.transform.smoothscale(pygame.image.load(image_path+'Sprite\Right\image_2-2.png').convert_alpha(), (88,88)),
    pygame.transform.smoothscale(pygame.image.load(image_path+'Sprite\Right\image_2-3.png').convert_alpha(), (88,88)),
]

walk_left = [
    pygame.transform.smoothscale(pygame.image.load(image_path+'Sprite\left\image_1-0.png').convert_alpha(), (88,88)),
    pygame.transform.smoothscale(pygame.image.load(image_path+'Sprite\left\image_1-1.png').convert_alpha(), (88,88)),
    pygame.transform.smoothscale(pygame.image.load(image_path+'Sprite\left\image_1-2.png').convert_alpha(), (88,88)),
    pygame.transform.smoothscale(pygame.image.load(image_path+'Sprite\left\image_1-3.png').convert_alpha(), (88,88)),
   
]

walk_up = [
    pygame.transform.smoothscale(pygame.image.load(image_path+'Sprite/up\image_3-0.png').convert_alpha(), (88,88)),
    pygame.transform.smoothscale(pygame.image.load(image_path+'Sprite/up\image_3-1.png').convert_alpha(), (88,88)),
    pygame.transform.smoothscale(pygame.image.load(image_path+'Sprite/up\image_3-2.png').convert_alpha(), (88,88)),
    pygame.transform.smoothscale(pygame.image.load(image_path+'Sprite/up\image_3-3.png').convert_alpha(), (88,88)), 
] 

player_anim_count = 0
bg_x = 0

gameplay = True

label = pygame.font.Font('Righteous\Righteous-Regular.ttf', 60)
lose_label = label.render('You lose!', True, (193, 196, 199))
restart_label = label.render('Play again', True, (115, 132, 148))

restart_label_react = restart_label.get_rect(topleft=(360,300))

bullet = pygame.transform.smoothscale(pygame.image.load(image_path+'image/bullet.png'), (88,88))
bullets = []

player_speed = 20
player_jump = 8
is_jump = False
player_x = 150
player_y = 530
bg_sound = pygame.mixer.Sound(image_path+'music.mp3')
bg_sound.set_volume(1)
bg_sound.play(loops=-1)


running = True
while running:
    if gameplay == True:
        ghost_timer = pygame.USEREVENT +1 
        pygame.time.set_timer(ghost_timer, random.randint(1500, 2500))
        screen.blit(bg, (bg_x, 0))
        screen.blit(bg, (bg_x + 700, 0))

        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))
        
        if ghost_list_in_game:
            for (i, el) in enumerate(ghost_list_in_game):
                screen.blit(ghost, el)
                el.x -= 10
                for ghost_rect in ghost_list_in_game: # Iterate through all ghost rectangles
                    pygame.draw.rect(screen, (255, 0, 0), ghost_rect) # Red rectangle

                if el.x < -10:
                    ghost_list_in_game.pop(i)
                
                if player_rect.colliderect(el):
                    gameplay = False

        keys = pygame.key.get_pressed()
        
        # Обработка движения и отображение анимации
        if keys[pygame.K_d]:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))
        elif keys[pygame.K_a]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_down[0], (player_x, player_y - 15))

        if keys[pygame.K_LEFT] or (keys[pygame.K_a] and player_x > 50):
            player_x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x += player_speed


        # Логика прыжка
        if not is_jump:
            if keys[pygame.K_SPACE] or keys[pygame.K_w]:
                is_jump = True
                player_jump = 8  # Сброс высоты прыжка при начале прыжка
        else:
            if player_jump >= -8:
                if player_jump > 0:
                    player_y -= (player_jump ** 2) / 2
                else:
                    player_y += (player_jump ** 2) / 2
                player_jump -= 1
            else:
                is_jump = False
                player_jump = 8  # Сброс высоты прыжка после завершения

        # Обновление анимации
        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        bg_x -= 10
        if bg_x <= -618:
            bg_x = 0

        if keys[pygame.K_k]:
            bullets.append(bullet.get_rect(topleft = (player_x+30, player_y-5))) 

        if bullets:
            for el in bullets:
                screen.blit(bullet, (el.x, el.y))
                el.x+=25

    else:
        screen.fill((87,88,89))
        screen.blit(lose_label, (400, 200))
        screen.blit(restart_label, restart_label_react)
        bg_sound.set_volume(0)

        mouse = pygame.mouse.get_pos()
        if restart_label_react.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
 
            ghost_list_in_game.clear()

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == ghost_timer:
            rect = ghost.get_rect(topleft=(1020, 530))
            ghost_list_in_game.append(rect) 


    # Установка частоты кадров
    if is_jump:
        clock.tick(20)  # Быстрая частота для прыжка
    else:
        clock.tick(7)  # Медленная частота для обычной анимации

pygame.quit()
