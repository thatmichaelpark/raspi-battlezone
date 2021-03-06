import pi3d
from math import pi, sin, cos

class Background(pi3d.Shape):
	def __init__(self, camera=None, light=None, name='', w=1.0, h=1.0, d=1.0,
		x=0.0, y=0.0, z=0.0,
		rx=0.0, ry=0.0, rz=0.0,
		sx=1.0, sy=1.0, sz=1.0,
		cx=0.0, cy=0.0, cz=0.0):
		
		super(Background, self).__init__(camera, light, name, x, y, z, rx, ry, rz,
			sx, sy, sz, cx, cy, cz)
	
		pts = [(i * 160.0, 0.0) for i in range(11)] + [
			(0, -0.01), (30, 25), (70, 3), (85, 7), (96, 15), (120, 0),
			(175, -0.01), (220, 12), (260, 0), 
			(250, -3), (280, 18), (300, 9), (319, 7), (280, -18), (350, 0), 
			(362, -0.01), (388, 9), (383, -0.01), (388, 9), (404, 0), 
			(450, -0.01), (482, 8), (519, 4), (515, -0.01), (529, 14), (540, 17), (566, 0), 
			(600, -0.01), (607, 12), (612, 9), (620, 0), 
			(680, -0.01), (720, 6), (730, 16), (735, 16), (750, 8), (780, 0), (765, -4), (787, 10), (798, 4), (790, -0.01), (815, 12), (840, 0), 
			(900, -0.01), (920, 15), (953, 0), (920, -15), (980, 0), (1005, 18), (1017, 7), (1035, 23), (1053, 0), (1017, -7), (1035, 0),
			(1100, -0.01), (1125, 13), (1133, 6), (1144, 11), (1169, 5), 
			(1160, -0.01), (1175, 8), (1200, 8), (1240, 0),
			(1260, -0.01), (1275, 12), (1295, 0), 
			(1320, -0.01), (1342, 5), (1337, -0.01), (1350, 12), (1370, 4), (1366, -0.01), (1385, 18), (1400, 15), (1425, 0),   
			(1470, -0.01), (1485, 15), (1505, 7), (1500, -0.01), (1511, 14), (1525, 18), 
			(1540, 0), (1537, -4), (1555, 8), (1560, 4), (1600, 0), (-1, -1)
		]
		verts = []
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
		r = 10000.0
		i = 0
		for pt in pts:
			a, h = pt
			if a < 0:
				quit
			a *= pi / 800.0
			f = h >= 0
			h = abs(h) * 100.0
			verts.append((r * sin(a), r * cos(a), -h))
			if f:
				endbuffer = appendToBuffer(endbuffer, i-1)
				endbuffer = appendToBuffer(endbuffer, i)
			i += 1
		closeBuffer(endbuffer)
		uvs = [(0, 0) for i in range(len(verts))]
		norms = [(0, 0, 1) for i in range(len(verts))]
		buff = pi3d.Buffer(self, verts, uvs, inds, norms) # force no normals
		buff.set_material((0.0, 1.0, 0.0))
		self.buf.append(buff)
		self.set_line_width(2.5, False)
		buff.draw_method = pi3d.GL_LINES
		shader = pi3d.Shader('mat_flat')
		self.set_draw_details(shader, [])

