import pygame,random
from display import *
from camera import *

class BubbleParticle():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.dx = (random.randint(0,4)-2)/10
        self.dy = (random.randint(0,3)-2)/10
        self.radius = random.randint(1,4)
        self.duration = random.randint(4,6)
    def update(self):
        self.x += self.dx
        self.y += self.dy
        #self.dy -= .02
        self.duration -= .1
    def draw(self,surface):
        pygame.draw.circle(surface,(255,255,255),(int(self.x-camera.x),int(self.y-camera.y)),self.radius)

class ParticleSystem():
    def __init__(self):
        self.particles = []

    def add_particle(self,x,y):
        self.particles.append(BubbleParticle(x,y))

    def update(self):
        for particle in self.particles:
            particle.update()
            if particle.duration < 0:
                self.particles.remove(particle)
            particle.draw(display.display)

particle_system = ParticleSystem()