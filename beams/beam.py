import pi3d
from pi3d.util.Utility import magnitude, distance, vec_sub
import numpy as np

from math import sqrt, sin, cos, atan2

def beam(v0, v1, t2):
	# return a list of 8 vertices of a beam of 'radius' t2 extending from v0 to v1
	# (t2 is like 'thickness'/2)
	d = pi3d.Utility.vec_sub(v1, v0)
	# Transform unit x vector to vector v0->v1:
	# 1. Scale along x by factor |v1-v0|
	# 2. Rotate around y
	# 3. Rotate around z
	# 4. Translate to v0
	
	# compute z-rotation to align with x-z plane
	az = atan2(d[1], d[0])
	# compute y-rotation to align with x axis
	r = magnitude(d[0], d[1])
	ay = atan2(d[2], r)
	
	# scale by |d|
	l = magnitude(*d)
	m = np.array([[  l, 0.0, 0.0, 0.0],
				  [0.0, 1.0, 0.0, 0.0],
				  [0.0, 0.0, 1.0, 0.0],
				  [0.0, 0.0, 0.0, 1.0]
	])
	
	# y-rotate 
	s = sin(ay)
	c = cos(ay)
	m = np.dot(m, [[  c, 0.0,   s, 0.0],
				   [0.0, 1.0, 0.0, 0.0],
				   [ -s, 0.0,   c, 0.0],
				   [0.0, 0.0, 0.0, 1.0]
	])
	
	# z-rotate
	s = sin(az)
	c = cos(az)
	m = np.dot(m, [[  c,   s, 0.0, 0.0],
				   [ -s,   c, 0.0, 0.0],
				   [0.0, 0.0, 1.0, 0.0],
				   [0.0, 0.0, 0.0, 1.0]
	])
	
	#translate
	m = np.dot(m, [[1.0, 0.0, 0.0, 0.0],
				   [0.0, 1.0, 0.0, 0.0],
				   [0.0, 0.0, 1.0, 0.0],
				   [v0[0], v0[1], v0[2], 1.0]
	])
	tt = t2 / l
	v = [[0.0-tt, 0.0+t2, 0.0+t2],
		 [0.0-tt, 0.0+t2, 0.0-t2],
		 [0.0-tt, 0.0-t2, 0.0-t2],
		 [0.0-tt, 0.0-t2, 0.0+t2],
		 [1.0+tt, 0.0+t2, 0.0+t2],
		 [1.0+tt, 0.0+t2, 0.0-t2],
		 [1.0+tt, 0.0-t2, 0.0-t2],
		 [1.0+tt, 0.0-t2, 0.0+t2]
	]
	v = np.append(v, np.ones([len(v), 1]), 1)
	a = np.delete(np.dot(v, m), -1, 1)
	return a
