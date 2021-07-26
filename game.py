import pygame
import os
import random
import pickle

pygame.display.set_caption("Flappy Bird")
pygame.init()

font = pygame.font.SysFont('Comic Sans MS', 30)

RES = (575, 800)

screen = pygame.display.set_mode(RES)

clock = pygame.time.Clock()

bird_img = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png")).convert_alpha()), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png")).convert_alpha()), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")).convert_alpha())]
pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")).convert_alpha())
base_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")).convert_alpha())
bg = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")).convert())

class Bird:
    IMGS = bird_img
    ANIMATION_TIME = 10

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tick = 0
        self.vel = 0
        self.img_cnt = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.y -= 5
        self.vel = -5
        self.tick = 0
    
    def move(self):
        self.tick += 1
        disp = (self.vel*self.tick) + 0.5*(self.tick)**2 

        if disp >= 15:
            disp = 15

        self.y = self.y + disp

    def draw(self, screen):
        self.img_cnt += 1

        if self.img_cnt <= self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_cnt <= self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_cnt <= self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_cnt <= self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        else:
            self.img = self.IMGS[0]
            self.img_cnt = 0

        screen.blit(self.img, (self.x, self.y))


class Pipe:

    def __init__(self):
        self.top_img = pygame.transform.flip(pipe_img, False, True)
        self.bot_img = pipe_img
        self.height = random.randrange(10, 500)
        self.top = self.height - self.top_img.get_height()
        self.bot = self.height + 200
        self.x = 575
        self.passed = False

    def move(self, up):
        self.x -= 5
        
        if up:
            self.top -= 3
            self.bot -= 3
        if not up:
            self.top += 3
            self.bot += 3

    def collision(self, bird):
        bird_mask = pygame.mask.from_surface(bird.img)
        top_mask = pygame.mask.from_surface(self.top_img)
        bot_mask = pygame.mask.from_surface(self.bot_img)

        if top_mask.overlap(bird_mask, (bird.x - self.x, round(bird.y) - self.top)) or bot_mask.overlap(bird_mask, (bird.x - self.x, round(bird.y) - self.bot)):
            return True
        
        return False

    def draw(self, screen):
        screen.blit(self.top_img, (self.x, self.top))
        screen.blit(self.bot_img, (self.x, self.bot))

class Base:

    def __init__(self, x):
        self.y = 730
        self.x = x
        self.img = base_img

    def move(self):
        self.x -= 5

    def collision(self, bird):
        bird_mask = pygame.mask.from_surface(bird.img)
        base_mask = pygame.mask.from_surface(self.img)

        if base_mask.overlap(bird_mask, (0, round(bird.y) - self.y)):
            return True
        
        return False


    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

def draw_screen(screen, birds, pipes, bases, score, clock):
    screen.blit(bg, (0,0))

    for pipe in pipes:
        pipe.draw(screen)
    for bird in birds:
        bird.draw(screen)
    for base in bases:
        base.draw(screen)
    
    score_card = font.render('Score :' + str(score), False, (0, 0, 0))
    screen.blit(score_card,(0,0))
    Hi_score_card = font.render('Hi-Score :' + str(Hi), False, (0, 0, 0))
    screen.blit(Hi_score_card, (0, 30))

    # fps = font.render('FPS: {}'.format(clock.get_fps()), False, (0, 0, 255))
    # screen.blit(fps, (25, 50))

    if len(birds) == 0:
        gameover = font.render("Press Any Key to Respawn", False, (255, 255, 255))
        rect = gameover.get_rect()
        rect.center = screen.get_rect().center
        screen.blit(gameover, rect)

    pygame.display.update()

def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        screen.fill((255, 255, 255))
        largeText = pygame.font.Font('freesansbold.ttf',115)
        textSurface = largeText.render("Flappy", True, (0,0,0))
        TextRect = textSurface.get_rect()
        TextRect.center = ((575/2),(800/2))
        screen.blit(textSurface, TextRect)

        pygame.draw.rect(screen, (0,0,0),(300,500,100,50))

        
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        

        if 150+100 > mouse[0] > 150 and 500+50 > mouse[1] > 500:
            pygame.draw.rect(screen, (0,50,0),(150,500,100,50))
            if click[0] == 1:
                main() 
        else:
            pygame.draw.rect(screen, (0,0,0),(150,500,100,50))

        if 300+100 > mouse[0] > 300 and 500+50 > mouse[1] > 500:
            pygame.draw.rect(screen, (0,50,0),(300,500,100,50))
            if click[0] == 1:
                pygame.quit()
                quit()
        else:
            pygame.draw.rect(screen, (0,0,0),(300,500,100,50))  

        small_text = pygame.font.Font('freesansbold.ttf', 30)
        play_surf = small_text.render("Play!", True, (255,255,255))
        quit_surf = small_text.render("Quit", True, (255,255,255))
        play_rect = play_surf.get_rect()
        quit_rect = quit_surf.get_rect()
        play_rect.center = (150+50, 500+25)
        quit_rect.center = (300+50, 500+25)
        screen.blit(play_surf, play_rect)
        screen.blit(quit_surf, quit_rect)


        clock.tick(60)

        pygame.display.update()

Hi = 0

def main():
    global Hi
    play = True
    up = True

    pipes = [Pipe()]
    bases = [Base(0)]
    birds = [Bird(50,250)]

    score = 0

    run = False

    while play:
        clock.tick(60)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                play = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:

                if len(birds) > 0:
                    birds[0].jump()
                    run = True

                if len(birds) == 0:
                    main()
        
        
        draw_screen(screen, birds, pipes, bases, score, clock) 

        if run == True:
             
            rem_b = []
            rem_p = []
            add_p = False
            add_b = False

            for bird in birds:

                if bird.y < 0:
                    Hi = max(score, Hi)
                    birds.remove(bird)

                bird.move()

            for pipe in pipes:

                if pipe.bot > 730 and not up:
                    up = True

                if pipe.bot - 200 < 10 and up:
                    up = False

                pipe.move(up)

                for bird in birds:

                    if pipe.collision(bird):
                        Hi = max(score, Hi)
                        birds.remove(bird)

                    if pipe.x + pipe.top_img.get_width() < 0:
                        rem_p.append(pipe)

                    if pipe.x < bird.x and not pipe.passed:
                        add_p = True
                        pipe.passed = True 
                        score += 1

            if add_p:
                pipes.append(Pipe())

            for rp in rem_p:
                pipes.remove(rp)

            for base in bases:

                base.move()

                for bird in birds:
                    if base.collision(bird):
                        Hi = max(score, Hi)
                        birds.remove(bird)

                if base.x + base.img.get_width() <= 0:
                    rem_b.append(base)

                if base.x <= 0 and len(bases) < 2:
                    add_b = True

            if add_b:
                bases.append(Base(bases[0].x + bases[0].img.get_width()))

            for rb in rem_b:
                bases.remove(rb)

        
game_intro()