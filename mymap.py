from pymunk.vec2d import Vec2d
import pymunk

class Layer:
	"""Creates bodies and shapes for all physical things in the layer.
	In setting the positions, we subtract the cam_offset in case we are moving the camera."""
	def __init__(self, bricks:tuple, goal:Vec2d = None, spike_pos:tuple = None, cam_offset:Vec2d = Vec2d(0,0)):
		super(Layer, self).__init__()
		self.brick_pos = bricks
		self.goal_pos = goal
		self.spike_pos = spike_pos
		self.cam_offset = cam_offset
		self.bricks = []
		for i in range(len(bricks[0])):
			for j in range(len(bricks)):
				if bricks[j][i]:
					pos_x, pos_y = (80+i*50, 80+j*50) - cam_offset #50 is brick_width
					body = pymunk.Body(body_type=pymunk.Body.STATIC)
					body.position = (pos_x, pos_y)
					brick = pymunk.Poly.create_box(body, (50, 50)) #shape takes in body, 50 is brick_width
					brick.collision_type = 1
					brick.friction = 0.6
					brick.elasticity = 0.6
					self.bricks.append((body, brick))


		if goal:
			goalbody = pymunk.Body(body_type=pymunk.Body.STATIC)
			goalbody.position = goal - cam_offset
			goal = pymunk.Circle(goalbody, 10)
			goal.color = (255, 165, 0, 0)
			goal.collision_type = 2
			goal.friction = 0.9
			self.goalbody = goalbody
			self.goal = goal
		if spike_pos:
			self.spikes = []
			for spike in spike_pos:
				spikebody = pymunk.Body(body_type=pymunk.Body.STATIC)
				spikebody.position = spike - cam_offset
				spike_shape = pymunk.Poly(spikebody, [(0, 0), (15, 0), (7.5, -13)]) 
				spike_shape.color = (255, 0, 0, 0)
				spike_shape.collision_type = 3
				spike_shape.friction = 0.9
				self.spikes.append((spikebody, spike_shape))



		
		

