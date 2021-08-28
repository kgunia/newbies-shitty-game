from pygame.math import Vector2
from pygame.transform import rotozoom
from pygame import mouse
from pygame.font import Font

from utils import load_sprite, load_sound, print_text

import math
import random

UP = Vector2(0,-1)
DOWN = Vector2(0,1)
LEFT = Vector2(-1,0)
RIGHT = Vector2(1,0)


class GameObject:

    def __init__(self, position, sprite, velocity=(0,0), acceleration = 1):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 4
        self.velocity = Vector2(velocity)
        self.acceleration = acceleration
        self.direction = Vector2(UP)
        self.angle = 0

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def look_at(self, destination):
        angle_rad = math.atan2(self.position.y - destination[1], destination[0] - self.position.x)
        self.angle = math.degrees(angle_rad)


    def move(self):
        self.position = self.position + self.velocity * self.acceleration

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius




class Humanoid(GameObject):

    def draw(self, surface):
        rotated_surface = rotozoom(self.sprite, self.angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def look_at(self, destination):
        angle_rad = math.atan2(self.position.y - destination[1], destination[0] - self.position.x)
        self.angle = math.degrees(angle_rad)
        self.direction = (destination - self.position).normalize()
        # self.direction = self.direction.rotate_ip(self.angle)

class Player(Humanoid):
    def __init__(self, position, create_bullet_callback):
        self.create_bullet_callback = create_bullet_callback
        self.shoot_sound = load_sound('pistol')
        self.die_sound = load_sound('die')
        self.eating_sound = load_sound('eating')
        super().__init__(position, load_sprite('player', ratio=0.4), Vector2(0), acceleration=2)

    def __del__(self):
        self.die_sound.play()
        self.eating_sound.play()


    def shoot(self):
        bullet_speed = 10
        bullet_velocity = self.direction * bullet_speed
        print(bullet_velocity)
        bullet = Bullet(self.position, bullet_velocity)
        self.create_bullet_callback(bullet)
        self.shoot_sound.play()



class Enemy(Humanoid):
    def __init__(self, position):
        super().__init__(position, load_sprite('enemy', ratio=0.4), Vector2(1))
        self.zombie_sound = load_sound('zombie')


    def __del__(self):
        self.zombie_sound.play()

    def move(self, target):
        self.position += (target - self.position).normalize() * self.acceleration
        #self.position = self.position + self.velocity.rotate_ip(self.angle)

class Bullet(GameObject):

    def __init__(self, position, velocity):
        super().__init__(position, load_sprite('bullet'), velocity)

class Scoreboard():
    def __init__(self):
        self.points = 0
        self.font = Font(None, 24)
        self.message = f"Points: {self.points}"

    def draw(self, surface):
        self.message = f"Points: {self.points}"
        print_text(surface, self.message, self.font, (45,20))

