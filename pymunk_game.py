from my_pymunk_base import pymunk, space, App, GRAY
from pymunk.vec2d import Vec2d
from pymunk.space_debug_draw_options import SpaceDebugColor
from mymap import Layer
from layers import layerlist
import pygame
pygame.init()
import time
import display_map

mainclock = pygame.time.Clock()

COLLTYPE_PL = 0
COLLTYPE_WALL = 1
COLLTYPE_GOAL = 2
COLLTYPE_SPIKE = 3
ISCOLLIDING = False
REACHED_GOAL = False
SPIKED = False
class CountCalls:
	def __init__(self, func):
		self.func = func
		self.num_calls = 0
	def __call__(self, *args, **kwargs):
		self.num_calls += 1
		res = self.func(*args, **kwargs)
		#print(f"Collided with walls {self.num_calls} times")
		return res


@CountCalls
def collided_wall(space, arbiter, arg3): #Lol I literally got this from SO, the original function took 2 args, but mine gave an error telling me it needs 3 args, so I just added arg3
	global ISCOLLIDING, playerbody			#Turns out arg3 is 'data'
	ISCOLLIDING = True
	return True
coll_handler = space.add_collision_handler(COLLTYPE_PL, COLLTYPE_WALL)
coll_handler.begin = collided_wall

def collided_goal(space, arbiter, data):
	global REACHED_GOAL
	REACHED_GOAL = True
	print("Congratulations!")
	return True
coll_handlergoal = space.add_collision_handler(COLLTYPE_PL, COLLTYPE_GOAL)
coll_handlergoal.begin = collided_goal

def collided_spike(space, arbiter, data):
	global SPIKED
	SPIKED = True
	print("SPIKED!")
	return True
coll_handlerspike = space.add_collision_handler(COLLTYPE_PL, COLLTYPE_SPIKE)
coll_handlerspike.begin = collided_spike

def display(layer):
	for brick in layer.bricks:
		space.add(*brick)
	try:
		space.add(layer.goalbody, layer.goal)
	except: pass
	try:
		for spike in layer.spikes:
			space.add(*spike)
	except: pass




