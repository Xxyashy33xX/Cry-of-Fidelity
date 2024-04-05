import pygame as pg
from Settings import *
import math

class SpriteObject: # inisialise all variables
    def __init__(self, game, path='Resources/Sprites/Monster.png',
                 pos=(11, 5), scale=0.7, shift=0.27, speed=0.0025): 
        self.game = game
        self.player = game.player
        self.x, self.y = pos
        self.image = pg.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.sprite_half_width = 0
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift
        self.speed = speed

    def get_sprite_projection(self):
        proj = screen_distance / self.norm_dist * self.SPRITE_SCALE
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj

        image = pg.transform.scale(self.image, (proj_width, proj_height))

        self.sprite_half_width = proj_width // 2
        # Calculate the vertical shift of the sprite based on its height
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT
        pos = self.screen_x - self.sprite_half_width, height_half - proj_height // 2 + height_shift

        # Calculate the vertical shift of the sprite based on its height
        self.game.raycasting.objects_to_render.append((self.norm_dist, image, pos))

    def get_sprite(self):
        # Calculate the relative position of the sprite to the player
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy

        # Calculate the angle (theta) from the player to the sprite
        self.theta = math.atan2(dy, dx)
        delta = self.theta - self.player.angle

        # Adjust for angles greater than 180 degrees or negative angles
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau

        # Calculate the number of rays to the sprite from the player's view angle
        delta_rays = delta / angle_change

        # Calculate the horizontal screen position of the sprite
        self.screen_x = (half_number_of_rays + delta_rays) * scaling_factor
        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)

        # If the sprite is within the player's view, calculate its projection
        if -self.IMAGE_HALF_WIDTH < self.screen_x < (width + self.IMAGE_HALF_WIDTH) and self.norm_dist > 0.5:
            self.get_sprite_projection()

    def update(self):
        # Calculate direction vector to the player
        dx = self.game.player.x - self.x
        dy = self.game.player.y - self.y
        # Calculate the distance to the player
        distance = math.sqrt(dx ** 2 + dy ** 2)
        # Define a chase threshold distance
        chase_threshold = 3.5

        # Only move the sprite towards the player if within chase_threshold
        if distance <= chase_threshold:
            # Normalise the direction vector if distance is not zero
            if distance > 0:
                dx, dy = dx / distance, dy / distance

            # Move the sprite towards the player, adjusting speed based on delta_time
            self.x += dx * self.speed * self.game.delta_time
            self.y += dy * self.speed * self.game.delta_time

        self.get_sprite()



