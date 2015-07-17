import pi3d
from objects import Tank

class WireCube(pi3d.Shape):
	def __init__(self, camera=None, light=None, name='', w=1.0, h=1.0, d=1.0,
		x=0.0, y=0.0, z=0.0,
		rx=0.0, ry=0.0, rz=0.0,
		sx=1.0, sy=1.0, sz=1.0,
		cx=0.0, cy=0.0, cz=0.0):
		
		super(WireCube, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
			sx, sy, sz, cx, cy, cz)
		
		w /= 2
		h /= 2
		d /= 2
		verts = ((-w, -h, -d),
				 (w, -h, -d),
				 (w, h, -d),
				 (-w, h, -d),
				 (-w, -h, d),
				 (w, -h, d),
				 (w, h, d),
				 (-w, h, d))

		inds = ((0, 1, 2),(3, 0, 4),(5, 1, 2),(6, 7, 4),(5, 6, 7),(3, 0, 0))
		buff = pi3d.Buffer(self, verts, [], inds, []) # force no normals
		buff.set_material((0.0, 1.0, 0.0))
		self.buf.append(buff)
		self.set_line_width(15.0, False)
		shader = pi3d.Shader('mat_flat')
		self.set_draw_details(shader, [])

class WireCube2(pi3d.Shape):
	def __init__(self, camera=None, light=None, name='', w=1.0, h=1.0, d=1.0,
		x=0.0, y=0.0, z=0.0,
		rx=0.0, ry=0.0, rz=0.0,
		sx=1.0, sy=1.0, sz=1.0,
		cx=0.0, cy=0.0, cz=0.0):
		
		super(WireCube2, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
			sx, sy, sz, cx, cy, cz)
		
		w /= 2
		h /= 2
		d /= 2
		verts = ((-w, -h, -d),
				 (w, -h, -d),
				 (w, h, -d),
				 (-w, h, -d),
				 (-w, -h, d),
				 (w, -h, d),
				 (w, h, d),
				 (-w, h, d))

		inds = ((0, 1, 2),(3, 0, 4),(5, 1, 2),(6, 7, 4),(5, 6, 7),(3, 0, 0))
		buff = pi3d.Buffer(self, verts, [], inds, []) # force no normals
		buff.set_material((0.0, 1.0, 0.0))
		self.buf.append(buff)
		self.set_line_width(5.0, False)
		shader = pi3d.Shader('mat_flat')
		self.set_draw_details(shader, [])

class Thang(pi3d.Shape):
	def __init__(self, camera=None, light=None, name='', w=1.0, h=1.0, d=1.0,
		x=0.0, y=0.0, z=0.0,
		rx=0.0, ry=0.0, rz=0.0,
		sx=1.0, sy=1.0, sz=1.0,
		cx=0.0, cy=0.0, cz=0.0):
		
		super(Thang, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
			sx, sy, sz, cx, cy, cz)

		self.wq = WireCube(camera0)
		self.qq = pi3d.Cuboid(camera1)
		self.qq.set_material((1.0, 0.0, 0.0))
		shader = pi3d.Shader('mat_flat')
		self.set_draw_details(shader, [])
		self.add_child(self.wq)
		self.add_child(self.qq)

class Qube(pi3d.Cuboid):
	def __init__(self, camera=None, light=None, name='', w=1.0, h=1.0, d=1.0,
		x=0.0, y=0.0, z=0.0,
		rx=0.0, ry=0.0, rz=0.0,
		sx=1.0, sy=1.0, sz=1.0,
		cx=0.0, cy=0.0, cz=0.0):
		z=0
		super(Qube, self).__init__(camera, light, w,h,d,name, x, y, z, rx, ry, rz,
			sx, sy, sz, cx, cy, cz)
		
DISPLAY = pi3d.Display.create(samples=4)
from pi3d.Display import Display
lens = [Display.INSTANCE.near, Display.INSTANCE.far*1.1, Display.INSTANCE.fov,
		Display.INSTANCE.width / float(Display.INSTANCE.height)]
camera0 = pi3d.Camera(lens=lens)

lens = [Display.INSTANCE.near, Display.INSTANCE.far, Display.INSTANCE.fov,
		Display.INSTANCE.width / float(Display.INSTANCE.height)]
camera1 = pi3d.Camera(lens=lens)
q = Qube(z=5)
b = pi3d.Sphere(z=5, sx=2)
if __name__ == '__main__':
	inputs = pi3d.InputEvents()
	
	while DISPLAY.loop_running() and not inputs.key_state('KEY_ESC'):
		a=0	
		inputs.do_input_events()
		if inputs.key_state('KEY_LEFT'):
			a = 1
		if inputs.key_state('KEY_RIGHT'):
			a = -1
		b.rotateIncY(a)
		b.draw()
		
DISPLAY.destroy()
	
