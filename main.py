import pygame as pg
import sys
from Settings import *
from Maps import *
from Player import *
from Raycasting import *
from myGame import *
from Object_renderer import *
from Sprite_object import *

class Main_Game:
	def __init__(self):
		pg.init()
		pg.mouse.set_visible(False)
		self.screen = pg.display.set_mode(res)
		self.clock = pg.time.Clock()
		self.delta_time = 1
		self.sprites = []
		self.new_game()
		self.is_game_over = False

	def new_game(self):
		self.map = Map(self)
		self.player = Player(self)
		self.sprites.append(SpriteObject(self,path='Resources/Sprites/Monster.png',  pos=(15, 5), speed=0.003))
		self.sprites.append(SpriteObject(self,path='Resources/Sprites/Monster2.png',  pos=(20, 12), speed=0.002))
		self.sprites.append(SpriteObject(self,path='Resources/Sprites/Monster2.png', pos=(8, 2), speed=0.002))
		self.sprites.append(SpriteObject(self,path='Resources/Sprites/Monster2.png',  pos=(11, 7), speed=0.001))
		self.sprites.append(SpriteObject(self, path='Resources/Sprites/5.png', pos=(30.5, 1.5), speed=0))
		self.sprites.append(SpriteObject(self, path='Resources/Sprites/5.png', pos=(27.3, 21.25), speed=0))
		self.sprites.append(SpriteObject(self, path='Resources/Sprites/9.png', pos=(28.5, 7.5), speed=0))
		self.sprites.append(SpriteObject(self, path='Resources/Sprites/9.png', pos=(11.5, 13.5), speed=0))
		self.sprites.append(SpriteObject(self, path='Resources/Sprites/9.png', pos=(3, 21.8), speed=0))
		self.sprites.append(SpriteObject(self, path='Resources/Sprites/8.png', pos=(21.5, 14.6), speed=0))
		self.sprites.append(SpriteObject(self, path='Resources/Sprites/8.png', pos=(6, 19.5), speed=0))
		self.sprites.append(SpriteObject(self, path='Resources/Sprites/7.png', pos=(11.5, 3.5), speed=0))
		self.sprites.append(SpriteObject(self, path='Resources/Sprites/7.png', pos=(22.5, 3.5), speed=0))
		self.sprites.append(SpriteObject(self, path='Resources/Sprites/5.png', pos=(18.5, 18.5), speed=0))
		self.sprites.append(SpriteObject(self, path='Resources/Sprites/6.png', pos=(24.5, 14.5), speed=0, shift=0)) # left sign for trick
		self.object_renderer = ObjectRenderer(self)
		self.raycasting = RayCasting(self)
		self.static_sprite = SpriteObject(self)


	def update(self):
		self.player.update()
		self.check_end_game_condition()
		self.raycasting.update()
		self.static_sprite.update()
		pg.display.flip()
		self.delta_time = self.clock.tick(fps)
		pg.display.set_caption(f'{self.clock.get_fps() :.1f}')
		for sprite in self.sprites:
			sprite.update()

	def check_end_game_condition(self):
		end_x, end_y = 31.5, 23.5  # end point coordinates
		tolerance = 1  # How close the player needs to be to the end point

		if abs(self.player.x - end_x) < tolerance and abs(self.player.y - end_y) < tolerance:
			self.is_game_over = True

	def show_end_screen(self):
		self.screen.fill((0, 0, 0))  # Clears the screen
		font = pg.font.Font(None, 50)  # defining the font
		text = font.render("Thanks for playing, you have escaped the Fidelity of the Crying monsters!!", True, (255, 255, 255))
		text_rect = text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
		self.screen.blit(text, text_rect)
		pg.display.flip()  # Updates the display to show the end screen
		pg.time.wait(10000)  # Wait a few seconds before closing
		
	def draw(self):
		#self.screen.fill("black")
		self.object_renderer.draw()
		#self.map.draw()
		#self.player.draw()


	def event_checker(self):
		for event in pg.event.get():
			if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
				pg.quit()
				sys.exit()

	def run(self):
		while not self.is_game_over:
			self.event_checker()
			self.update()
			self.draw()
		self.show_end_screen()

if __name__ == '__main__':
    g = myGame()

    while g.running:
        g.curr_menu.display_menu()
        g.game_loop()
