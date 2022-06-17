import pygame
import random

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load('images/player_walk1.png').convert_alpha()
        player_walk2 = pygame.image.load('images/player_walk2.png').convert_alpha()
        self.player_walk = [player_walk1, player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load('images/player_jump.png')
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('images/images_audio_jump.mp3')
        self.jump_sound.set_volume(0.2)

    def user_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    def update(self):
        self.user_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            fly_1 = pygame.image.load('images/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('images/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('images/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('images/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (random.randint(900, 1100), y_pos))
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


pygame.init()
DIFFICULTY = 1400
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800,400))
bg = pygame.image.load('images/Sky.png')
bg_music = pygame.mixer.Sound('images/music.wav')
bg_music.set_volume(0.2)
bg_music.play(loops = -1)
ground = pygame.image.load('images/ground.png')
font = pygame.font.Font('images/Pixeltype.ttf', 50) #(style, size)
text_surface = font.render('My game', False, 'Green') #(text, AA, color)
text_rect = text_surface.get_rect(center = ((400, 50)))

player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()


# Times
start_time = 0
score = 0
obstacle_timer = pygame.USEREVENT + 1 # +1 means avoid other pygame events
pygame.time.set_timer(obstacle_timer, DIFFICULTY) # new enemy spawn every __ ms

snail_animation_timer = pygame.USEREVENT+2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT+3
pygame.time.set_timer(fly_animation_timer, 200)

# obstacles
# snail
snail_frame1 = pygame.image.load('images/snail1.png').convert_alpha()
snail_frame2 = pygame.image.load('images/snail2.png').convert_alpha()
snail_frames = [snail_frame1, snail_frame2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]
# fly
fly_frame_1 = pygame.image.load('images/fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('images/fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []

#player
player_walk1 = pygame.image.load('images/player_walk1.png').convert_alpha()
player_walk2 = pygame.image.load('images/player_walk2.png').convert_alpha()
player_walk = [player_walk1, player_walk2]
player_index = 0
player_jump = pygame.image.load('images/player_jump.png')
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80,300)) #300 is the same y as ground, so this places character on ground
gravity = 0

# intro screen
player_stand = pygame.image.load('images/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2) # rotozoom(x, flip x 90 degrees, scale 2 times)
player_stand_rect = player_stand.get_rect(center = (400, 200))
intro = font.render('Pixel Runner', False, (111, 196, 169))
intro_rect = intro.get_rect(center = (400, 80))
instructions = font.render('Press space to run', False, (111, 196, 169))
instructions_rect = instructions.get_rect(center = (400, 320))

def display_score():
    curr_time = int(pygame.time.get_ticks()/1000)-start_time # change ms to seconds by /1000
    score_surf = font.render(f'{curr_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center = (400, 100))
    screen.blit(score_surf, score_rect)
    return curr_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 10
            # check y for snail or fly
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def player_animation():
    global player_surf, player_index
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]

game = False
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if game:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300: # only allow a jump if character is on ground
                    gravity = -20
        else: # if game is over, reset snail position on space click
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game = True
                start_time = int(pygame.time.get_ticks()/1000) # reset timer on game over
        if game:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(random.choice(['fly', 'snail', 'fly', 'snail']))) # 50% each
                # if random.randint(0, 1):
                #     obstacle_rect_list.append(snail_surface.get_rect(bottomright = (random.randint(900, 1100), 300)))
                # else:
                #     obstacle_rect_list.append(fly_surf.get_rect(bottomright = (random.randint(900, 1100), 210)))

            #snail animation
            if event.type == snail_animation_timer:
                if snail_frame_index == 0: snail_frame_index = 1
                else: snail_frame_index = 0
                snail_surface = snail_frames[snail_frame_index]

            #fly animation
            if event.type == fly_animation_timer:
                if fly_frame_index == 0: fly_frame_index = 1
                else: fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]

    if game: # game state management, once collision, stop game and to go else
        screen.blit(bg, (0,0))
        screen.blit(ground, (0,300))
        score = display_score()
        screen.blit(text_surface, (text_rect))
        # obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        #player
        # gravity += 1
        # player_rect.y += gravity
        # if player_rect.bottom > 300: player_rect.bottom = 300
        # player_animation()
        # screen.blit(player_surf, (player_rect))
        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()

        #collision
        game = collision_sprite()
        # game = collisions(player_rect, obstacle_rect_list)
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear() #clear array

        # balances counterplay vs fly hitbox
        player_rect.midbottom = (80, 300)
        gravity = 0

        score_message = font.render(f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center = (400, 330))
        screen.blit(intro, intro_rect)
        if score == 0: screen.blit(instructions, instructions_rect)
        else: screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)