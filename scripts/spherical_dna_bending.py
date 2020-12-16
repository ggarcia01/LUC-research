'''
garcia, gil
created: 12/3/2020
updated: 12/3/2020

purpose: model how DNA bends under presence of protein (in the \phi and beta directions)
    - using spherical coordinates
'''


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#defining constants
NT = 10 # nucleotides per loop
Z_LEN = 3.4 #length of strand in nm
RADIUS = 1 #radius of DNA loop in nm


#our independent variables
num_of_loops = 5
theta = 0
input_phi = 0#deg
input_beta  = 0 #deg
start_bend = Z_LEN * num_of_loops / 2 #DNA will begin to bend at the given distance in nm



#creating the DNA data points

#initializing strand1 and strand2's list of data points
r1,theta1,phi1 = [],[],[]
#strand 2's first point
r2,theta2,phi2 = [],[],[]


phi_bend = np.deg2rad(input_phi)
current_theta = np.pi
length = 0
while length < num_of_loops*Z_LEN:
    #calculating the coordinate for strand 1's next DNA point
    d_r1 = np.sqrt(length**2 + 1**2)
    d_theta1 =  current_theta
    d_phi1 = np.pi/2 - np.arctan(length/1) + phi_bend
    #calculating the coordinate for strand 2's next DNA point
    d_r2 = np.sqrt(length**2 + 1**2)
    d_theta2 = current_theta + np.pi
    d_phi2 = np.pi/2 - np.arctan(length/1) + phi_bend

    #adding these coordinates to their list
    r1 += [d_r1]
    theta1 += [d_theta1]
    phi1 +=[d_phi1]
    r2 += [d_r2]
    theta2 += [d_theta2]
    phi2 +=[d_phi2]


    length += Z_LEN/NT
    current_theta += 2*np.pi/NT



#for strand 1,
x1,y1,z1 = [],[],[]
#for strand 2,
x2,y2,z2 = [],[],[]


def spherical2cart(r,theta,phi):
    return r*np.sin(phi)*np.cos(theta), r*np.sin(phi)*np.sin(theta),r*np.cos(phi)


for i in range(len(r1)):
    dx1,dy1,dz1 = spherical2cart(r1[i],theta1[i],phi1[i])
    dx2,dy2,dz2 = spherical2cart(r2[i],theta2[i],phi2[i])

    x1 += [dx1]
    y1 += [dy1]
    z1 += [dz1]

    x2 += [dx2]
    y2 += [dy2]
    z2 += [dz2]


dna_dict = {
    'x1':x1,
    'y1':y1,
    'z1':z1,
    'x2':x2,
    'y2':y2,
    'z2':z2
}

df = pd.DataFrame.from_dict(dna_dict)

print(df)


fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(x1,y1,z1, color = 'blue')
ax.plot(x2,y2,z2, color = 'red')
ax.set(xlabel = 'x', ylabel = 'y', zlabel = 'z')
#ax.set_xlim(-10, 10)
#ax.set_ylim(-10, 10)
#ax.set_zlim(0, 20)
plt.show()





plt.polar(theta1,r1)
plt.show()
