'''
garcia, gil
created: 10/28/2020
last updated: 12/16/2020

purpose: model how the DNA bends under the presence
of a protein
    - 10/28/2020: built DNA w/o any bending
    - 11/4/2020: successfully added phi dependence


To do:
    - add beta angle dependence

'''



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def dna_bend(phi_angle,beta_angle):
    #defining constants
    NT = 10 # nucleotides per loop
    Z_LEN = 3.4 #length of strand in nm
    RADIUS = 1 #radius of DNA loop in nm


    #our independent variables
    num_of_loops = 5
    theta = 0
    input_phi = phi_angle#deg
    input_beta  = beta_angle #deg
    start_bend = Z_LEN * num_of_loops / 2 #DNA will begin to bend at the given distance in nm



    #initializing our list which will be appended too as our prgm runs and hold our coord data
    #for strand 1,
    x1,y1,z1 = [],[],[]
    #for strand 2,
    x2,y2,z2 = [],[],[]
    theta_lst = []

    #creating the x,y,z coordinate and angles for the remainding nucleotides:
    counter = 0
    Lo = 0 #length of strand after bend
    length_of_strand = 0 #current length of strand
    while length_of_strand < num_of_loops*Z_LEN :
        phi = input_phi
        beta = input_beta
        theta_rad = np.deg2rad(theta)
        phi_rad = np.deg2rad(phi)
        beta_rad = np.deg2rad(beta)

        '''
        bend dependence
        '''

        if length_of_strand <= start_bend:
            #phi = 0

            #x1 += [Lo*np.sin(phi_rad) - RADIUS*np.cos(phi_rad)*np.cos(theta_rad)]
            x1 += [RADIUS * np.cos(theta_rad) ]
            y1 += [RADIUS * np.sin(theta_rad) ]
            z1 += [length_of_strand]
            #x2 += [Lo*np.sin(phi_rad) - RADIUS*np.cos(phi_rad)*np.cos(theta_rad + np.pi) ]
            x2 += [RADIUS * np.cos(theta_rad + np.pi) ]
            y2 += [RADIUS * np.sin(theta_rad+ np.pi) ]
            z2 += [length_of_strand]


        else:
            if counter == 0:
                z1_offset =z1[-1]
                z2_offset =z2[-1]
                counter +=1

            Lo += Z_LEN/NT
            z1_offset
            '''
            #beta angle
            #strand 1
            x1 += [RADIUS * np.sin(theta_rad) ]
            y1 += [Lo*np.sin(phi_rad) + RADIUS*np.cos(phi_rad)*np.cos(theta_rad) ]
            z1 += [Lo*np.cos(phi_rad) - RADIUS*np.sin(phi_rad)*np.cos(theta_rad) + z1_offset  ]
            #strand 2
            x2 += [RADIUS * np.sin(theta_rad + np.pi)]
            y2 += [Lo*np.sin(phi_rad) + RADIUS*np.cos(phi_rad)*np.cos(theta_rad + np.pi)]
            z2 += [Lo*np.cos(phi_rad) - RADIUS*np.sin(phi_rad)*np.cos(theta_rad + np.pi)  + z2_offset]
            '''

            '''
            #phi angle
            #strand 1
            x1 += [Lo*np.sin(phi_rad) + RADIUS*np.cos(phi_rad)*np.cos(theta_rad) ]
            y1 += [RADIUS * np.sin(theta_rad) ]
            z1 += [Lo*np.cos(phi_rad) - RADIUS*np.sin(phi_rad)*np.cos(theta_rad)   + z1_offset]
            #strand 2
            x2 += [Lo*np.sin(phi_rad) + RADIUS*np.cos(phi_rad)*np.cos(theta_rad + np.pi) ]
            y2 += [RADIUS * np.sin(theta_rad+ np.pi) ]
            z2 += [Lo*np.cos(phi_rad) - RADIUS*np.sin(phi_rad)*np.cos(theta_rad + np.pi)  +z2_offset]

            '''
            #combining both angles?

            #strand 1
            x1 += [(1/1.41)*(Lo * np.sin(phi_rad) + RADIUS*np.cos(phi_rad)*np.cos(theta_rad) + RADIUS*np.sin(theta_rad))]
            y1 += [(1/1.41)*(Lo*np.sin(beta_rad) + RADIUS*np.cos(beta_rad)*np.cos(theta_rad) - RADIUS*np.sin(theta_rad))]
            z1 += [Lo*np.cos(phi_rad)*np.cos(beta_rad) - RADIUS*np.sin(phi_rad)*np.cos(theta_rad) - RADIUS*np.sin(beta_rad)*np.cos(theta_rad) +  z1_offset  ]
            #stand 2
            x2 += [(1/1.41)*(Lo * np.sin(phi_rad) + RADIUS*np.cos(phi_rad)*np.cos(theta_rad + np.pi)+ (RADIUS*np.sin(theta_rad + np.pi)))]
            y2 += [(1/1.41)*(Lo*np.sin(beta_rad) + RADIUS*np.cos(beta_rad)*np.cos(theta_rad + np.pi) - RADIUS*np.sin(theta_rad + np.pi))]
            z2 += [Lo*np.cos(phi_rad)*np.cos(beta_rad) - RADIUS*np.sin(phi_rad)*np.cos(theta_rad + np.pi) - RADIUS*np.sin(beta_rad)*np.cos(theta_rad + np.pi) +  z2_offset  ]




        theta_lst +=[theta]
        theta += 360/NT
        length_of_strand += Z_LEN/NT



    dna_dict = {
        'theta1':theta_lst,
        'x1':x1,
        'y1':y1,
        'z1':z1,
        'x2':x2,
        'y2':y2,
        'z2':z2
    }

    df = pd.DataFrame.from_dict(dna_dict)
    return df

#df.to_csv('../data/dna_50deg_phi_bend.csv',index = False)

'''


print(df)




fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(x1,y1,z1)
ax.plot(x2,y2,z2)
ax.set(xlabel = 'x', ylabel = 'y', zlabel = 'z')
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_zlim(0, 20)
plt.show()



plt.plot(x1,z1)
plt.plot(x2,z2)
plt.xlabel('x')
plt.ylabel('z')
plt.axis('square')
plt.show()


plt.plot(y1,z1)
plt.plot(y2,z2)
plt.xlabel('y')
plt.ylabel('z')
plt.axis('square')
plt.show()



plt.plot(x1,y1)
plt.plot(x2,y2)
plt.xlabel('y')
plt.ylabel('z')
plt.axis('square')
plt.show()


'''