class Child(App):
	def __init__(self):
		self.hor_accel = Vec2d(0.6, 0)
		self.vel = Vec2d(0,0)
		self.currlayer = 0
		self.cam_offset = Vec2d(0,0)
		self.map_cam_offset = Vec2d(0,0)
		self.key_down = 0 #not pressing any key
		super().__init__()


	def run(self):
		global playerbody, ISCOLLIDING, text
		while self.running:
			#print(playerbody.position)
			
			text = font.render(str(self.currlayer), True, (0,0,128), GRAY)
			if keymap['left'] and not keymap["left_up"] and not ISCOLLIDING:
				self.vel -= self.hor_accel
			elif keymap['right'] and not keymap['right_up'] and not ISCOLLIDING:
				self.vel += self.hor_accel
			else: self.vel = Vec2d(0,0)
			if keymap['left'] and keymap['left_up']:
				self.vel = Vec2d(0,0)
			if keymap['right'] and keymap['right_up']:
				self.vel = Vec2d(0,0)
			if keymap['up'] and not keymap['up_up']:
				playerbody.apply_force_at_world_point((0,-1000), playerbody.position)
				if not ((keymap['left'] and not keymap["left_up"]) or (keymap['right'] and not keymap['right_up'])):
					self.vel = Vec2d(-0.8*playerbody.velocity.x, 0)
			if keymap['down'] and not keymap['down_up']:
				self.vel = Vec2d(0, 0.5)
			if keymap['up'] and keymap['up_up']:
				self.vel = Vec2d(0,0)
			if keymap['down'] and keymap['down_up']:
				self.vel = Vec2d(0,0)

			if keymap['t']:
				self.cam_offset += (0,-6) #The vector by which the cam moves, in pygame space
				playerbody.position += (0, 6) #The negative of the vector
				for brick in space.shapes:
					space.remove(brick, brick.body)
				display(Layer(layers2use[self.currlayer].brick_pos, layers2use[self.currlayer].goal_pos, layers2use[self.currlayer].spike_pos, self.cam_offset))
				space.add(playerbody, box)
			if keymap['g']:
				self.cam_offset -= (0,-6) #The vector by which the cam moves, in pygame space
				playerbody.position -= (0, 6) #The negative of the vector
				for brick in space.shapes:
					space.remove(brick, brick.body)
				display(Layer(layers2use[self.currlayer].brick_pos, layers2use[self.currlayer].goal_pos, layers2use[self.currlayer].spike_pos, self.cam_offset))
				space.add(playerbody, box)

			if playerbody.position.y > 510: #This block is to facilitate automatic camera movement
				keymap['g'] = True
			elif not self.key_down:
				keymap['g'] = False
			if playerbody.position.y < 50:
				keymap['t'] = True
			elif not self.key_down:
				keymap['t'] = False


			if keymap['i']:
				self.map_cam_offset += (0, 3)
			if keymap['k']:
				self.map_cam_offset -= (0, 3)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
					pygame.image.save(self.screen, 'intro.png')

				if event.type == pygame.KEYDOWN:
					self.key_down = 1
					if event.key == pygame.K_LEFT:
						keymap["left"] = True;keymap["left_up"] = False; keymap["right"] = False; keymap['up'] = False; keymap['down'] = False

					if event.key == pygame.K_RIGHT:
						keymap["right"] = True;keymap["right_up"] = False; keymap["left"] = False; keymap['up'] = False; keymap['down'] = False

					if event.key == pygame.K_UP:
						keymap["up"] = True;keymap["up_up"] = False; keymap["down"] = False;keymap["left"] = False;keymap["right"] = False
					if event.key == pygame.K_DOWN:
						keymap["down"] = True;keymap["down_up"] = False; keymap["up"] = False;keymap["left"] = False;keymap["right"] = False


					if event.key == pygame.K_w:
						for brick in space.shapes:
							if brick != box:
								space.remove(brick, brick.body)
						self.currlayer = self.currlayer + 1 if self.currlayer<len(layers2use) - 1 else len(layers2use) -1
						display(Layer(layers2use[self.currlayer].brick_pos, layers2use[self.currlayer].goal_pos, layers2use[self.currlayer].spike_pos, self.cam_offset))
						print(f"Layer {self.currlayer}")
					if event.key == pygame.K_s:
						for brick in space.shapes:
							if brick != box:
								space.remove(brick, brick.body)
						self.currlayer = self.currlayer - 1 if self.currlayer>0 else 0
						display(Layer(layers2use[self.currlayer].brick_pos, layers2use[self.currlayer].goal_pos, layers2use[self.currlayer].spike_pos, self.cam_offset))
						print(f"Layer {self.currlayer}")
					if event.key == pygame.K_t:
						keymap['t'] = True
					if event.key == pygame.K_g:
						keymap['g'] = True
					if event.key == pygame.K_i:
						keymap['i'] = True
					if event.key == pygame.K_k:
						keymap['k'] = True
						

				if event.type == pygame.KEYUP:
					self.key_down = 0
					if event.key == pygame.K_LEFT:
						keymap["left_up"] = True
					elif event.key == pygame.K_RIGHT:
						keymap["right_up"] = True
					elif event.key == pygame.K_UP:
						keymap["up_up"] = True
					elif event.key == pygame.K_DOWN:
						keymap['down_up'] = True
					elif event.key == pygame.K_w:
						keymap['w'] = False
					elif event.key == pygame.K_s:
						keymap['s'] = False
					elif event.key == pygame.K_t:
						keymap['t'] = False
					elif event.key == pygame.K_g:
						keymap['g'] = False
					elif event.key == pygame.K_i:
						keymap['i'] = False
					elif event.key == pygame.K_k:
						keymap['k'] = False

			ISCOLLIDING = False
			self.screen.fill(GRAY)
			self.screen.blit(text, textRect)
			display_map.display_map(self.screen, layers2use, playerbody.position, self.currlayer, self.cam_offset, self.map_cam_offset)
			playerbody.velocity += self.vel
			space.debug_draw(self.draw_options)
			pygame.display.update()
			mainclock.tick(200)

			space.step(0.02)
			#if REACHED_GOAL: break
			

		print("You're done.")
		pygame.quit()


brick_width = 50
brick_height = 50

playerbody = pymunk.Body(mass=1, moment=10)
playerbody.position = (210, 150)
box = pymunk.Poly(playerbody, [(-30, -10), (-30, 10), (-10, 30), (10, 30), (30, 10), (30, -10), (10, -30), (-10, -30)])
box.collision_type = COLLTYPE_PL
box.friction = 0.1
box.elasticity = 0.4
space.add(playerbody, box)


layers2use = layerlist

keymap = {
    "up":False,
    "down":False,
    "left":False,
    "right":False,
    "up_up":True,
    "down_up":True,
    "left_up":True,
    "right_up":True,
	"w":False,
	"s":False,
	"t":False,
	"g":False,
	"i":False,
	"k":False
}

font = pygame.font.SysFont('arial.ttf',33)
text = font.render("0", True, (0,0,128), GRAY)
textRect = text.get_rect()
textRect.center = (20, 30)
display(layers2use[0])

sim = Child()
sim.run()
