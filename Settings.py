import math

res = width, height = 1440, 1000
width_half = width // 2
height_half = height // 2
fps = 75

Player_Pos = 1.5, 5  # on the mini map
Player_Angle = 0
Player_Speed = 0.004
Player_Rot_Speed = 0.0035

Mouse_sensitivity = 0.0002
Mouse_max_rel = 40
Mouse_border_left = 100
Mouse_border_right = width - Mouse_border_left

Floor_colour = (30,30,30)

fov = math.pi / 2
half_of_fov = fov / 2
number_of_rays = width // 2
half_number_of_rays = number_of_rays // 2
angle_change = fov / number_of_rays
depth = 20

screen_distance = width_half / math.tan(half_of_fov)
scaling_factor = width // number_of_rays

Texture_size = 256
Half_texture_size = Texture_size // 2

#pg.draw.line(self.game.screen, "white", ((px * 100), (py * 100)),
#                         ((100 * px) + (cos_A * 100 * main_depth), (100 * py) + (sin_A * 100 * main_depth))
#

#C:\Users\Aryan\PycharmProjects\pythonProject2\Resources