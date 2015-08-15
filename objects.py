import pi3d
from random import random
FLASHTIME = 0.5 # in seconds
	
class WireObject(pi3d.Shape):
	def __init__(self, verts, ends, camera=None, light=None, name='', w=1.0, h=1.0, d=1.0, t2=0.1,
		x=0.0, y=0.0, z=0.0,
		rx=0.0, ry=0.0, rz=0.0,
		sx=1.0, sy=1.0, sz=1.0,
		cx=0.0, cy=0.0, cz=0.0):
		
		super(WireObject, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
			sx, sy, sz, cx, cy, cz)

		uvs = [(0, 0) for i in range(len(verts))]
		norms = [(0, 0, 1) for i in range(len(verts))]
		inds = []
		endbuffer = []
		def appendToBuffer(b, a):
			b.append(a)
			if len(b) == 3:
				inds.append(b)
				b = []
			return b
		def closeBuffer(b):
			if len(b):
				while len(b) != 3:
					b.append(b[0])
				inds.append(b)
		for e in ends:
			endbuffer = appendToBuffer(endbuffer, e[0])
			endbuffer = appendToBuffer(endbuffer, e[1])
		closeBuffer(endbuffer)
		buff = pi3d.Buffer(self, verts, uvs, inds, norms)
		buff.set_material((0.0, 1.0, 0.0))
		self.buf.append(buff)
		self.set_line_width(3.0, False)
		buff.draw_method = pi3d.GL_LINES
		shader = pi3d.Shader('mat_flat')
		self.set_draw_details(shader, [])
		self.set_fog((0, 0, 0, 1), 30000)

class SolidObject(pi3d.Shape):
	def __init__(self, verts, inds, camera=None, light=None, name='', w=1.0, h=1.0, d=1.0,
		x=0.0, y=0.0, z=0.0,
		rx=0.0, ry=0.0, rz=0.0,
		sx=1.0, sy=1.0, sz=1.0,
		cx=0.0, cy=0.0, cz=0.0):
		
		super(SolidObject, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
			sx, sy, sz, cx, cy, cz)

		uvs = [(0, 0) for i in range(len(verts))]
		norms = [(0, 0, 1) for i in range(len(verts))]

		buff = pi3d.Buffer(self, verts, uvs, inds) # let pi3d compute normals
		buff.set_material((0.0, 0.0, 0.0))
		self.buf.append(buff)
		self.set_fog((0, 0, 0, 1), 30000)

