import pymunk
import pymunk.pygame_util
import pygame

GRAY = (220, 220, 220)
space = pymunk.Space()
space.gravity = 0, 500
b0 = space.static_body

class App:
    size = 1200, 568 #Androis aspect ratio 16:10
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.running = True

    def update_func(self):
        pass

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.image.save(self.screen, 'intro.png')

            self.screen.fill(GRAY)
            space.debug_draw(self.draw_options)
            pygame.display.update()
            self.update_func()
            space.step(0.01)

        pygame.quit()

if __name__ == '__main__':
    p0, p1 = (0, 400), (700, 400)
    segment = pymunk.Segment(b0, p0, p1, 4)
    segment.elasticity = 1

    body = pymunk.Body(mass=1, moment=10)
    body.position = (100, 200)

    circle = pymunk.Circle(body, radius=30)
    circle.elasticity = 0.95
    space.add(body, circle, segment)

    App().run()