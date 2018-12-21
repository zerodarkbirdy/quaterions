# Created: 12/19/18
# Author: Connor McNaboe
# Purpose: Transform reference frames using quaterions 

from math import * 
import numpy as np
from numpy.linalg import inv
import scipy

from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

# Method One: Use a give set of three consequtive rotations about each a
# axis (euler angles)

def rot_ang(gamma, theta, phi):

	Cx = np.array([[1, 0, 0],[0, cos(phi), sin(phi)],[0, -sin(phi), cos(phi)]])
	Cy = np.array([[cos(theta), 0, -sin(theta)], [0,1,0], [sin(theta), 0, cos(theta)]])
	Cz = np.array([[cos(gamma), sin(gamma), 0], [-sin(gamma), cos(gamma), 0], [0,0,1]])
	C = np.array([Cx, Cy, Cz])
	return C

def quaterion_ang(C): 
	#Takes Rotation matrix as an argument and returns a quaterion

	q4 = 0.5*sqrt(1+np.trace(C))
	q1 = (C[1, 2] - C[2,1])/(4*q4)
	q2 = (C[2,0] - C[0,2])/(4*q4)
	q3 = (C[0,1] - C[1, 0])/(4*q4)
	q = np.array([q1, q2, q3])
	check = q1**2 + q2**2 + q3**2 + q4**2
	print("Check ang: " + str(check) + "\n")
	return q, q4

# Method 2: Use given euler axis and principle angle to determine quaterions

def quterion_axis(e, PHI):
	
	q1 = e[0]*sin(PHI/2)
	q2 = e[1]*sin(PHI/2)
	q3 = e[2]*sin(PHI/2)
	q4 = cos(PHI/2)
	q = np.array([q1, q2, q3])
	print(q)
	check = q1**2 + q2**2 + q3**2 + q4**2
	print("Check axis: " + str(check) + "\n")
	return q, q4

def rot_axis(q, q4):

	S = np.array([[0, -q[2], q[1]], [q[2], 0, -q[0]], [-q[1], q[0], 0]])
	#C = (q4**2 - q.T*q)*np.identity(3) + 2*q*q.T - 2*q4*S
	c11 = q[0]**2 - q[1]**2 - q[2]**2 + q4**2
	c12 = 2*(q[0]*q[1] + q[2]*q4)
	c13 = 2*(q[0]*q[2] - q[1]*q4)
	c21 = 2*(q[0]*q[1] - q[2]*q4)
	c22 = -q[0]**2 + q[1]**2 - q[2]**2 + q4**2
	c23 = 2*(q[1]*q[2] + q[0]*q4)
	c31 = 2*(q[0]*q[2] + q[1]*q4)
	c32 = 2*(q[1]*q[2] - q[0]*q4)
	c33 = -q[0]**2 - q[1]**2 + q[2]**2 + q4**2
	C = np.array([[ c11, c12, c13], [c21, c22, c23], [c31, c32, c33]])
	return C

def transform(q, r):
	r_in = np.append([0], r)
	
	qmtrx = np.array([[(q[0]**2 + q[1]**2+ q[2]**2 + q[3]**2), 0, 0, 0], \
		[0, (q[0]**2 + q[1]**2- q[2]**2 - q[3]**2), (2*q[1]*q[2] - 2*q[0]*q[3]), \
		(2*q[1]*q[3]+2*q[0]*q[2])], [0, (2*q[1]*q[2] + 2*q[0]*q[3]), \
		(q[0]**2 - q[1]**2+ q[2]**2 - q[3]**2), (2*q[2]*q[3] - 2*q[0]*q[1])], \
		[0, (2*q[1]*q[3]-2*q[0]*q[2]), (2*q[2]*q[3] + 2*q[0]*q[1]), \
		(q[0]**2 -q[1]**2- q[2]**2 + q[3]**2)]])
	print(qmtrx)
	r_out = r_in.dot(qmtrx)
	return r_out

def transfrom2(q, r):
	r_in = np.append([0], r)
	qcon = np.array([q[0], -1*q[1], -1*q[2], -1*q[3]])
	r_out = q*r_in*qcon
	print(r_out)
# Rotation 1
PHI1 = radians(-90)	     # Principle angle 
e1 = np.array([0,1,0])   # Euler axis

qax1, q4ax1 = quterion_axis(e1, PHI1)
Cax = rot_axis(qax1, q4ax1)
qax = np.append(q4ax1, qax1)
r = np.array([1,0,0])
r_ax1 = Cax.dot(r)
r_ax2 = transform(qax, r)
transfrom2(qax, r)
print("Vectors: \n")
print(r)
print(r_ax1)
print(r_ax2)

# Data for a three-dimensional line

ax = plt.axes(projection='3d')

ax.scatter(r[0], r[1], r[2], zdir='z', c='r')
ax.scatter(r_ax1[0], r_ax1[1], r_ax1[2], zdir='z',  c='b')
ax.scatter(r_ax2[1], r_ax2[2], r_ax2[3], zdir='z',  c='g')

for a  in r:
    rx = np.linspace(0, r[0], 100)
    ry = np.linspace(0, r[1], 100)
    rz = np.linspace(0, r[2], 100)
    ax.plot(rx, ry, rz)

    rax = np.linspace(0, r_ax1[0], 100)
    ray = np.linspace(0, r_ax1[1], 100)
    raz = np.linspace(0, r_ax1[2], 100)
    ax.plot(rax, ray, raz)

#ax.plot3D([0, r[0]], [0, r[1]], zs=[0, r[2]], 'blue')
#ax.plot3D([0, r_ax[0]], [0, r_ax[1]], [0, r_ax[2]], 'gray')
#ax.plot3D([0, r_ang[0]], [0, r_ang[1]], [0, r_ang[2]], 'green')

plt.show()
