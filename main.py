import pi3d
from objects import Tank, Cube, HalfCube, Pyramid, Bullet
from background import Background
import random
from math import sin, cos, radians, hypot
import ctypes

def Arrange(objects):
	FIELDSIZE = 6000.0
	f0 = -FIELDSIZE / 2
	f1 = FIELDSIZE / 2
	while True:
		for o in objects:
			o.positionX(random.uniform(f0, f1))
			o.positionY(random.uniform(f0, f1))
		break
		
DISPLAY = pi3d.Display.create(near=50.0, far=11000.0, samples=4)
DISPLAY.set_background(0, 0, 0, 1)
camera = pi3d.Camera()
from pi3d.Display import Display
lens0 = [Display.INSTANCE.near, Display.INSTANCE.far, Display.INSTANCE.fov,
		Display.INSTANCE.width / float(Display.INSTANCE.height)]
lens1 = [Display.INSTANCE.near, Display.INSTANCE.far*1.01, Display.INSTANCE.fov,
		Display.INSTANCE.width / float(Display.INSTANCE.height)]

bkgd = Background(camera)
bkgd.set_fog((0, 0, 0, 0), 30000)

objects = []
def addToObjects(n):
	global objects
	FIELDSIZE = 6000.0
	f0 = -FIELDSIZE / 2
	f1 = FIELDSIZE / 2
	MINDISTANCE = 1000.0
	while True:
		tooClose = False
		n.positionX(random.uniform(f0, f1))
		n.positionY(random.uniform(f0, f1))
		for o in objects:
			if hypot(o.x()-n.x(), o.y()-n.y()) < MINDISTANCE:
				tooClose = True
				break
		if not tooClose:
			break
	objects.append(n)

def blocked(t):
	for o in objects:
		if o == t:
			continue
		r = 150
		if isinstance(o, Tank):
			r = 200
		elif isinstance(o, Bullet):
			continue
		if abs(o.x()-t.x()) < r and abs(o.y()-t.y()) < r:
			return True
	return False

def MoveTank(t, l, r, u, d, f, b):
	x = t.x()
	y = t.y()
	if l:
		t.a += 1
	if r:
		t.a -= 1
	if u:
		t.positionX(x - v * sin(radians(t.a)))
		t.positionY(y + v * cos(radians(t.a)))
	if d:
		t.positionX(x + v * sin(radians(t.a)))
		t.positionY(y - v * cos(radians(t.a)))
	if u or d:
		if blocked(t):		# on collision, undo move
			t.positionX(x)
			t.positionY(y)
	if f:
		if b.t == 0:
			b.t = 50
			b.dx = bv * -sin(radians(t.a))
			b.dy = bv * cos(radians(t.a))
			b.positionX(t.x())
			b.positionY(t.y())
			b.a = t.a
			
def MoveBullet(b, t):
	if b.t == 0:
		return
	x = b.x()
	y = b.y()
	for i in range(10):
		x += b.dx
		y += b.dy
		for o in objects:
			if o == b or o == t:
				continue
			if o.hitTest(x, y):
				o.hit()
				b.t = 0
				return
	b.positionX(x)
	b.positionY(y)
	
tank0 = Tank(camera)
tank1 = Tank(camera)
bullet0 = Bullet(camera)
bullet1 = Bullet(camera)
addToObjects(tank0)
addToObjects(tank1)
addToObjects(bullet0)
addToObjects(bullet1)
for i in range(5):
	addToObjects(Cube(camera))
	addToObjects(HalfCube(camera))
	addToObjects(Pyramid(camera))

mwo = pi3d.MergeShape(camera)	# merged wireframe objects
mso = pi3d.MergeShape(camera)
for i in range(4, len(objects)):
	o = objects[i]
	mwo.add(o.wo, x=o.x(), y=o.y())
	mso.add(o.so, x=o.x(), y=o.y())
mwo.set_material((0.0, 1.0, 0.0))
mso.set_material((0.0, 0.0, 0.0))
mwo.set_line_width(3.0, False)
mwo.buf[0].draw_method = pi3d.GL_LINES
shader = pi3d.Shader('mat_flat')
mwo.set_draw_details(shader, [])
mwo.set_fog((0, 0, 0, 1), 30000)
mso.set_fog((0, 0, 0, 1), 30000)

inputs = pi3d.InputEvents()
v = 10
bv = 10
tself = tank0
while DISPLAY.loop_running() and not inputs.key_state('KEY_ESC'):
	inputs.do_input_events()
	MoveTank(tself,
		inputs.key_state("KEY_LEFT"),
		inputs.key_state("KEY_RIGHT"),
		inputs.key_state("KEY_UP"),
		inputs.key_state("KEY_DOWN"),
		inputs.key_state("KEY_SPACE"),
		bullet0)
	MoveTank(tank1, False, True, True, False, True, bullet1)
	MoveBullet(bullet0, tank0)
	MoveBullet(bullet1, tank1)
	camera.reset(lens1)
	camera.rotateY(tself.a)
	camera.rotateX(90)
	camera.position((tself.x(), tself.y(), -60.0))
	pi3d.opengles.glLineWidth(ctypes.c_float(2.0))
	bkgd.positionX(tself.x())
	bkgd.positionY(tself.y())
	bkgd.tick()
	bkgd.draw()
	pi3d.opengles.glLineWidth(ctypes.c_float(3.0))
	for o in objects:
		o.tick()
	for i in range(0, 4):	# draw moving objects
		if objects[i] != tself:
			objects[i].draw(False)	# wireframe
	mwo.draw()				# draw stationary wireframe objects
	camera.reset(lens0)
	camera.rotateY(tself.a)
	camera.rotateX(90)
	camera.position((tself.x(), tself.y(), -60.0))
	for i in range(0, 4):	# draw moving objects
		if objects[i] != tself:
			objects[i].draw(True)	# solid
	mso.draw()				# draw stationary solid objects
	
DISPLAY.destroy()
