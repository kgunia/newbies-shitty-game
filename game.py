import pygame

from random import randint

from models import Player, Enemy, Scoreboard
from utils import load_sprite, get_random_position, load_sound, print_text


WIDTH, HEIGHT = 600, 600
TOP_LEFT = (0, 0)
TOP_RIGHT = (WIDTH, 0)
BOTTOM_LEFT = (0, HEIGHT)
BOTTOM_RIGHT = (WIDTH, HEIGHT)
CENTER = (WIDTH/2, HEIGHT/2)
FPS = 60

VEl_0 = (0,0)

#COLOURS
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)

class Game():
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.background = load_sprite('grass', False)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ""

        self.theme_sound = load_sound('theme')
        self.theme_sound.set_volume(0.8)


        self.shoot_delay = 0

        self.scoreboard = Scoreboard()
        self.enemies = []
        self.bullets = []

        self.player = Player(CENTER, self.bullets.append)
        self.multiplier = 1

        for x in range(10):
            self.enemies.append(Enemy(get_random_position(self.screen)))

    def main_loop(self):
        self.theme_sound.play()
        pygame.mouse.set_visible(True)
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption('Newbie\'s shitty Game')


    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        is_key_presed = pygame.key.get_pressed()

        if self.player:
            if is_key_presed[pygame.K_a]:
                self.player.velocity.x = -1
            elif is_key_presed[pygame.K_d]:
                self.player.velocity.x = 1
            else:
                self.player.velocity.x = 0
            if is_key_presed[pygame.K_w]:
                self.player.velocity.y = -1
            elif is_key_presed[pygame.K_s]:
                self.player.velocity.y = 1
            else:
                self.player.velocity.y = 0
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                if self.shoot_delay > 0:
                    self.shoot_delay -= 1
                else:
                    self.player.shoot()
                    self.shoot_delay = 7


    def _process_game_logic(self):


        if self.player:
            self.player.look_at(pygame.mouse.get_pos())
            self.player.move()
            self.last_known_player_position = self.player.position

        for enemy in self.enemies:
            enemy.look_at(self.last_known_player_position)
            enemy.move(self.last_known_player_position)

        for bullet in self.bullets:
            bullet.move()

        if self.player:
            for enemy in self.enemies:
                if enemy.collides_with(self.player):
                    self.player = None
                    self.theme_sound.stop()
                    self.message = "You lost!"
                    break

        for bullet in self.bullets:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        for bullet in self.bullets:
            for enemy in self.enemies:
                if enemy.collides_with(bullet):
                    self.enemies.remove(enemy)
                    self.bullets.remove(bullet)
                    self.scoreboard.points += 1
                    if self.scoreboard.points % 10 == 0:
                        self.multiplier = self.scoreboard.points // 10

                    # for i in range(self.multiplier):
                    self.enemies.append(Enemy(get_random_position(self.screen)))
                    break

    def _draw(self):
        self.screen.blit(self.background, TOP_LEFT)

        if self.player:
           self.player.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        for bullet in self.bullets:
            bullet.draw(self.screen)

        if self.message:
            print_text(self.screen, self.message, self.font, CENTER)

        self.scoreboard.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(FPS)

    # def _get_game_objects(self):
    #     return [*self.enemies, self.player]
