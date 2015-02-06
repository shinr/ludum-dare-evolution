from pyglet import gl
import pyglet
import random
import math

class Particle:
	def __init__(self, x, y, sx, sy, type="sine", player=False):
		self.x, self.y = x, y
		self.sx, self.sy = sx, sy
		
		self.w = random.randint(2, 6)
		self.h = self.w
		self.grav = 2
		
		self.life = 0.0
		self.totallife = 3.0
		
		self.dead =False
		self.type = type
		
		if player:
			self.color = [.8, .8, 1.0]
		else:
			self.color = [1.0, 1.0, 1.0]
		
	def update(self, dt):
		
		self.life += dt
		if self.life > self.totallife:
			self.dead = True
	
		self.y += self.sy * dt
		if self.type == "sine":
			self.x += math.sin(self.life * self.sx)
		elif self.type == "aimed":
			self.x += self.sx * dt
		
		self.color[0] -= dt / 3.0
		self.color[1] -= dt / 3.0
		self.color[2] -= dt / 3.0
		
		if self.color[0] < 0:
			self.color[0] = 0.0
		if self.color[1] < 0:
			self.color[1] = 0.0
		if self.color[2] < 0:
			self.color[2] = 0.0
		
	def render(self):
		gl.glColor3f(*self.color)
		gl.glVertex2f(self.x, self.y)
		
		