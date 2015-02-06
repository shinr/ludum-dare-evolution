import pyglet
import thing
import worldtree
from pyglet import gl
import particlemanager
import resources
import math
import sys


class Game(pyglet.window.Window):
	def __init__(self):
		pyglet.window.Window.__init__(self, 640, 480)
		
		self.particles = particlemanager.ParticleManager()
		self.start = (2320, 240)
		self.fadein = True
		self.things = [thing.Thing(self.start[0], self.start[1], player=True, particles=self.particles)]
		
		self.namething = pyglet.text.Label(text="the world tree", x=320, y=400, font_name="Courier New", font_size=12, color=(0, 0, 0, 255))
		self.tutorial = 0
		self.tutorial_texts = [
			pyglet.text.Label(text="follow the sound and press down to pick the artifact up", x=60, y=400, font_name="Courier New", font_size=8),
			pyglet.text.Label(text="press down to place the artifact on a pedestal", x=60, y=400, font_name="Courier New", font_size=8),
			pyglet.text.Label(text="click the pedestal to activate the artifact", x=60, y=400, font_name="Courier New", font_size=8),
			pyglet.text.Label(text="use up to float upwards for a short while.  find all artifacts and evolve the world tree.  watch out for dangers in this evolving wilderness", x=60, y=400, font_name="Courier New", font_size=8, multiline=True, width=520)
		]
		self.fadeinl = [1.0, 1.0, 1.0, 1.0]
		self.fadeout = [1.0, 1.0, 1.0, 0.0]
		self.actives = []	
		self.lock = True
		self.sounds = [resources.artifact_1, resources.artifact_2, resources.artifact_3, resources.artifact_4, resources.artifact_5, resources.artifact_6 ]
		self.particles.player = self.things[0]
		self.things.append(worldtree.WorldTree(self.particles, self.things[0]))
		
		self.worldtree = self.things[-1]

		#level 1
		self.things += [thing.Thing(2000, 100, static=True, blockable=True, width=40, height=250, activatephase=1,desound=resources.obstacle_down, deactivatephase=2),
						thing.Thing(1700, 220, static=True, blockable=True, width=100, height=20, activatephase=1, deactivatephase=2),
						thing.Thing(1500, 400, static=True, blockable=True, width=100, height=20, activatephase=1, deactivatephase=2),
						thing.Thing(1300, 100, static=True, blockable=True, width=200, height=200, activatephase=1, deactivatephase=2),
						thing.Thing(1400, 330, artifact=True, static=True, sound=resources.artifact_2, playerref=self.things[0], particlemanager=self.particles),
						
						]
		#level 2
		self.things += [thing.Thing(2600, 100, static=True, blockable=True, width=40, height=200, activatephase=2,desound=resources.obstacle_down, deactivatephase=3),
						thing.Thing(2800, 100, static=True, blockable=True, width=100, height=100, activatephase=2, deactivatephase=3),
						thing.Thing(2900, 200, static=True, blockable=True, width=100, height=100, activatephase=2, deactivatephase=3),
						thing.Thing(3000, 300, static=True, blockable=True, width=100, height=100, activatephase=2, deactivatephase=3),
						thing.Thing(3100, 380, static=True, blockable=True, width=200, height=20, activatephase=2, deactivatephase=3),
						thing.Thing(3300, 100, static=True, blockable=True, width=20, height=300, activatephase=2, deactivatephase=3),
						thing.Thing(3400, 200, static=True, blockable=True, width=60, height=10, activatephase=2, deactivatephase=3),
						thing.Thing(3470, 300, static=True, blockable=True, width=60, height=10, activatephase=2, deactivatephase=3),
						thing.Thing(3400, 150, static=True, blockable=True, width=10, height=300, activatephase=2, deactivatephase=3),
						thing.Thing(3530, 100, static=True, blockable=True, width=10, height=300, activatephase=2, deactivatephase=3),
						thing.Thing(3730, 100, static=True, blockable=True, width=80, height=150, activatephase=2, deactivatephase=3),
						thing.Thing(2400, 450, static=True, blockable=True, width=1200, height=10, activatephase=2, deactivatephase=3),
						
						thing.Thing(3666, 130, artifact=True, static=True, sound=resources.artifact_3, playerref=self.things[0], particlemanager=self.particles,activatephase=2),
						
						]
		#level 3
		self.things += [thing.Thing(2000, 100, static=True, blockable=True, width=40, height=250, activatephase=3,desound=resources.obstacle_down, deactivatephase=4),
						thing.Thing(1700, 220, static=True, blockable=True, width=100, height=20, activatephase=3, deactivatephase=4),
						thing.Thing(1500, 400, static=True, blockable=True, width=100, height=20, activatephase=3, deactivatephase=4),
						thing.Thing(1300, 100, static=True, blockable=True, width=200, height=200, activatephase=3, deactivatephase=4),
						thing.Thing(1400, 330, artifact=True, static=True, sound=resources.artifact_4, playerref=self.things[0], particlemanager=self.particles, activatephase=3),
						thing.Thing(1940, 150, static=True, blockable=True, width=64, height=64, deadly=True, activatephase=3, deactivatephase=4),
						thing.Thing(1880, 150, static=True, blockable=True, width=64, height=64, deadly=True, activatephase=3, deactivatephase=4),
						thing.Thing(1820, 150, static=True, blockable=True, width=64, height=64, deadly=True, activatephase=3, deactivatephase=4),
						thing.Thing(1760, 150, static=True, blockable=True, width=64, height=64, deadly=True, activatephase=3, deactivatephase=4),
						thing.Thing(1700, 150, static=True, blockable=True, width=64, height=64, deadly=True, activatephase=3, deactivatephase=4),
						thing.Thing(1640, 150, static=True, blockable=True, width=64, height=64, deadly=True, activatephase=3, deactivatephase=4),
						thing.Thing(1580, 150, static=True, blockable=True, width=64, height=64, deadly=True, activatephase=3, deactivatephase=4),
						thing.Thing(1520, 150, static=True, blockable=True, width=64, height=64, deadly=True, activatephase=3, deactivatephase=4),
						thing.Thing(1460, 150, static=True, blockable=True, width=64, height=64, deadly=True, activatephase=3, deactivatephase=4),
						thing.Thing(1400, 150, static=True, blockable=True, width=64, height=64, deadly=True, activatephase=3, deactivatephase=4)
						]
		#level 4
		self.things += [thing.Thing(2600, 100, static=True, blockable=True, width=50, height=100, activatephase=4,desound=resources.obstacle_down, deactivatephase=5),
						thing.Thing(2650, 200, static=True, blockable=True, width=50, height=100, activatephase=4, deactivatephase=5),
						thing.Thing(2700, 300, static=True, blockable=True, width=50, height=100, activatephase=4, deactivatephase=5),
						thing.Thing(3000, 200, static=True, blockable=True, width=100, height=250, activatephase=4, deactivatephase=5),
						thing.Thing(2950, 100, static=True, blockable=True, width=250, height=20, activatephase=4, deactivatephase=5),
						thing.Thing(3300, 100, static=True, blockable=True, width=20, height=300, activatephase=4, deactivatephase=5),
						thing.Thing(3400, 200, static=True, blockable=True, width=60, height=10, activatephase=4, deactivatephase=5),
						thing.Thing(3170, 300, static=True, blockable=True, width=60, height=10, activatephase=4, deactivatephase=5),
						thing.Thing(3400, 150, static=True, blockable=True, width=10, height=300, activatephase=4, deactivatephase=5),
						thing.Thing(3530, 100, static=True, blockable=True, width=10, height=300, activatephase=4, deactivatephase=5),
						thing.Thing(3730, 100, static=True, blockable=True, width=80, height=150, activatephase=4, deactivatephase=5),
						thing.Thing(2400, 450, static=True, blockable=True, width=1200, height=10, activatephase=4, deactivatephase=5),
						
						thing.Thing(3650, 150, artifact=True, static=True, sound=resources.artifact_5, playerref=self.things[0], particlemanager=self.particles,activatephase=4),
						thing.Thing(2700, 250, static=True, blockable=True, width=64, height=64, deadly=True, activatephase=4, deactivatephase=5),
						thing.Thing(2750, 200, static=True, blockable=True, width=64, height=64, deadly=True, activatephase=4, deactivatephase=5),
						thing.Thing(2800, 150, static=True, blockable=True, width=64, height=64, deadly=True, activatephase=4, deactivatephase=5),
						thing.Thing(2850, 100, static=True, blockable=True, width=64, height=64, deadly=True, activatephase=4, deactivatephase=5),
						thing.Thing(2800, 400, static=True, blockable=True, width=64, height=64, deadly=True, activatephase=4, deactivatephase=5),
						thing.Thing(2850, 350, static=True, blockable=True, width=64, height=64, deadly=True, activatephase=4, deactivatephase=5),
						thing.Thing(2900, 300, static=True, blockable=True, width=64, height=64, deadly=True, activatephase=4, deactivatephase=5),
						thing.Thing(2950, 250, static=True, blockable=True, width=64, height=64, deadly=True, activatephase=4, deactivatephase=5),
						thing.Thing(2900, 100, static=True, blockable=True, width=64, height=64, deadly=True, activatephase=4, deactivatephase=5)
						]
		#level 5
		self.things += [thing.Thing(2000, 100, static=True, blockable=True, width=60, height=250, activatephase=5,desound=resources.obstacle_down, deactivatephase=6),
						thing.Thing(1700, 100, static=True, blockable=True, width=60, height=200, activatephase=5, deactivatephase=6),
						thing.Thing(1500, 100, static=True, blockable=True, width=60, height=150, activatephase=5, deactivatephase=6),
						thing.Thing(1300, 100, static=True, blockable=True, width=60, height=200, activatephase=5, deactivatephase=6),
						thing.Thing(1200, 130, artifact=True, static=True, sound=resources.artifact_6, playerref=self.things[0], particlemanager=self.particles, activatephase=5),
						thing.Thing(1940, 300, static=True, blockable=True, width=64, height=64, deadly=True, activatephase=5, deactivatephase=6),
						thing.Thing(1880, 300, static=True, blockable=True, width=64, height=64, deadly=True, activatephase=5, deactivatephase=6),
						thing.Thing(1820, 300, static=True, blockable=True, width=64, height=64, deadly=True, activatephase=5, deactivatephase=6),
						thing.Thing(1760, 300, static=True, blockable=True, width=64, height=64, deadly=True, activatephase=5, deactivatephase=6),
						thing.Thing(1340, 250, static=True, blockable=True, width=64, height=64, deadly=True, activatephase=5, deactivatephase=6),
						thing.Thing(1640, 250, static=True, blockable=True, width=64, height=64, deadly=True, activatephase=5, deactivatephase=6),
						thing.Thing(1580, 250, static=True, blockable=True, width=64, height=64, deadly=True, activatephase=5, deactivatephase=6),
						thing.Thing(1220, 250, static=True, blockable=True, width=64, height=64, deadly=True, activatephase=5, deactivatephase=6),
						thing.Thing(1460, 200, static=True, blockable=True, width=64, height=64, deadly=True, activatephase=5, deactivatephase=6),
						thing.Thing(1400, 200, static=True, blockable=True, width=64, height=64, deadly=True, activatephase=5, deactivatephase=6)
						]
		
		self.things += [thing.Thing(2650, 110, artifact=True, static=True, sound=resources.artifact_1, playerref=self.things[0], particlemanager=self.particles),
					
					thing.Thing(2100, 100, static=True, pedestal=True, particles=self.particles, height=10, width=24, playerref=self.things[0]),
					thing.Thing(2164, 100, static=True, pedestal=True, particles=self.particles, height=10, width=24, playerref=self.things[0]),
					thing.Thing(2228, 100, static=True, pedestal=True, particles=self.particles, height=10, width=24, playerref=self.things[0]),
					thing.Thing(2376, 100, static=True, pedestal=True, particles=self.particles, height=10, width=24, playerref=self.things[0]),
					thing.Thing(2440, 100, static=True, pedestal=True, particles=self.particles, height=10, width=24, playerref=self.things[0]),
					thing.Thing(2504, 100, static=True, pedestal=True, particles=self.particles, height=10, width=24, playerref=self.things[0])]
		# thing 0 is player
		self.keys = []
		
		self.phases = []
		
		self.camera = [0, 0]
		
		self.init = False
		
	def play_sound(self, dt, id):
		self.sounds[id].play()
		
		pyglet.clock.schedule_once(self.play_sound, 8, id)
	
	def aabb(self, thing, player): # this is kinda bad way to do this, I'm finding
		if thing.deadly:
			distx = math.fabs(player.x - (thing.x + thing.w / 2)) 
			disty = math.fabs(player.y + player.h - (thing.y + thing.h / 2))
			
			dist = distx / 2 + disty / 2
			
			if dist < 128:
				vol = 1.0 - dist / 128
				if dist < 48:
					vol = 1.0
				thing.music.volume = vol
				if not thing.music.playing:
					thing.music.seek(0)
					thing.music.play()
			else:
				if thing.music.volume > 0.0:
					thing.music.volume = 0.0
			
			
		if player.x <= thing.x + thing.w and player.x + player.w >= thing.x:
			if player.y <= thing.y + thing.h and player.y + player.h >= thing.y:
				if thing.deadly: # vortexes
					
					
					if distx < 24.0 and disty < 24.0:
				
						if player.item:
							player.item.held = False
							player.item.visible = True
							player.item = None
						player.x = self.start[0]
						player.y = self.start[1]
						
					else:
						maxdistx = thing.w
						maxdisty = thing.h
						
						if player.x > thing.x + thing.w / 2:
							player.x -= 3 - (distx / maxdistx) * 2
						else:	
							player.x += 3 - (distx / maxdistx) * 2
							
						if player.y > thing.y + thing.h / 2:
							player.y -= 3 - (disty / maxdisty) * 2
						else:	
							player.y += 3 - (disty / maxdisty) * 2
						
					
					return
				
				transleft = player.x + player.w - thing.x
				transright = thing.x + thing.w - player.x
				transup = thing.y + thing.h - player.y
				transdown = player.y + player.h - thing.y
				
				translist = [transleft, transright, transup, transdown]
				
				mintrans = min(translist)
				
				attrb = translist.index(mintrans)
				
				if attrb == 0:
					player.x -= mintrans
				elif attrb == 1:
					player.x += mintrans
				elif attrb == 2:
					player.y += mintrans
					player.energy = 12
				else:
					player.y -= mintrans
					
					
				
				
	def updatephase(self):
		for thing in self.things:
			thing.phase += 1
			
		toremove = [item for item in self.things if item.cleanup == True]
		for kill in toremove:
			self.things.remove(kill)
	
	def fadeinn(self, dt):
		self.fadeinl[3] -= .02
		if self.fadeinl[3] <= .02:
			self.fadein = False
			return
		pyglet.clock.schedule_once(self.fadeinn, .1)	
	def fade(self, dt):
		self.fadeout[3] += .02
		pyglet.clock.schedule_once(self.fade, .5)
	
	def update(self, dt):
		if not self.init:
			pyglet.clock.schedule_once(self.fadeinn, .1)
			self.init = True
		
		if self.fadein == False:
			self.lock = False
			self.fadein = None
	
		if self.fadeout[3] >= .9999:
			pyglet.app.exit()
			sys.exit()
	
		if len(self.actives) == 6 and not self.lock:
			self.worldtree.energy += 300
			self.worldtree.energymultiplier = 100
			self.lock = True
			pyglet.clock.schedule_once(self.play_sound, 1, 0)
			pyglet.clock.schedule_once(self.play_sound, 2, 1)
			pyglet.clock.schedule_once(self.play_sound, 3, 2)
			pyglet.clock.schedule_once(self.play_sound, 4, 3)
			pyglet.clock.schedule_once(self.play_sound, 5, 4)
			pyglet.clock.schedule_once(self.play_sound, 6, 5)
			self.things[0].x, self.things[0].y = 2320, 150
			pyglet.clock.schedule_once(self.fade, 12)
			
		for thing in self.things:
			thing.update(dt)
		
		if not self.lock:
			if pyglet.window.key.LEFT in self.keys:
				self.things[0].sx = -100.0
			elif pyglet.window.key.RIGHT in self.keys:	
				self.things[0].sx = 100.0
				
		if pyglet.window.key.ESCAPE in self.keys:
			pyglet.app.exit()
			sys.exit()
			
		if not self.lock:
			if pyglet.window.key.UP in self.keys:
				if self.tutorial == 3:
					self.tutorial += 1
				self.things[0].sy = 10.0 * self.things[0].energy
			
		
						
		for item in [obj for obj in self.things if obj.blockable is True and obj.visible is True]:
			self.aabb(item, self.things[0])
		
		self.particles.update(dt)
		
	def on_draw(self): # all the rendering uses immediate mode which might not be optimal except for the
		self.clear()	# fact that it's simple.  so if you stumbled upon this piece of code, it's not
		gl.glEnable(gl.GL_COLOR_MATERIAL) # optimal.
		gl.glLoadIdentity()
		gl.glPushMatrix()
		gl.glTranslatef(-self.camera[0], self.camera[1], 0.0)
		
		self.camera[0] = self.things[0].x - 320
		
		for thing in self.things[1:]:
			thing.render()
			
		self.things[0].render()	
		self.particles.render()
		gl.glPopMatrix()
		gl.glColor3f(0.05, 0.05, 0.05)
		gl.glBegin(gl.GL_QUADS)
		gl.glVertex2f(0.0, 100.0)
		gl.glVertex2f(640.0, 100.0)
		gl.glVertex2f(640.0, 0.0)
		gl.glVertex2f(0.0, 0.0)
		gl.glEnd()
		if self.fadeout[3] > 0:
			gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
			gl.glEnable(gl.GL_BLEND)
			gl.glColor4f(*self.fadeout)
			gl.glBegin(gl.GL_QUADS)
			gl.glVertex2f(0.0, 0.0)
			gl.glVertex2f(640.0, 0.0)
			gl.glVertex2f(640.0, 480.0)
			gl.glVertex2f(0.0, 480.0)
			gl.glEnd()
			gl.glDisable(gl.GL_BLEND)
		elif self.fadein:
			gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
			gl.glEnable(gl.GL_BLEND)
			gl.glColor4f(*self.fadeinl)
			gl.glBegin(gl.GL_QUADS)
			gl.glVertex2f(0.0, 0.0)
			gl.glVertex2f(640.0, 0.0)
			gl.glVertex2f(640.0, 480.0)
			gl.glVertex2f(0.0, 480.0)
			gl.glEnd()
			gl.glDisable(gl.GL_BLEND)
		
		
		
		gl.glDisable(gl.GL_COLOR_MATERIAL) 
		
		if self.tutorial < 4 and not self.fadein:
			
			self.tutorial_texts[self.tutorial].draw()
		elif self.fadein:
			self.namething.draw()
		
	def on_key_press(self, button, modifiers):
		if self.lock:
			return 
			
		#if button == pyglet.window.key.E: #cheat
		#	self.updatephase()
		#	self.actives += 1
			
		elif button == pyglet.window.key.DOWN:
			if self.things[0].item:
				for item in [obj for obj in self.things if obj.pedestal is True and obj.visible is True]:
					if item.x < self.things[0].x + self.things[0].w and item.x + item.w > self.things[0].x:
						xd = self.things[0].item.vertices[0][0] - item.x
						yd = self.things[0].item.vertices[0][1] - item.y
						self.things[0].item.vertices = [(vrt[0] - xd, vrt[1] - yd + 42) for vrt in self.things[0].item.vertices]
						
						self.things[0].item.held = False
						self.things[0].item.visible = True
						self.things[0].item.x = item.x
						self.things[0].item.y = item.y + 8
						self.things[0].item.placed = True
						self.worldtree.energymultiplier += 1
						self.things[0].item.music.eos_action = self.things[0].item.music.EOS_PAUSE
						self.things[0].item = None
						resources.pick.play()
						if self.tutorial == 1:
							self.tutorial += 1
						
						if not item in self.phases:
							self.updatephase()
							self.phases.append(item)
						
			else:
				for item in [obj for obj in self.things if obj.artifact is True and obj.visible is True]:
					if item.x < self.things[0].x + self.things[0].w and item.x + item.w > self.things[0].x:
						if not item.placed:
							resources.pick2.play()
							item.placed = False
							item.visible = False
							item.held = True
							self.things[0].add(item)
							
							if self.tutorial == 0:
								self.tutorial += 1
						
		else:
			if not button in self.keys:
				self.keys.append(button)
	
	def on_key_release(self, button, modifiers):
		if self.lock:
			return
		while button in self.keys:
			self.keys.remove(button)
	def minus_one(self, dt, item):
		if item in self.actives:
			self.actives.remove(item)
		
	def on_mouse_press(self, x, y, button, modifiers):
		if self.lock:
			return
		for thang in self.things:
			if thang.x + thang.w > x + self.camera[0] and thang.x - thang.w < x + self.camera[0]: 
				if thang.y + thang.h > y and thang.y - thang.h < y:
					thang.xmod = 16.0
					if thang.artifact and thang.placed:
						pyglet.clock.schedule_once(self.minus_one, 5, thang)
						if not thang in self.actives:
							self.actives.append(thang)
						thang.music.seek(0)
						thang.music.play()
						thang.ymod = 256.0
						if self.tutorial == 2:
							self.tutorial += 1
						
		
game = Game()
if __name__ == '__main__':
	pyglet.clock.schedule_interval(game.update, 1/120.0)
	pyglet.app.run()