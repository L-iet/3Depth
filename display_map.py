import pygame
from pymunk.vec2d import Vec2d

def display_map(screen,layers, playerpos, currlayer, cam_offset, map_cam_offset):
	#cam_offset: if cam is moving, we want to preserve players position on map
	font = pygame.font.SysFont('arial.ttf',33)
	map_correction_vec = 0.16*cam_offset
	for ind,layer in enumerate(layers):
		layer_b = layer.brick_pos
		for i in range(len(layer_b[0])):
			for j in range(len(layer_b)):
				if layer_b[j][i]:
					x, y = Vec2d(800+i*8, 8+j*8 + (ind*180)) + map_cam_offset #position the map appropriately
					pygame.draw.rect(screen,(0,200,200),(x, y, 8, 8))
		if layer.goal_pos:
			apparent_goal_pos = Vec2d(*(0.16*layer.goal_pos + (793, -4) + (0,180*ind))) + map_cam_offset #0.16 is the scaling factor for the position vector to fit on the map
			pygame.draw.circle(screen, (200, 200, 0), apparent_goal_pos, 3)#(0, 180*ind) ensures that that it is positioned on each layer with a goal, (793, -4) is to position it on the screen, first layer


		layertext = font.render(str(ind), True, (0,0,128), (220, 220, 220)) #GRAY is the background color
		layertextRect = layertext.get_rect()
		layertextRect.center = map_cam_offset  + (940, ind*175 + 98) #place layer number accordingly
		screen.blit(layertext, layertextRect)

	apparent_player_pos = Vec2d(*(0.16*playerpos + (787, -4) +(0,180*currlayer)))
	apparent_player_pos = apparent_player_pos + map_correction_vec + map_cam_offset
	pygame.draw.rect(screen, (0,0,0), (*apparent_player_pos, 8, 8))