class Tank(pi3d.Shape):
	def __init__(self, camera=None, light=None, name='', w=1.0, h=1.0, d=1.0,
		x=0.0, y=0.0, z=0.0,
		rx=0.0, ry=0.0, rz=0.0,
		sx=1.0, sy=1.0, sz=1.0,
		cx=0.0, cy=0.0, cz=0.0):

		super(Tank, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
			sx, sy, sz, cx, cy, cz)

		vs = (
			(100, -50, 0),		# rf0
			(100, 50, 0),		# lf0
			(-100, 50, 0),		# lb0
			(-100, -50, 0),		# rb0
			(115, -65, -20),	# rf1
			(115, 65, -20),		# lf1
			(-115, 65, -20),	# lb1
			(-115, -65, -20),	# rb1
			(50, -30, -40),		# rf2
			(50, 30, -40),		# lf2
			(-90, 30, -40),		# lb2
			(-90, -30, -40),	# rb2
			(-60, -15, -75),	# r3
			(-60, 15, -75),		# l3
			(90, -5, -55),		# grf0
			(90, 5, -55),		# glf0
			(5, 5, -55),		# glb0
			(5, -5, -55),		# grb0
			(90, -5, -65),		# grf1
			(90, 5, -65),		# glf1
			(-25, 5, -65),		# glb1
			(-25, -5, -65)		# grb1
		)
		ends = (
			(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6),
			(6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7),
			(8, 9), (9, 10), (10, 11), (11, 8), (8, 4), (9, 5),
			(10, 6), (11, 7), (12, 13), (12, 8), (12, 11), (13, 9),
			(13, 10), (14, 15), (15, 16), (16, 17), (17, 14), (18, 19),
			(19, 20), (20, 21), (21, 18), (14, 18), (15, 19), (16, 20), (17, 21)
		)
		rf0 = 0
		lf0 = 1
		lb0 = 2
		rb0 = 3
		rf1 = 4
		lf1 = 5
		lb1 = 6
		rb1 = 7
		rf2 = 8
		lf2 = 9
		lb2 = 10
		rb2 = 11
		r3 = 12
		l3 = 13
		grf0 = 14
		glf0 = 15
		glb0 = 16
		grb0 = 17
		grf1 = 18
		glf1 = 19
		glb1 = 20
		grb1 = 21
		inds = (
			(rf0, lf0, lb0), (rb0, rf0, lb0), # we don't really NEED the bottom face
			(lf0, lf1, lb0), (lb0, lf1, lb1),
			(rf0, rf1, lf0), (lf0, rf1, lf1),
			(rb0, rb1, rf0), (rf0, rb1, rf1),
			(lb0, lb1, rb0), (rb0, lb1, rb1),
			(lf1, lf2, lb1), (lb1, lf2, lb2),
			(rf1, rf2, lf1), (lf1, rf2, lf2),
			(rb1, rb2, rf1), (rf1, rb2, rf2),
			(lb1, lb2, rb1), (rb1, lb2, rb2),
			(rf2, r3, lf2), (lf2, r3, l3),
			(rf2, rb2, r3),
			(l3, lb2, lf2),
			(rb2, lb2, r3), (r3, lb2, l3),
			(grf0, glf0, glb0), (grb0, grf0, glb0), # we don't really NEED the bottom face of the gun
			(glf0, glf1, glb0), (glb0, glf1, glb1),
			(grf0, grf1, glf0), (glf0, grf1, glf1),
			(grf0, grb0, grf1), (grf1, grb0, grb1),
			(grf1, glb1, glf1), (grf1, grb1, glb1)
		)
		self.so = SolidObject(vs, inds)
		self.wo = WireObject(vs, ends)
		self.add_child(self.wo)
		shader = pi3d.Shader('mat_flat')
		self.set_draw_details(shader, [])

		self.t = 0	# -1 => dead; 0 => alive; +ve => flashing
		self.a = 0.0
		self.reloadtime = 0 # 0 => can fire; +ve => reloading/can't fire
		
	def tick(self, dt):
		if self.t > 0:
			self.so.set_material((random(), random(), random()))
			self.t -= dt
			if self.t <= 0:
				self.t = 0
				self.so.set_material((0.0, 0.0, 0.0))
		if self.reloadtime > 0:
			self.reloadtime -= dt
			if self.reloadtime <= 0:
				self.reloadtime = 0

	def hitTest(self, x, y):
		r = 35
		return abs(self.x() - x) < r and abs(self.y() - y) < r
			
	def hit(self):
		self.t = FLASHTIME
		
	def draw(self, f):
		self.rotateToZ(90.0 + self.a)
		self.children[0] = self.so if f else self.wo
		self.MFlg = True
		super(Tank, self).draw()

class Cube(pi3d.Shape):
	def __init__(self, camera=None, light=None, name='', w=1.0, h=1.0, d=1.0,
		x=0.0, y=0.0, z=0.0,
		rx=0.0, ry=0.0, rz=0.0,
		sx=1.0, sy=1.0, sz=1.0,
		cx=0.0, cy=0.0, cz=0.0):
		
		super(Cube, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
			sx, sy, sz, cx, cy, cz)

		vs = (
			( 50, -50, 0),		# se0
			( 50,  50, 0),		# ne0
			(-50,  50, 0),		# nw0
			(-50, -50, 0),		# sw0
			( 50, -50, -120),	# se2
			( 50,  50, -120),	# ne2
			(-50,  50, -120),	# nw2
			(-50, -50, -120),	# sw2
		)
		ends = (
			(0, 1), (1, 2), (2, 3), (3, 0),
			(4, 5), (5, 6), (6, 7), (7, 4),
			(0, 4), (1, 5), (2, 6), (3, 7)
		)
		inds = (
			(0, 4, 1), (1, 4, 5),
			(1, 5, 2), (2, 5, 6),
			(2, 6, 3), (3, 6, 7),
			(3, 7, 0), (0, 7, 4),
			(5, 4, 6), (6, 4, 7)	# top
		)
		self.so = SolidObject(vs, inds)
		self.wo = WireObject(vs, ends)
		self.add_child(self.wo)
		shader = pi3d.Shader('mat_flat')
		self.set_draw_details(shader, [])

		self.t = 0	# 0 => normal; +ve => flashing
		
	def tick(self, dt):
		if self.t > 0:
			self.so.set_material((random(), random(), random()))
			self.t -= dt
			if self.t <= 0:
				self.t = 0
				self.so.set_material((0.0, 0.0, 0.0))

	def hitTest(self, x, y):
		r = 50
		return abs(self.x() - x) < r and abs(self.y() - y) < r
			
	def hit(self):
		self.t = FLASHTIME
		
	def draw(self, f):
		self.children[0] = self.so if f else self.wo
		self.MFlg = True
		super(Cube, self).draw()

	def drawIfHit(self, f):
		if self.t:
			self.scale(1.05, 1.05, 1.05)
			self.children[0] = self.so if f else self.wo
			self.MFlg = True
			super(Cube, self).draw()
		
