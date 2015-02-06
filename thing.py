import pyglet
from pyglet import gl
import random
import particle
import math
import resources

class Thing:
	def __init__(self, x, y, **stuff):
		self.x, self.y = x, y
		self.sx, self.sy = 0.0, 0.0
		self.w, self.h = 32, 32
		self.xmod, self.ymod = 0.0, 0.0
		self.energy = 12.0
		self.cleanup = False
		self.player = False
		self.playerref = None
		self.particles = None
		self.artifact = False
		self.sound = None
		self.music = pyglet.media.Player()
		self.blockable = False
		self.static = False
		self.deadly = False
		self.color = (1.0, 1.0, 1.0, 1.0)
		self.visible = True
		self.phase = 0
		self.activatephase = 0
		self.deactivatephase = 9999999
		self.angle = 0.0
		self.item = None
		self.held = False
		self.pedestal = False
		self.placed = False
		self.desound = None
		self.vertices = []
		self.life = 0
		
		
		if "particlemanager" in stuff:
			self.particles = stuff["particlemanager"]
		
		if "player" in stuff:
			self.player = True
			self.vertices = [(16, 0),
							  (14, 4),
							  (15, 6),
							  (13, 14),
							  (14, 16),
							  (12, 27),
							  (0, 23),
							  (0, 24),
							  (14, 29),
							  (15, 36),
							  (17, 36),
							  (18, 29),
							  (31, 24),
							  (31, 23),
							  (19, 27),
							  (17, 16),
							  (16, 14),
							  (18, 6),
							  (17, 4)
							  
			]
			
		if "particles" in stuff:
			self.particles = stuff["particles"]
			
		if "artifact" in stuff:
			self.artifact = stuff["artifact"]
			self.sound = stuff["sound"]
			self.music.queue(self.sound)
			self.music.eos_action = self.music.EOS_LOOP
			self.vertices += [(self.x, self.y),
							  (self.x, self.y + 2),
							  (self.x+ 2, self.y + 2),
							  (self.x+4, self.y + 8),
							  (self.x+6,self.y+9),
							  (self.x+10, self.y+26),
							  (self.x+16, self.y+31),
							  (self.x+17, self.y+31),
							  (self.x+23, self.y+26),
							  (self.x+27, self.y+9),
							  (self.x+29, self.y+8),
							  (self.x+31, self.y+2),
							  (self.x+31, self.y)]
			
		if "playerref" in stuff:
			self.playerref = stuff["playerref"]
			
		if "blockable" in stuff:
			self.blockable = True
			
			
		if "deadly" in stuff:
			self.deadly = True
			self.sound = resources.vortex
			self.music.queue(self.sound)
			self.music.eos_action = self.music.EOS_LOOP
			
			self.vertices = [
			(self.x+4, self.y),
			(self.x+30, self.y+32),
			(self.x, self.y + 32),
			(self.x+30, self.y+32),
			
			(self.x+4, self.y + 64),
			(self.x+32, self.y+30),
			(self.x+32, self.y + 60),
			(self.x+32, self.y+30),
			
			(self.x + 60, self.y + 60),
			(self.x+34, self.y+32),
			(self.x + 64, self.y + 32),
			(self.x+34, self.y+32),
			
			(self.x + 60, self.y),
			(self.x+32, self.y+34),
			(self.x + 32, self.y),
			(self.x+32, self.y+34),
			]
			
		if "static" in stuff:
			self.static = True
		
		if "activatephase" in stuff:
			self.activatephase = stuff["activatephase"]
			if not self.activatephase == self.phase:
				self.visible = False
				
		if "deactivatephase" in stuff:
			self.deactivatephase = stuff["deactivatephase"]
			
		if "pedestal" in stuff:
			self.pedestal = True
			
		if "height" in stuff:
			self.h = stuff["height"]
		
		if "width" in stuff:
			self.w = stuff["width"]
			
		if "desound" in stuff:
			self.desound = stuff["desound"]
			
		if "pedestal" in stuff:
			self.vertices = [
			(self.x, self.y),
			(self.x, self.y + 2),
			(self.x+4, self.y+2),
			(self.x+4, self.y+32),
			(self.x-2, self.y+34),
			(self.x-2, self.y+36),
			(self.x+34, self.y+36),
			(self.x+34, self.y+34),
			(self.x+28, self.y+32),
			(self.x+28, self.y+2),
			(self.x+32, self.y+2),
			(self.x+32, self.y)
			]
	
	def add(self, artifact):
		if self.player:
			if self.item:
				artifact.visible = True
				artifact.held = False
				
			else:
				self.item = artifact
			
	
	def update(self, dt):
		if self.phase > self.deactivatephase or self.phase < self.activatephase:
			if self.music.playing:
				self.music.pause()
				
			if self.phase > self.deactivatephase:
				self.cleanup = True
			return 
		if self.phase == self.activatephase and self.visible == False and not self.held:
			self.visible = True
			
		if self.phase == self.deactivatephase and self.visible == True and not self.held:
			if self.desound:
				self.desound.volume = .6
				self.desound.play()
			self.visible = False
		self.life += dt
		if self.artifact:
			if not self.held and not self.placed:
				dist = math.fabs(self.x - self.playerref.x)
				if dist < 512:
					self.music.play()
					self.music.volume = 1.0 - dist / 512
					if dist < 128:
						if random.random() < .3:
							randh = random.randint(0, self.h)
							randw = random.randint(0, self.w)
							xd = self.x + randw - (self.playerref.x + self.playerref.w / 2)
							yd = self.y + randh - (self.playerref.y + self.playerref.h / 2)
						
							xs = 100
							if xd > 0:
								xs = -100
							elif xd == 0:
								xd = .1
							ys = xs * (yd / xd)
						
							self.particles.add(particle.Particle(randw + self.x, randh + self.y, xs, ys, type="aimed"))		
					if dist < 16:
						self.music.volume = 1.0
				else:
					if not self.music.volume == 0.0:
						self.music.volume = 0.0
				
			elif not self.placed:
				self.music.play()
				
		if self.pedestal:
			if random.random() < .2:
				self.particles.add(particle.Particle(random.randint(0, self.w) + self.x, self.y, 300, 40))		
				
		if self.particles and self.player:
			if random.random() < .4:
				self.particles.add(particle.Particle(random.randint(8, 23) + self.x, random.randint(16, 24) + self.y, 200, -15, player=True))		
				
		if self.static:
			if self.deadly:
				self.color = (1.0 - random.random() / 5, 0.0, 0.0, 0.8 - random.random() / 4)
				self.angle += dt * 100
			else:
				self.color = (1.0 - random.random() / 6, 1.0 - random.random() / 6, 1.0 - random.random() / 6, 1.0 - random.random() / 4)
			
			if self.artifact:
				self.xmod *= .90
				if self.xmod < 1 and self.xmod > -1:
					self.xmod = 0.0
					
				self.ymod *= .95
				if self.ymod < 1 and self.ymod > -1:
					self.ymod = 0.0
			else:
				self.xmod = 0.0
			return 
			
		self.x += self.sx * dt
		self.y += self.sy * dt
		
		if not self.xmod == 0.0:
			self.xmod *= .90
			if self.xmod < 1 and self.xmod > -1:
				self.xmod = 0.0
				
		if not self.ymod == 0.0:
			self.ymod *= .50
			if self.ymod < 1 and self.ymod > -1:
				self.ymod = 0.0
		
		if not self.sx == 0.0:
			self.sx *= .90
			if self.sx < 15 and self.sx > -15:
				self.sx = 0.0
			
		if not self.sy == 0.0:
			self.sy *= .95
			if self.sy < 15 and self.sy > -15:
				self.sy = 0.0
				
		if self.y > 100:
			self.sy -= 20.0
			self.energy -= 2.8 * dt
		else:
			self.y = 100
			self.sy = 0.0
			self.energy = 12.0
		
	def render(self):
		if not self.visible:
			return

		if self.phase > self.deactivatephase or self.phase < self.activatephase:
			return
			
		gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
		gl.glEnable(gl.GL_BLEND)
		if self.deadly:
			gl.glPushMatrix()
			
			
			
			for i in range(0, 2):
				randnum = (math.sin(self.angle / 4) + (random.random() / 10)) / 17
				gl.glTranslatef(self.x + self.w / 2, self.y + self.h / 2, 0.0)
				gl.glScalef(.7 - randnum, .7 - randnum, .7)
				gl.glRotatef(self.angle, 0.0, 0.0, 1.0)
				gl.glTranslatef(-(self.x + self.w / 2), -(self.y + self.h / 2), 0.0)
				gl.glBegin(gl.GL_QUADS)
				c = random.random() / 4.0
				
				gl.glColor4f(c, 0.0, 0.0, 1.0 - random.random() / 5)
				gl.glVertex2f(self.x - self.xmod, self.y)
				gl.glVertex2f(self.x+ self.w + self.xmod, self.y)
				gl.glVertex2f(self.x+ self.w + self.xmod, self.y +self.h)
				gl.glVertex2f(self.x - self.xmod, self.y +self.h)
				gl.glEnd()
				
			
			
			
			gl.glPopMatrix()
			gl.glPushMatrix()
			gl.glTranslatef(self.x + self.w / 2, self.y + self.h / 2, 0.0)
			randnum = (math.sin(self.angle / 4) + (random.random() / 10)) / 17
			gl.glScalef(1.0 - randnum, 1.0 - randnum, 1.0)
			gl.glRotatef(self.angle, 0.0, 1.0, 1.0)
			gl.glTranslatef(-(self.x + self.w / 2), -(self.y + self.h / 2), 0.0)
		
		if self.artifact and self.placed:
			
			gl.glBegin(gl.GL_QUADS)
			
			for i in range(0,3):
				c = random.random() / 4.0
				color = (.7 - c, .7 - c, .7 - c, random.random())
				h = random.randint(1, 40)
				w = random.randint(1, 10)
				gl.glColor4f(*color)
				gl.glVertex2f(self.x + w / 2 + self.w / 4, self.y + 28)
				gl.glVertex2f(self.x + self.w / 2 + self.w / 4 - w / 2, self.y + 28)
				gl.glVertex2f(self.x + self.w / 2 + self.w / 4 - w / 2, self.y + self.h + h + 64 + 28 + self.ymod)
				gl.glVertex2f(self.x + w / 2 + self.w / 4, self.y + self.h + h + 64 + 28 + self.ymod)
				
			gl.glEnd()
			
		if self.blockable and self.static and not self.deadly:
			gl.glBegin(gl.GL_QUADS)
		else:
			gl.glBegin(gl.GL_LINE_LOOP)
		
		if self.artifact or self.pedestal or self.deadly or self.player:
			v = 0
			for vert in self.vertices:
				v += 1
				c = math.fabs(math.sin(self.life + v))
				if self.deadly:
					gl.glColor4f(c, 0.0, 0.0, 1.0 - random.random() / 5)
				elif self.player:
					gl.glColor4f(.35, .35, 1.0 - c / 1.5, 1.0 - random.random() / 5)
				else:
					gl.glColor4f(c, c, c, 1.0 - random.random() / 5)	
				if self.player:
					gl.glVertex2f(self.x + vert[0], self.y + vert[1])
				else:
					gl.glVertex2f(vert[0], vert[1])
		else:
			gl.glColor4f(*self.color)
			gl.glVertex2f(self.x - self.xmod, self.y)
			gl.glVertex2f(self.x+ self.w + self.xmod, self.y)
			gl.glVertex2f(self.x+ self.w + self.xmod, self.y +self.h)
			gl.glVertex2f(self.x - self.xmod, self.y +self.h)
		gl.glEnd()
		if self.deadly:
			gl.glPopMatrix()
			
		gl.glDisable(gl.GL_BLEND)