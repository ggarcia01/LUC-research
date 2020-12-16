'''

garcia,gil
created: 12/7/2020
last updated: 12/14/2020

purpose: analyzing the bent DNA data

'''


import matplotlib.pyplot as plt
from scipy.stats import chisquare
import pandas as pd
import numpy as  np
import random


#constants
Z_LEN = 3.4 #length of strand in nm
num_of_loops = 5

#input values
expected_angle = 50



#distance calculation
def pythagorean_dist(x1,y1,z1,x2,y2,z2):
    return np.sqrt( (x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)

#law_of_cosines to find length of side C. angle C should be in radians.
def law_of_cosines_side_c(side_a,side_b,angle_C):
    return np.sqrt(side_a**2 + side_b**2 - 2*side_a*side_b*np.cos(angle_C))
#law of cosines to solve for the angle C, returns angle in degrees
def law_of_cosines_angle_C(side_a,side_b,side_c):
    return (180/np.pi)*np.arccos((side_c**2 - side_a**2 - side_b**2)/(2*side_a*side_b))

#method of least squares to find the line of best fit's slop and y-int
def least_squares(x,y):
	N=float(len(x))
	delta=(N*(np.sum(x**2)))-((np.sum(x))**2)
	A_top=((np.sum(y))*(np.sum(x**2)))-((np.sum(x))*(np.sum(x*y)))
	A=(A_top)/(delta)
	B_top=((N*(np.sum(x*y)))-((np.sum(x))*(np.sum(y))))
	B=(B_top)/(delta)
	#A= y-int, B= slope
	return A,B



#bend starts at nt num. 39
df = pd.read_csv('../data/dna_50deg_phi_bend.csv')
#index of the nucleotides before the kink
points_before_bend = [0,1,2,3,4,5,6,7,8,9]
#index of the nucleotides after the kink
points_after_bend = [45,44,43,42,41,40,39,38,37,36]


#getting the coordinates for all our points
x1,y1,z1 = [],[],[]
x2,y2,z2 = [],[],[]

for i in points_before_bend:
    x1 += [df.iloc[i,1]]
    y1 +=[df.iloc[i,2]]
    z1 += [df.iloc[i,3]]

for j in points_after_bend:
    x2 += [df.iloc[j,1]]
    y2 +=[df.iloc[j,2]]
    z2 += [df.iloc[j,3]]



#calculating the distance from each point to the kink site
kink_location = [0,0,Z_LEN*num_of_loops/2] #x,y,z coords

kink_pts1_dist = [] #this is side A for law of cosines
kink_pts2_dist = [] #side B
nt_distances = [] #side C

for i in range(len(x1)):
    kink_pts1_dist += [pythagorean_dist(x1[i],y1[i],z1[i],kink_location[0],kink_location[1],kink_location[2])]
    kink_pts2_dist += [pythagorean_dist(x2[i],y2[i],z2[i],kink_location[0],kink_location[1],kink_location[2])]
    nt_distances += [pythagorean_dist(x1[i],y1[i],z1[i],x2[i],y2[i],z2[i])] #comparing first and last, 2nd and 2nd last, etc.


#solving for the phi angle
angles =[]
for i in range(len(nt_distances)):
    angles += [law_of_cosines_angle_C(kink_pts1_dist[i],kink_pts2_dist[i],nt_distances[i])]


plt.scatter(nt_distances,angles)
plt.axhline(expected_angle, color='black')
plt.show()

print('Chi Squared Test for Expected Angle:')
print('-----------------------------------------')
exp_values = [expected_angle]*len(angles)
chi_values = chisquare(angles,f_exp=exp_values)
print(chi_values)
print()


print()
print('Chi Squared Minimization Test')
print('-----------------------------------------')
least_chi_value = 100000
for num in np.linspace(0,90,1000):
    exp_values = [num]*len(angles)
    chi_values = chisquare(angles,f_exp=exp_values)
    if chi_values[0] < least_chi_value:
        least_chi_value = chi_values[0]
        best_angle = num

print()
print('angle that minimizes the Chi Square value is:',best_angle)
print('chi squared test for best fit angle:',chisquare(angles,[best_angle]*len(angles)   ))


#adding 10% error to data
angles_w_err = []
for element in angles:
    err = random.uniform(0.05,0.1)
    angles_w_err += [element + (element*err)]


minimized_chi_test = 1000000

for elm in np.linspace(0,90,1000):
    best_fit_line = [elm]*len(angles_w_err)
    chi_test = chisquare(angles_w_err,f_exp=best_fit_line)
    if chi_test[0] < minimized_chi_test:
        minimized_chi_test = chi_test[0]
        best_fit_angle = elm



print()
print('Chi Squared Minimization Test with 5%-10% added error')
print('-----------------------------------------')
print()
print('angle that minimizes the Chi Square value is:',best_fit_angle)
print('chi squared test for best fit angle:',chisquare(angles_w_err,[best_fit_angle]*len(angles_w_err)))
