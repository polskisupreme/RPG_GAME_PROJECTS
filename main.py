import pygame
from sprites import *
from settings import *
import sys


class Game:
    def __init__(self):
        self.playing = None
        pygame.init()
        #tworzenie okna
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        #zegar/FPS
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('ArialTh.ttf', 32)
        self.running = True

        self.character_sprite = SpriteSheet('img/mainPlayer.png')
        self.terrain_sprite = SpriteSheet('img/floor_patterns.png')
        self.block_sprite = SpriteSheet('img/terrain.png')
        self.enemies_sprite = SpriteSheet('img/enemy.png')
        self.attack_sprite = SpriteSheet('img/attack.png')
        self.intro_background = pygame.image.load('./img/introbackground.png')
        self.game_over_bg = pygame.image.load('./img/gameover.png')

    def create_tilemap(self):
        for i, row in enumerate(tilemap):
            for j, coll in enumerate(row):
                Ground(self, j, i)
                if coll == 'B':
                    Block(self, j, i)
                if coll == 'P':
                    self.player = Player(self, j, i)
                if coll == 'E':
                    Enemy(self, j, i)
                if coll == 'W':
                    Water(self, j, i)

    def new(self):
        # rozpoczęcie nowej gry
        self.playing = True

        #grupy sprite'ów
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.create_tilemap()

    def events(self):
        # funkcja odpowiedzialna za wychodzenie z gry
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.playing = False
                self.running = False

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    if self.player.facing == 'up':
                        Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE)
                    if self.player.facing == 'down':
                        Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE)
                    if self.player.facing == 'right':
                        Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y)
                    if self.player.facing == 'left':
                        Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y)

    def update(self):
        # aktualizowanie wszystkich spriteów z grupy
        self.all_sprites.update()

    def draw(self):
        # rysowanie obiektow
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        # główna pętla gry
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def game_over(self):
        text = self.font.render('Game over', True, WHITE)
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))

        restart_button = Button(10, HEIGHT - 60, 120, 50, WHITE, BLACK, 'Restart', 32)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for e in  pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            self.screen.blit(self.game_over_bg, (0, 0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()


    def intro_screen(self):
        intro = True

        title = self.font.render('BEST RPG GAME', True, BLACK)
        title_rect = title.get_rect(x=WIDTH/2 - 150, y=150)

        play_button = Button(WIDTH/2 - 100, HEIGHT/2 - 50, 100, 50, WHITE, BLACK, 'PLAY', 32)

        while intro:
            for e in  pygame.event.get():
                if e.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()


g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()
