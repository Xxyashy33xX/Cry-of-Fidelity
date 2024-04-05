from Settings import *
import pygame as pg
import math

class Player:
    def __init__(self, game): # initialise 
        self.game = game
        self.x, self.y = Player_Pos
        self.angle = Player_Angle

    def movement(self):
        sin_a = math.sin(self.angle) # to find the direction the player is looking at
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = Player_Speed * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()
        num_key_pressed = -1
        if keys[pg.K_w]: #the player presses "W"
            num_key_pressed += 1
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]: #the player presses "S"
            num_key_pressed += 1
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]: #the player presses "A"
            num_key_pressed += 1
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]: #the player presses "D"
            num_key_pressed += 1
            dx += -speed_sin
            dy += speed_cos

        self.check_wall_collision(dx, dy)


        self.angle %= math.tau

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy): # checks if the player has gone inside the wall, and if so stops movement

        if self.check_wall(int(self.x + dx), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x ), int(self.y + dy)):
            self.y += dy
        self.angle %= math.tau

    def draw(self): # draws a white line to show where the player is looking at in the 2D map
        pg.draw.line(self.game.screen, "white", (self.x * 100, self.y * 100),
                     (self.x * 100 + width * math.cos(self.angle),
                      self.y * 100 + width * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, "red", (self.x * 100, self.y * 100), 15) # The shape of the player in the 2D map

    def mouse_control(self):
        # Get the current mouse position
        Mx, My = pg.mouse.get_pos()

        # Check if the mouse is outside the specified borders
        if Mx < Mouse_border_left or Mx > Mouse_border_right:
            pg.mouse.set_pos([width_half, height_half]) # Center the mouse position if it's outside the borders

        self.rel = pg.mouse.get_rel()[0] # Get the relative movement of the mouse
        self.rel = max(-Mouse_max_rel, min(Mouse_max_rel, self.rel)) # Limit the relative movement within a specified range
        # Update the viewing angle based on the relative mouse movement and sensitivity
        self.angle += self.rel * Mouse_sensitivity * self.game.delta_time



    def update(self): # outputs the movements and mouse controls to the update method
        self.movement()
        self.mouse_control()
# to give "special" functionality to certain methods to make them act as getters, setters or deleters when we define properties in a class.
    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
