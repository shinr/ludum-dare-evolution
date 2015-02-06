import particle
from pyglet import gl

class ParticleManager:
	def __init__(self):
		self.particles = []
		
		self.limit = 100
		self.player = None
		
	def add(self, particle):
		self.particles.append(particle)
		
	def popparticle(self):
		self.particles.pop(-1)	
			
	def update(self, dt):
		toremove = []
		for particle in self.particles:
			particle.update(dt)
			if particle.dead:
				toremove.append(particle)
			
		for delete in toremove:
			self.particles.remove(delete)
			
		if len(self.particles) > self.limit:
			self.popparticle()
			
	def render(self):
		gl.glBegin(gl.GL_POINTS)
		
		for particle in self.particles:	
			if self.player.x < particle.x + 320 and self.player.x > particle.x - 320:
				particle.render()
		
		gl.glEnd()