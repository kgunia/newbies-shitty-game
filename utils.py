from pygame.image import load
from pygame.transform import scale
from pygame.math import Vector2
from pygame.mixer import Sound
from pygame import Color

from random import randint


# game utils ---------------------------------------------------------------------#

def scale_sprite(sprite,ratio):
    return scale(sprite, (int(sprite.get_width()*ratio), int(sprite.get_height()*ratio)))

def load_sprite(name, with_alpha=True, ratio=1):
    path = f"assets/sprites/{name}.png"
    loaded_sprite = load(path)
    loaded_sprite = scale_sprite(loaded_sprite, ratio)
    loaded_sprite.set_colorkey((0, 0, 0))
    return loaded_sprite.convert_alpha() if with_alpha else loaded_sprite

def get_random_position(surface, offscreen=True):
    width, height = surface.get_width(), surface.get_height()
    if offscreen:
        return Vector2(randint(-width,width*2), randint(-height, height*2))
    else:
        return Vector2(randint(0, width), randint(0, height))

def load_sound(name):
    path = f"assets/sounds/{name}.wav"
    return Sound(path)

def print_text(surface, text, font, position, color=Color('white')):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    rect.center = Vector2(position)
    surface.blit(text_surface,rect)

# model utils --------------------------------------------------------------------#

def increase_value(value, max_value=1, step=1):
    return value + step if value < max_value else max_value

def decrease_value(value, min_value=-1, step=1):
    return value - step if value > min_value else min_value

def reset_value(value, base_value=0, step=1):
    if value > base_value: return_value = value - step
    elif value < base_value: return_value = value + step
    else: return_value = base_value
    return return_value