class HalfCube(pi3d.Shape):
	def __init__(self, camera=None, light=None, name='', w=1.0, h=1.0, d=1.0,
		x=0.0, y=0.0, z=0.0,
		rx=0.0, ry=0.0, rz=0.0,
		sx=1.0, sy=1.0, sz=1.0,
		cx=0.0, cy=0.0, cz=0.0):
		
		super(HalfCube, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
			sx, sy, sz, cx, cy, cz)

		vs = (
			( 50, -50, 0),		# se0
			( 50,  50, 0),		# ne0
			(-50,  50, 0),		# nw0
			(-50, -50, 0),		# sw0
			( 50, -50, -55),	# se1
			( 50,  50, -55),	# ne1
			(-50,  50, -55),	# nw1
			(-50, -50, -55)		# sw1
		)
		ends = (
			(0, 1), (1, 2), (2, 3), (3, 0),
			(4, 5), (5, 6), (6, 7), (7, 4),
			(0, 4), (1, 5), (2, 6), (3, 7)
		)
		inds = (
			(0, 4, 1), (1, 4, 5),
			(1, 5, 2), (2, 5, 6),
			(2, 6, 3), (3, 6, 7),
			(3, 7, 0), (0, 7, 4),
			(5, 4, 6), (6, 4, 7)	# top
		)
		self.so = SolidObject(vs, inds)
		self.wo = WireObject(vs, ends)
		self.add_child(self.wo)
		shader = pi3d.Shader('mat_flat')
		self.set_draw_details(shader, [])

		self.t = 0	# 0 => normal; +ve => flashing
		
	def tick(self, dt):
		if self.t > 0:
			self.so.set_material((random(), random(), random()))
			self.t -= dt
			if self.t <= 0:
				self.t = 0
				self.so.set_material((0.0, 0.0, 0.0))

	def hitTest(self, x, y):
		return False
		
	def hit(self):
		self.t = FLASHTIME
		
	def draw(self, f):
		self.children[0] = self.so if f else self.wo
		self.MFlg = True
		super(HalfCube, self).draw()

	def drawIfHit(self, f):
		if self.t:
			self.scale(1.05, 1.05, 1.05)
			self.children[0] = self.so if f else self.wo
			self.MFlg = True
			super(HalfCube, self).draw()
		
