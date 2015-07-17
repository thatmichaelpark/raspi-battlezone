import pi3d
from objects import Tank, Cube, HalfCube, Pyramid, Bullet
from background import Background
import random

def Arrange(objects):
	FIELDSIZE = 6000.0
	f0 = -FIELDSIZE / 2
	f1 = FIELDSIZE / 2
	while True:
		for o in objects:
			o.positionX(random.uniform(f0, f1))
			o.positionY(random.uniform(f0, f1))
		break
		
DISPLAY = pi3d.Display.create(near=100.0, far=11000.0, samples=4)
DISPLAY.set_background(0, 0, 0, 1)
camera = pi3d.Camera()

objects = []
objects.append(Tank(camera))
objects.append(Tank(camera))
objects.append(Bullet(camera))
objects.append(Bullet(camera))
for i in range(4):
	objects.append(Cube(camera))
	objects.append(HalfCube(camera))
	objects.append(Pyramid(camera))
Arrange(objects)

bkgd = Background(camera)
bkgd.set_fog((0, 0, 0, 0), 30000)

inputs = pi3d.InputEvents()
a = 0.0

while DISPLAY.loop_running() and not inputs.key_state('KEY_ESC'):
	inputs.do_input_events()
	if inputs.key_state("KEY_LEFT"):
		a += 1
	elif inputs.key_state("KEY_RIGHT"):
		a -= 1
	camera.reset()
	camera.rotateX(0)
	camera.rotateY(a)
	camera.rotateX(90)
	camera.position((100.0, -100.0, -60.0))
	bkgd.draw()
	for o in objects:
		o.MFlg = True	# hack for child-not-drawing bug
		o.draw()
	
DISPLAY.destroy()
