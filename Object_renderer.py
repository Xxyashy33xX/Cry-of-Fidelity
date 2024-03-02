import pygame as pg
from Settings import *

class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_texture()
        self.sky_image = self.get_texture('Resources/Texture/sky.png', (width, height_half))
        self.sky_offset = 0

    def draw(self):
        self.draw_background()
        self.render_game_objects()


    def draw_background(self):
        # Update sky offset based on player movement
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % width
        # Draw the sky image twice to create a scrolling effect
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + width, 0))

        # Draw the floor
        pg.draw.rect(self.screen, Floor_colour, (0, height_half, width, height))

    def render_game_objects(self):
        # sorts rendered images into order depending on the distance
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)

        # Iterate through the list of objects to render
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos) # Blit (draw) the image onto the screen at the specified position

    @staticmethod
    def get_texture(path, res = (Texture_size, Texture_size)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_texture(self):
        return {
            1: self.get_texture('Resources/Texture/1.png'),
            2: self.get_texture('Resources/Texture/2.png'),
            3: self.get_texture('Resources/Texture/3.png'),
            4: self.get_texture('Resources/Texture/4.png'),
            5: self.get_texture('Resources/Texture/5.png'),
            6: self.get_texture('Resources/Texture/6.png')


        }