class Pyramid(pi3d.Shape):
	def __init__(self, camera=None, light=None, name='', w=1.0, h=1.0, d=1.0,
		x=0.0, y=0.0, z=0.0,
		rx=0.0, ry=0.0, rz=0.0,
		sx=1.0, sy=1.0, sz=1.0,
		cx=0.0, cy=0.0, cz=0.0):
		
		super(Pyramid, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
			sx, sy, sz, cx, cy, cz)

		vs = (
			( 50, -50, 0),		# se0
			( 50,  50, 0),		# ne0
			(-50,  50, 0),		# nw0
			(-50, -50, 0),		# sw0
			(  0,   0, -120)	# top
		)
		ends = (
			(0, 1), (1, 2), (2, 3), (3, 0),
			(0, 4), (1, 4), (2, 4), (3, 4)
		)
		inds = (
			(4, 1, 0), (4, 2, 1), (4, 3, 2), (4, 0, 3),
		)
		self.so = SolidObject(vs, inds)
		self.wo = WireObject(vs, ends)
		self.add_child(self.wo)
		shader = pi3d.Shader('mat_flat')
		self.set_draw_details(shader, [])

		self.t = 0	# 0 => normal; +ve => flashing
		
	def tick(self, dt):
		if self.t > 0:
			self.so.set_material((random(), random(), random()))
			self.t -= dt
			if self.t <= 0:
				self.t = 0
				self.so.set_material((0.0, 0.0, 0.0))

	def hitTest(self, x, y):
		r = 25
		return abs(self.x() - x) < r and abs(self.y() - y) < r
			
	def hit(self):
		self.t = FLASHTIME
		
	def draw(self, f):
		self.children[0] = self.so if f else self.wo
		self.MFlg = True
		super(Pyramid, self).draw()

	def drawIfHit(self, f):
		if self.t:
			self.scale(1.05, 1.05, 1.05)
			self.children[0] = self.so if f else self.wo
			self.MFlg = True
			super(Pyramid, self).draw()
		
class Bullet(pi3d.Shape):
	def __init__(self, camera=None, light=None, name='', w=1.0, h=1.0, d=1.0,
		x=0.0, y=0.0, z=0.0,
		rx=0.0, ry=0.0, rz=0.0,
		sx=1.0, sy=1.0, sz=1.0,
		cx=0.0, cy=0.0, cz=0.0):
		
		super(Bullet, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
			sx, sy, sz, cx, cy, cz)

		vs = (
			(-10, 5, -55),		# l0
			(-10, 5, -65),		# l1
			(-10,-5, -65),		# r1
			(-10,-5, -55),		# r0
			( 10, 0, -60)		# front
		)
		ends = (
			(0, 1), (1, 2), (2, 3), (3, 0),
			(0, 4), (1, 4), (2, 4), (3, 4)
		)
		inds = (
			(4, 1, 0), (4, 2, 1), (4, 3, 2), (4, 0, 3),
			(1, 2, 0), (0, 2, 3)
		)
		self.so = SolidObject(vs, inds)
		self.wo = WireObject(vs, ends)
		self.add_child(self.wo)
		shader = pi3d.Shader('mat_flat')
		self.set_draw_details(shader, [])

		self.t = 0	# 0 => dead; +ve => in flight
		self.a = 0.0
		
	def tick(self, dt):
		if self.t > 0:
			self.t -= dt
			if self.t <= 0:
				self.t = 0

	def hitTest(self, x, y):
		return False
			
	def hit(self):
		self.t = FLASHTIME
		
	def draw(self, f):
		if self.t:
			self.rotateToZ(90.0 + self.a)
			self.children[0] = self.so if f else self.wo
			self.MFlg = True
			super(Bullet, self).draw()

if __name__ == '__main__':
	DISPLAY = pi3d.Display.create(near=100.0, far=11000.0, samples=4)
#	DISPLAY.set_background(0, 0, 0, 1)
	camera = pi3d.Camera()
	from pi3d.Display import Display
	lens0 = [Display.INSTANCE.near, Display.INSTANCE.far, Display.INSTANCE.fov,
			Display.INSTANCE.width / float(Display.INSTANCE.height)]
	lens1 = [Display.INSTANCE.near, Display.INSTANCE.far*1.1, Display.INSTANCE.fov,
			Display.INSTANCE.width / float(Display.INSTANCE.height)]

	q = Tank(camera)
	
	inputs = pi3d.InputEvents()
	
	a=0	
	while DISPLAY.loop_running() and not inputs.key_state('KEY_ESC'):
		inputs.do_input_events()
		if inputs.key_state("KEY_LEFT"):
			a += 1
		elif inputs.key_state("KEY_RIGHT"):
			a -= 1
		q.rotateIncY(0.21)
		q.rotateIncX(0.1)
		camera.reset(lens0)
		camera.rotateY(a)
		camera.rotateX(90)
		camera.position((0.0, -500.0, -60.0))
		q.draw(True)
		camera.reset(lens1)
		camera.rotateY(a)
		camera.rotateX(90)
		camera.position((0.0, -500.0, -60.0))
		q.draw(False)

	DISPLAY.destroy()
	
