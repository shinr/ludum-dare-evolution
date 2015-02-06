import pyglet
from pyglet import gl
import particle
import random
import branch
import math

class WorldTree:
	def __init__(self, particles, player):
		self.x, self.y = 2320, 150
		self.sx, self.sy = 0.0, 0.0
		self.w, self.h = 32, 32
		self.xmod, self.ymod = 0.0, 0.0
		self.nodes = [(self.x, self.y), (self.x + 2, self.y + 16), (self.x - 4, self.y + 36)]
		self.branches = []
		self.grownnodes = []
		self.particles = particles
		self.blockable = False
		self.energy = 0.1
		self.life = 0.1
		self.phase = 0
		self.pedestal = False
		self.artifact = False
		self.player = player
		self.energymultiplier = 1
		self.cleanup = False
		
	def grownode(self):
		self.nodes.append((self.nodes[-1][0] + (random.randint(0, 7) - random.randint(0, 7)), self.nodes[-1][1] + random.randint(8, 16)))
		
	def growbranch(self):
		ungrownnodes = []
		for node in self.nodes:
			for i in range(0, 2):
				if not (node[0], node[1], i) in self.grownnodes and not node == self.nodes[0]:
					ungrownnodes.append((node, i))
				
		if ungrownnodes:
			i = random.randint(0, len(ungrownnodes) - 1)
			
			node, l = ungrownnodes[i]
			if l == 0:
				lean = -5
			else:
				lean = 5
				
			self.grownnodes.append((node[0], node[1], l))
				
			newbranch = branch.Branch(node[0], node[1], lean, self.particles, 1, self.player)
			self.branches.append(newbranch)
			self.energy -= 2.0
		
	def update(self, dt):
		if random.random() < .01:
			if self.energy > 1.0:
				self.grownode()
				self.energy -= 1.0
			
		if random.random() < .02:
			if self.energy > 2.0:
				self.growbranch()
				
			
		for br in self.branches:
			br.update(dt)
			
		self.energy += (dt / (10.0 * self.life))*self.energymultiplier
		self.life += dt / 10.0
		#print self.energy
	
	def render(self):
		gl.glBegin(gl.GL_LINE_STRIP)
		for vertex in self.nodes:
			r = 1.0 - math.sin(self.life* 10 * self.nodes.index(vertex))
			g = 1.0 - math.sin(self.life * 10 * self.nodes.index(vertex))
			b = 1.0 - math.sin(self.life* 10 * self.nodes.index(vertex))
			
			gl.glColor3f(r, g, b)
			if self.player.x < vertex[0] + 320 and self.player.x > vertex[0] - 320:
				if random.random() < .05:
					self.particles.add(particle.Particle(vertex[0], vertex[1], 20, 20))
				
				gl.glVertex2f(vertex[0], vertex[1])
			
		
		gl.glEnd()
		
		for branch in self.branches:
			branch.render()