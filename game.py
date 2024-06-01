import pygame
import random
import time





pygame.init()
width = 1200
height = 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Catch The Ghosts!")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = [pygame.image.load("IMG/pacman-open-right.png"),pygame.image.load("IMG/pacman-closed-right.png")] 
        self.current_image_index = 0
        self.image = self.images[self.current_image_index]
        self.rect = self.image.get_rect()
        self.rect.center = (width//2, height - 50)

        self.lives = 5
        self.enter_safezone = 2
        self.speed = 8

        self.catch_sound = pygame.mixer.Sound("sounds/pacman_eatghost.wav")
        self.catch_sound.set_volume(0.1)
        self.wrong_sound = pygame.mixer.Sound("sounds/pacman_wrong.mp3")
        self.wrong_sound.set_volume(0.1)

        self.last_image_change_time = 0
        self.image_change_interval = 0.5
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.top > 109:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < height - 109:
            self.rect.y += self.speed
        if keys[pygame.K_a] and self.rect.left > 10:
            self.images = [pygame.image.load("IMG/pacman-open-left.png"),pygame.image.load("IMG/pacman-closed-left.png")]
            self.image = self.images[self.current_image_index]
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < width:
            self.images = [pygame.image.load("IMG/pacman-open-right.png"),pygame.image.load("IMG/pacman-closed-right.png")] 
            self.image = self.images[self.current_image_index]
            self.rect.x += self.speed
        current_time = time.time()


        if (current_time - self.last_image_change_time >= self.image_change_interval):
            self.current_image_index = (self.current_image_index + 1) % len(self.images)
            self.image = self.images[self.current_image_index]
            self.last_image_change_time = current_time

    def back_to_safe_zone(self):
        if self.enter_safezone > 0:
            self.enter_safezone -= 1
            self.rect.center = (width//2, height - 50)

    def reset(self):
        self.rect.center = (width//2, height - 50)


player_group = pygame.sprite.Group()
one_player = Player()
player_group.add(one_player)

class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, image, ghost_type):
        super().__init__()
        self.original_image = image
        self.original_type = ghost_type 
        self.image = image 
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        self.type = ghost_type
        self.speed = random.randint(1, 5)
        self.x = random.choice([-1, 1])
        self.y = random.choice([-1, 1])
    def update(self):
        
        if my_game.bonus_activated:
            my_game.wanted_ghost = my_game.blue_image
            self.image = my_game.blue_image
        else:
            self.image = self.original_image
            self.type = self.original_type
        self.rect.x += self.x * self.speed
        self.rect.y += self.y * self.speed
        
        if self.rect.left <= 0 or self.rect.right >= width:
            self.x *= -1
        if self.rect.top <= 100 or self.rect.bottom >= height - 100:
            self.y *= -1  
class Bonus(Ghost):
    def __init__(self, x, y):
        bonus_image = pygame.image.load("IMG/bonus.png")
        super().__init__(x, y, bonus_image, -1)
        self.speed = random.randint(1, 5)
        
    def update(self):
        super().update()
                  
class Game:
    def __init__(self, our_player, group_of_ghosts, bonus_group):
        self.our_player = our_player
        self.bonus_activated = False 
        self.bonus_activated_time = 0
        self.group_of_bonuses = bonus_group
        self.group_of_ghosts = group_of_ghosts
        self.score = 0
        self.highest_score = 0
        self.round_number = 0

        self.round_time = 0
        self.slowdown_cycle = 0

        pygame.mixer.music.load("sounds/pacman_beginning.wav")
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play(-1)

        self.bg_image = pygame.image.load("IMG/background.png")
        self.bg_rect = self.bg_image.get_rect()
        self.bg_rect.topleft = (0, 0)

        self.ghost_font = pygame.font.Font("font/pacman_font.otf", 22)

        self.blue_image = pygame.image.load("IMG/blue-ghost.png")
        cyan_image = pygame.image.load("IMG/cyan-ghost.png")
        pink_image = pygame.image.load("IMG/pink-ghost.png")
        red_image = pygame.image.load("IMG/red-ghost.png")
        orange_image = pygame.image.load("IMG/orange-ghost.png")
        self.ghost_images = [red_image, cyan_image, pink_image, orange_image]

        self.wanted_ghost_number = random.randint(0, 3)
        self.wanted_ghost = self.ghost_images[self.wanted_ghost_number]

        self.wanted_ghost_rect = self.wanted_ghost.get_rect()
        self.wanted_ghost_rect.centerx = width//2
        self.wanted_ghost_rect.top = 30
    def update(self):
        self.slowdown_cycle += 1
        if self.slowdown_cycle == fps:
            self.round_time += 1
            self.slowdown_cycle = 0
        
            
        self.check_colissions()
    def draw(self):
        red = (255,0,0)
        pink = (195, 23, 189)
        orange = (207, 128, 50)
        cyan = (0,255,255)
        colors = [red, cyan, pink, orange]

        catch_text = self.ghost_font.render("TARGET:", True, "green")
        catch_text_rect = catch_text.get_rect()
        catch_text_rect.centerx = width//2
        catch_text_rect.top = 5 

        score_text = self.ghost_font.render(f"SCORE: {self.score}", True, "green")
        score_text_rect = score_text.get_rect()
        score_text_rect.topleft = (10,4)

        lives_text = self.ghost_font.render(f"LIVES: {self.our_player.lives}", True, "green")
        lives_text_rect = lives_text.get_rect()
        lives_text_rect.topleft = (10, 30)

        round_text = self.ghost_font.render(f"ROUND: {self.round_number}", True, "green")
        round_text_rect = round_text.get_rect()
        round_text_rect.topleft = (10, 60)

        time_text = self.ghost_font.render(f"ROUND TIME: {self.round_time}", True, "green")
        time_text_rect = time_text.get_rect()
        time_text_rect.topright = (width - 5, 5)

        back_safe_zone_text = self.ghost_font.render(f"SAFE ZONE: {self.our_player.enter_safezone}", True, "green")
        back_safe_zone_text_rect = back_safe_zone_text.get_rect()
        back_safe_zone_text_rect.topright = (width - 5, 35)
        
        screen.blit(catch_text, catch_text_rect)
        screen.blit(self.wanted_ghost, self.wanted_ghost_rect)
        screen.blit(score_text, score_text_rect)
        screen.blit(lives_text , lives_text_rect)
        screen.blit(round_text, round_text_rect)
        screen.blit(time_text, time_text_rect)
        screen.blit(back_safe_zone_text, back_safe_zone_text_rect)

        pygame.draw.rect(screen, colors[self.wanted_ghost_number], (0, 100, width, height - 200), 4)
    def check_colissions(self):
        collided_ghost = pygame.sprite.spritecollideany(self.our_player, self.group_of_ghosts)
        collided_bonus = pygame.sprite.spritecollideany(self.our_player, self.group_of_bonuses)
        if collided_ghost:
            if self.bonus_activated:
                self.score += 10 * self.round_number
                collided_ghost.remove(self.group_of_ghosts)
                self.our_player.catch_sound.play()
                if self.group_of_ghosts == False:
                    self.our_player.reset()
                    self.start_new_round()
            elif collided_ghost.type == self.wanted_ghost_number: 
                self.score += 10 * self.round_number
                collided_ghost.remove(self.group_of_ghosts)  
                self.our_player.catch_sound.play()
                if self.group_of_ghosts:
                    self.choose_new_target()
                else:
                    self.our_player.reset()
                    self.start_new_round()

            else:
                self.our_player.wrong_sound.play()
                self.our_player.lives -= 1

                if self.our_player.lives <= 0:
                    pygame.mixer.music.stop()
                    death_sound = pygame.mixer.Sound("sounds/pacman_death.wav")
                    death_sound.set_volume(0.1)
                    death_sound.play()
                    if self.score > self.highest_score:
                        self.highest_score = self.score
                    
                    self.pause(f"YOUR SCORE: {self.score}.", f"HIGHEST SCORE: {self.highest_score}.","PRESS ENTER IF YOU WANT TO PLAY AGAIN.")
                    self.reset_game()
                self.our_player.reset() 
                
        if collided_bonus:
            eat_fruit = pygame.mixer.Sound("sounds/pacman_eatfruit.wav")
            eat_fruit.set_volume(0.1)
            eat_fruit.play()
            collided_bonus.remove(self.group_of_bonuses)
            self.bonus_activated = True
            self.bonus_activated_time = pygame.time.get_ticks()
    def cancel_bonus(self, time):
        if time - self.bonus_activated_time >= 0:
            bonus_text_create = self.ghost_font.render("BONUS: 3", True, "green")
        if time - self.bonus_activated_time >= 1000:
            bonus_text_create = self.ghost_font.render("BONUS: 2", True, "green")
        if time - self.bonus_activated_time >= 2000:
            bonus_text_create = self.ghost_font.render("BONUS: 1", True, "green")
        if time - self.bonus_activated_time >= 3000:
            self.choose_new_target()
            self.draw()
            self.bonus_activated = False
            
        bonus_text_create_rect = bonus_text_create.get_rect()
        bonus_text_create_rect.center = (width//2, height//2)
        screen.blit(bonus_text_create, bonus_text_create_rect)
        
    def start_new_round(self):
        
        self.score += int(100 * (self.round_number / (1 + self.round_time)))
        self.bonus_activated = False
        self.round_time = 0
        self.slowdown_cycle = 0
        self.round_number += 1
        self.our_player.enter_safezone += 1

        for deleted_ghost in self.group_of_ghosts:
            self.group_of_ghosts.remove(deleted_ghost)
        for deleted_bonus in self.group_of_bonuses:
            self.group_of_bonuses.remove(deleted_bonus)
        for _ in range(self.round_number):
            self.group_of_ghosts.add(Ghost(random.randint(0, width - 64), random.randint(110, height - 164), self.ghost_images[0], 0))
            self.group_of_ghosts.add(Ghost(random.randint(0, width - 64), random.randint(110, height - 164), self.ghost_images[1], 1))
            self.group_of_ghosts.add(Ghost(random.randint(0, width - 64), random.randint(110, height - 164), self.ghost_images[2], 2))
            self.group_of_ghosts.add(Ghost(random.randint(0, width - 64), random.randint(110, height - 164), self.ghost_images[3], 3))
            self.group_of_ghosts.add(Ghost(random.randint(0, width - 64), random.randint(110, height - 164), self.ghost_images[3], 3))
        if (self.round_number > 2 and random.randint(1,2) == 2):
            self.group_of_bonuses.add(Bonus(random.randint(0, width - 64), random.randint(100, height - 164)))
        self.choose_new_target()
    def choose_new_target(self):
        new_ghost_to_catch = random.choice(self.group_of_ghosts.sprites())
        self.wanted_ghost_number = new_ghost_to_catch.type
        self.wanted_ghost = new_ghost_to_catch.original_image
    def pause(self, main_text, highest_score_text, subheading_text):

        global play
        main_text_create = self.ghost_font.render(main_text, True, "green")
        main_text_create_rect = main_text_create.get_rect()
        main_text_create_rect.center = (width//2, height//2-60)

        highest_score_text = self.ghost_font.render(highest_score_text, True, "green")
        highest_score_text_rect = highest_score_text.get_rect()
        highest_score_text_rect.center = (width//2, height // 2)
        
        subheading_text = self.ghost_font.render(subheading_text, True, "green")
        subheading_text_rect = subheading_text.get_rect()
        subheading_text_rect.center = (width//2, height // 2 + 60)

        screen.fill("black")
        screen.blit(main_text_create, main_text_create_rect)
        screen.blit(subheading_text, subheading_text_rect)
        screen.blit(highest_score_text, highest_score_text_rect)
        pygame.display.update()
        paused = True
        while paused:
            
            for one_event in pygame.event.get():
                if one_event.type == pygame.KEYDOWN:
                    if one_event.key == pygame.K_RETURN:
                        paused = False
                if one_event.type == pygame.QUIT:
                    paused = False
                    play = False
        
        
    def show_intro_screen(self):
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    intro = False
            screen.fill((0, 0, 0))
            intro_player = pygame.image.load("IMG/pacman-open-right.png")
            intro_player_rect = intro_player.get_rect()
            intro_player_rect.center = (width // 2 - 175, height // 2 + 100)
            
            intro_ghost_red = pygame.image.load("IMG/red-ghost.png")
            intro_ghost_red_rect = intro_ghost_red.get_rect()
            intro_ghost_red_rect.center = (width // 2 -20, height // 2 + 100)
            intro_ghost_cyan = pygame.image.load("IMG/cyan-ghost.png")
            intro_ghost_cyan_rect = intro_ghost_cyan.get_rect()
            intro_ghost_cyan_rect.center = (width // 2 +55, height // 2 + 100)
            intro_ghost_pink = pygame.image.load("IMG/pink-ghost.png")
            intro_ghost_pink_rect = intro_ghost_pink.get_rect()
            intro_ghost_pink_rect.center = (width // 2 +130, height // 2 + 100)
            intro_ghost_orange = pygame.image.load("IMG/orange-ghost.png")
            intro_ghost_orange_rect = intro_ghost_orange.get_rect()
            intro_ghost_orange_rect.center = (width // 2 +205, height // 2 + 100)
            screen.blit(intro_player, intro_player_rect)
            screen.blit(intro_ghost_red, intro_ghost_red_rect)
            screen.blit(intro_ghost_orange, intro_ghost_orange_rect)
            screen.blit(intro_ghost_cyan, intro_ghost_cyan_rect)
            screen.blit(intro_ghost_pink, intro_ghost_pink_rect)
            font = pygame.font.Font("font/pacman_font.otf", 48)
            text = font.render("CATCH THE GHOSTS!", True, (255, 255, 255))
            text_rect = text.get_rect(center=(width // 2, height // 2 - 100))
            screen.blit(text, text_rect)

            font = pygame.font.Font("font/pacman_font.otf", 24)
            text = font.render("PRESS ENTER TO START", True, (255, 255, 255))
            text_rect = text.get_rect(center=(width // 2, height // 2))
            screen.blit(text, text_rect)

            pygame.display.update()
    def reset_game(self):
        self.score = 0
        self.round_number = 0
        self.our_player.lives = 5
        self.our_player.enter_safezone = 2
        self.start_new_round()

        pygame.mixer.music.play(-1, 0.0)



ghost_group = pygame.sprite.Group()
bonus_group = pygame.sprite.Group()

my_game = Game(one_player, ghost_group, bonus_group)
my_game.start_new_round()

my_game.show_intro_screen()
        

fps = 60
clock = pygame.time.Clock()
play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                   one_player.back_to_safe_zone()
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_d) or (event.key == pygame.K_s):
                    one_player.image = one_player.images[one_player.current_image_index]
    
    screen.blit(my_game.bg_image, my_game.bg_rect)
    
    my_game.draw()
    
    ghost_group.draw(screen)
    ghost_group.update()
    my_game.update()
    bonus_group.draw(screen)
    bonus_group.update()
    player_group.draw(screen)
    player_group.update()
    clock.tick(fps)
    if my_game.bonus_activated:
        pygame.draw.rect(screen, "blue", (0, 100, width, height - 200), 4)
        my_game.cancel_bonus(pygame.time.get_ticks())
    pygame.display.update()
pygame.quit()