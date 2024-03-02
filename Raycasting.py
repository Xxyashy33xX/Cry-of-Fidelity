import pygame as pg
import math
from Settings import *
from Object_renderer import*


step = 0.0001
class RayCasting:

    def __init__(self, game):
        self.game = game
        # Initialise ray casting related attributes
        self.ray_casting_result = []
        self.objects_to_render = []

        # Access textures from the ObjectRenderer in the game object
        self.textures = self.game.object_renderer.wall_textures

    def get_objects_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            main_depth, projection_height, texture, offset = values

            if projection_height < height:
                # Extract the wall column from the texture
                wall_column = self.textures[texture].subsurface(offset * (Texture_size - scaling_factor), 0, scaling_factor, Texture_size)
                # Scale the wall column to match the projected height
                wall_column = pg.transform.scale(wall_column, (scaling_factor, projection_height))
                # Calculate the position of the wall in the 2D view
                wall_position = (ray * scaling_factor, height_half - projection_height //2)

            else:
                Texture_height = Texture_size * height / projection_height
                wall_column = self.textures[texture].subsurface(
                    offset * (Texture_size - scaling_factor), Half_texture_size - Texture_height // 2,
                    scaling_factor, Texture_height
                )
                wall_column = pg.transform.scale(wall_column, (scaling_factor, height))
                wall_position = (ray * scaling_factor, 0)
            # Append the information to the list of objects to render
            self.objects_to_render.append((main_depth, wall_column, wall_position))
    def cast_ray(self):
        self.ray_casting_result = []

        px, py = self.game.player.pos
        X_map, Y_map = self.game.player.map_pos
        texture_vert, texture_hor = 1,1

        angle_ray = (self.game.player.angle - half_of_fov) + step
        for ray in range(number_of_rays):
            sin_A = math.sin(angle_ray)
            cos_A = math.cos(angle_ray)

            # vertical intersections
            x_vertical, dx = (X_map + 1, 1)\
                if cos_A > 0 \
                else (X_map - 1e-6, -1)

            depth_vertical = (x_vertical - px) / cos_A
            y_vertical = py + (sin_A * depth_vertical)

            depth_change = dx / cos_A
            dy = sin_A * depth_change

            for i in range(depth): # Iterate through the depth to find the vertical texture on the wall
                tile_vertical = int(x_vertical), int(y_vertical)
                # Check if the current vertical tile is part of the world map
                if tile_vertical in self.game.map.world_map:
                    texture_vert = self.game.map.world_map[tile_vertical]
                    break
                # Update the coordinates and depth for the next iteration
                x_vertical += dx
                y_vertical += dy
                depth_vertical += depth_change

            # horizontal intersections

            y_horizontal, dy = (Y_map + 1, 1) \
                if sin_A > 0 \
                else (Y_map - 1e-6, -1)

            depth_horizontal = (y_horizontal - py) / sin_A
            x_horizontal = px + (cos_A * depth_horizontal)

            depth_change = dy / sin_A
            dx = cos_A * depth_change

            for i in range(depth):  # Iterate over the depth of the ray
                tile_horizontal = int(x_horizontal), int(y_horizontal)
                # Check if the tile is within the world map
                if tile_horizontal in self.game.map.world_map:
                    texture_hor = self.game.map.world_map[tile_horizontal]
                    # Retrieve the texture for the horizontal direction
                    break
                x_horizontal += dx
                y_horizontal += dy
                depth_horizontal += depth_change  # Update the horizontal depth

            # depth of the ray

            if depth_horizontal < depth_vertical:
                # If the vertical depth is greater than horizontal depth
                main_depth, texture = depth_horizontal, texture_hor
                x_horizontal %= 1  # Get the fractional part of the vertical position
                # Set offset based on the direction of the ray
                offset = x_horizontal if cos_A < 0 else (1 - x_horizontal)

            else:  # Do the opposite if the horizontal depth is greater than vertical depth
                main_depth, texture = depth_vertical, texture_vert
                y_vertical %= 1
                offset = (1 - y_vertical) if sin_A < 0 else y_vertical

            # fix fishbowl effect
            main_depth *= math.cos(self.game.player.angle - angle_ray)

            #projection of the ray
            projection_height = screen_distance / (main_depth + step)

            #draw walls
            #pg.draw.rect(self.game.screen, 'white',
                       #(ray * scaling_factor, height_half - projection_height // 2, scaling_factor, projection_height))

            self.ray_casting_result.append((main_depth, projection_height, texture, offset))

            angle_ray += angle_change

    def update(self):
        self.cast_ray()
        self.get_objects_to_render()