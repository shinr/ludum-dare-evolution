from pyglet import gl
import pyglet
import random
import particle
import math

class Branch:
	def __init__(self, x, y, lean, particles, gen, player, energy=1.0, vertical=False):
		self.x, self.y = x, y
		
		self.nodes = [(x, y)]
		self.branches = []
		
		self.particles = particles
		self.lean = lean
		self.energy = energy
		
		self.gen = gen
		self.grownnodes = [] 
		self.player= player
		self.vertical = vertical
		self.life = 0
		
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
				lean = -3
			else:
				lean = 3
				
			
				
			self.grownnodes.append((node[0], node[1], l))
				
			newbranch = Branch(node[0], node[1], lean, self.particles, (self.gen * 5), self.player, self.energy, True)
			self.branches.append(newbranch)
		self.energy += 3.5 * self.gen
	def grownode(self):
		if self.vertical:
			self.nodes.append((self.nodes[-1][0] + (random.randint(0, 6) - random.randint(0, 6)), self.nodes[-1][1] + (random.randint(2, 6 + self.lean) - random.randint(0, 4 - self.lean))))
		else:
			self.nodes.append((self.nodes[-1][0] + (random.randint(6 + self.lean, 15 + self.lean) - random.randint(6 - self.lean, 15 - self.lean)), self.nodes[-1][1] + (random.randint(2, 6) - random.randint(0, 4))))
		self.energy += 1.0 * self.gen
	
	def update(self, dt):
		if random.random() < .1 / (self.energy * self.gen):
			self.grownode()
	
		if random.random() < .1 / (self.energy * self.gen):	
			self.growbranch()
			
		for br in self.branches:
			br.update(dt)
			
		self.life += dt
			
	def render(self):
		gl.glBegin(gl.GL_LINE_STRIP)
		for vertex in self.nodes:
			if self.player.x < vertex[0] + 320 and self.player.x > vertex[0] - 320:
				r = .9 - math.sin(self.life * self.nodes.index(vertex)) / 1.5
				g = .9 - math.sin(self.life * self.nodes.index(vertex)) / 1.5
				b = 1.0 - math.sin(self.life * self.nodes.index(vertex)) / 2.0
			
				gl.glColor3f(r, g, b)
				if random.random() < .01:
					self.particles.add(particle.Particle(vertex[0], vertex[1], 20, 20))
				
				gl.glVertex2f(vertex[0], vertex[1])
		gl.glEnd()
		
		for branc in self.branches:
			branc.render()