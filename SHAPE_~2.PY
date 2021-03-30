#coding=utf-8

"""
Created on Tuesday Apr 14 10:50:52 2020
"""
######import public package
import math

import xlwt

import numpy as np

import cv2

from operator import itemgetter, attrgetter

import pandas

from pandas import Series, DataFrame

import  matplotlib.pyplot as plt

from PIL import Image

import seaborn as sns

from scipy.spatial import ConvexHull

import scipy as sc

######import  private package
import shapefile

import new_point_rank

import shape_moment

import azimuth_overlap_main_direction


######three convolution kernel
fil_IDM9 = np.array([[1/128,1/128,1/128,1/128,1/128,1/128,1/128,1/128,1/128],
                     [1/128,1/96,1/96,1/96,1/96,1/96,1/96,1/96,1/128],
                     [1/128,1/96,1/64,1/64,1/64,1/64,1/64,1/96,1/128],
                     [1/128,1/96,1/64,1/32,1/32,1/32,1/64,1/96,1/128],
                     [1/128,1/96,1/64,1/32,0   ,1/32,1/64,1/96,1/128],
                     [1/128,1/96,1/64,1/32,1/32,1/32,1/64,1/96,1/128],
                     [1/128,1/96,1/64,1/64,1/64,1/64,1/64,1/96,1/128],
                     [1/128,1/96,1/96,1/96,1/96,1/96,1/96,1/96,1/128],
                     [1/128,1/128,1/128,1/128,1/128,1/128,1/128,1/128,1/128]])

fil_IDM7 = np.array([[0.0139,0.0139,0.0139,0.0139,0.0139,0.0139,0.0139],
                     [0.0139,0.021,0.021,0.021,0.021,0.021,0.0139],
                     [0.0139,0.021,0.042,0.042,0.042,0.021,0.0139],
                     [0.0139,0.021,0.042, 0,0.042,0.021,0.0139],
                     [0.0139,0.021,0.042,0.042,0.042,0.021,0.0139],
                     [0.0139,0.021,0.021,0.021,0.021,0.021,0.0139],
                     [0.0139,0.0139,0.0139,0.0139,0.0139,0.0139,0.0139]])

fil_IDM5 = np.array([[0.03125,0.03125,0.03125,0.03125,0.03125],
                     [0.03125,0.0625,0.0625,0.0625,0.03125],
                     [0.03125,0.0625, 0,0.0625,0.03125],
                     [0.03125,0.0625,0.0625,0.0625,0.03125],
                     [0.03125,0.03125,0.03125,0.03125,0.03125]])

fil_IDM3 = np.array([[0.125,0.125,0.125],
                     [0.125,0,0.125],
                     [0.125,0.125,0.125]])

fil_IDM1 = np.array([[1]])

def vector_angle(x1,y1,x2,y2,x3,y3):#the angle between two vector
    #origian vector
    vector_a = [x2-x1,y2-y1]
    #next vector
    vector_b = [x3-x2,y3-y2]
    
    #norm of vector
    mo_vector_a = math.sqrt(math.pow(vector_a[0],2)+math.pow(vector_a[1],2))
    mo_vector_b = math.sqrt(math.pow(vector_b[0],2)+math.pow(vector_b[1],2))
    
    if mo_vector_a*mo_vector_b == 0:
        
        return(0)
    
    cosin_angle = ((vector_a[0]*vector_b[0]+vector_a[1]*vector_b[1]))/(mo_vector_a*mo_vector_b)
    
    if cosin_angle>1:
        
        cosin_angle = 1
        
    if cosin_angle<-1:
        
        cosin_angle = -1
    
    angle = math.acos(cosin_angle)
    
    return(angle);#return radian

def include_angle(x1,y1,x2,y2,x3,y3,x4,y4):
    #
    vector_a = [x2-x1,y2-y1]
    #
    vector_b = [x4-x3,y4-y3]
    
    #
    mo_vector_a = math.sqrt(math.pow(vector_a[0],2)+math.pow(vector_a[1],2))
    mo_vector_b = math.sqrt(math.pow(vector_b[0],2)+math.pow(vector_b[1],2))
    
    if mo_vector_a*mo_vector_b == 0:
        
        return(0)
    
    cosin_angle = ((vector_a[0]*vector_b[0]+vector_a[1]*vector_b[1]))/(mo_vector_a*mo_vector_b)
    
    if cosin_angle>1:
        
        cosin_angle = 1
        
    if cosin_angle<-1:
        
        cosin_angle = -1
    
    angle = math.acos(cosin_angle)
    
    
    return(angle);#return radian

def calculatelength(X1,Y1,X2,Y2):#distance betwent point1 and point2
    
    s = math.sqrt(math.pow((X2 - X1),2) + math.pow((Y2 - Y1),2))
    
    return s

def Z(points):#the calculation of contour perimeter
    
    length_of_side = []
    
    num = len(points)
    
    Z = 0
    
    for k in range(num - 1):
        
        X1 = points[k][1]
        X2 = points[k+1][1]
        Y1 = points[k][0]
        Y2 = points[k+1][0]
        
        n = calculatelength(X1,Y1,X2,Y2)
        
        Z = Z + n
        
        length_of_side.append(n)

    FX1 = points[0][1]
    FX2 = points[num-1][1]
    FY1 = points[0][0]
    FY2 = points[num-1][0]
    
    end_side = calculatelength(FX1,FY1,FX2,FY2)
    
    perimeter = Z + end_side
    
    length_of_side.append(end_side)
    
    return(perimeter,length_of_side);

def Sk(points,k):#Calculating the arc length from the original point to the K-th point
    
    if k == 0:
        
        return(0);
        
    else :
    
        Sk = 0
    
        for j in range(k):
        
            #print(j)
            X1 = points[j][1]
            X2 = points[j+1][1]
            Y1 = points[j][0]
            Y2 = points[j+1][0]
        
            Sk = Sk + calculatelength(X1,Y1,X2,Y2)
    
        return Sk;

def point_num_of_side(n,nov,perimeter,length_of_side):#a list of the number of interpolation points of each side
    
    point_num_of_side_list = []
    
    for i in range(len(length_of_side)):
        
        num = int((length_of_side[i]/perimeter)*(n - nov))
        
        point_num_of_side_list.append(num)
        
    return(point_num_of_side_list);

def Judge_quadrant(shape_vertex):
    
    quadrant_list = []
    
    num_of_vertex = len(shape_vertex)

    for i in range(num_of_vertex-1):
        
        x1 = shape_vertex[i][0]
        y1 = shape_vertex[i][1]
        x2 = shape_vertex[i+1][0]
        y2 = shape_vertex[i+1][1]
        
        dx = x2-x1
        dy = y2-y1

        if (dx == 0) and (dy == 0):
            
            quadrant_list.append(1)
        
        if (dx >= 0) and (dy > 0):
            
            quadrant_list.append(1)
            
        if (dx > 0) and (dy <= 0):
            
            quadrant_list.append(4)
        
        if (dx < 0) and (dy >= 0):
            
            quadrant_list.append(2)
            
        if (dx <= 0) and (dy < 0):
            
            quadrant_list.append(3)
       
    x1_final = shape_vertex[num_of_vertex-1][0]
    y1_final = shape_vertex[num_of_vertex-1][1]
    x2_first = shape_vertex[0][0]
    y2_first = shape_vertex[0][1]
    
    dx_final = x2_first-x1_final
    dy_final = y2_first-y1_final

    if (dx == 0) and (dy == 0):
            
        quadrant_list.append(1)
    
    if (dx_final >= 0) and (dy_final > 0):
            
        quadrant_list.append(1)
            
    if (dx_final > 0) and (dy_final <= 0):
            
        quadrant_list.append(4)
        
    if (dx_final < 0) and (dy_final >= 0):
            
        quadrant_list.append(2)
            
    if (dx_final <= 0) and (dy_final < 0):
            
        quadrant_list.append(3)
        
    return(quadrant_list);

def gravity(point1):#calculating the centroid of polygon
    
    sum_x =0
    
    for i in range(len(point1)):
        
        sum_x = sum_x + point1[i][0]
    
    point_x = sum_x/(len(point1))
    
    sum_y =0
    
    for j in range(len(point1)):
        
        sum_y = sum_y + point1[j][1]
    
    point_y = sum_y/(len(point1))
    
    point_gravity = [0,0]
    
    point_gravity[0] = point_x
    
    point_gravity[1] = point_y

    return(point_gravity);

def interval_point(n,shape_vertex):#calculating coordinate of each interpolationg points
    
    num_of_vertex = len(shape_vertex)
    
    all_side = []
    
    perimeter,length_of_side = Z(shape_vertex)
    
    point_num_of_side_list = point_num_of_side(n,num_of_vertex,perimeter,length_of_side)

    quadrant_list = Judge_quadrant(shape_vertex)
    
    center_point = gravity(shape_vertex)

    Add_and_subtract_coefficient = [(1,1),(-1,1),(-1,-1),(1,-1)]#The coefficient of the quadrant times the length and the angle

    angle_dir = [(1,0),(-1,0),(-1,0),(1,0)]

    interval_point_list = []

    for i in range(num_of_vertex-1):
        
        #
        x1 = shape_vertex[i][0]
        y1 = shape_vertex[i][1]
        x2 = shape_vertex[i+1][0]
        y2 = shape_vertex[i+1][1]
        #
        x3 = 0
        y3 = 0

        x4 = angle_dir[(quadrant_list[i]-1)][0]
        y4 = angle_dir[(quadrant_list[i]-1)][1]
        
        angle = include_angle(x1,y1,x2,y2,x3,y3,x4,y4)
        
        L = length_of_side[i]

        coeff = Add_and_subtract_coefficient[(quadrant_list[i]-1)]
        
        temp = [shape_vertex[i][0],shape_vertex[i][1]]
        
        interval_point_list.append(temp)
        
        for j in range(point_num_of_side_list[i]):
            
            interval_point = [0,0]
            
            variance_x = ((j+1)/(point_num_of_side_list[i]+1))*L*math.cos(angle)*coeff[0]+x1
            variance_y = ((j+1)/(point_num_of_side_list[i]+1))*L*math.sin(angle)*coeff[1]+y1
            
            interval_point[0] = variance_x
            interval_point[1] = variance_y

            interval_point_list.append(interval_point)

    x1_fin = shape_vertex[num_of_vertex-1][0]
    y1_fin = shape_vertex[num_of_vertex-1][1]
    x2_fir = shape_vertex[0][0]
    y2_fir = shape_vertex[0][1]
    #
    x3 = 0
    y3 = 0
    x4_fin = angle_dir[(quadrant_list[num_of_vertex-1]-1)][0]
    y4_fin = angle_dir[(quadrant_list[num_of_vertex-1]-1)][1]
        
    angle_final = include_angle(x1_fin,y1_fin,x2_fir,y2_fir,x3,y3,x4_fin,y4_fin)
    
    L_fin = length_of_side[num_of_vertex-1]
    
    coeff_fin = Add_and_subtract_coefficient[(quadrant_list[num_of_vertex-1]-1)]
    
    temp_fin = [shape_vertex[num_of_vertex-1][0],shape_vertex[num_of_vertex-1][1]]
        
    interval_point_list.append(temp_fin)
    
    for j_fin in range(point_num_of_side_list[num_of_vertex-1]):
            
        interval_point = [0,0]
            
        variance_x = ((j_fin+1)/(point_num_of_side_list[num_of_vertex-1]+1))*L_fin*math.cos(angle_final)*coeff_fin[0]+x1_fin
        variance_y = ((j_fin+1)/(point_num_of_side_list[num_of_vertex-1]+1))*L_fin*math.sin(angle_final)*coeff_fin[1]+y1_fin
            
        interval_point[0] = variance_x
        interval_point[1] = variance_y
        interval_point_list.append(interval_point)

    return(interval_point_list)

def amendment_interval_point(interval_point,center_point):
    
    amendment = [0,0]
    
    dx_final = interval_point[0]-center_point[0]
    dy_final = interval_point[1]-center_point[1]
    
    if dx_final == 0:
        
        if dy_final > 0:
            
            amendment[0] = interval_point[0]
            amendment[1] = 0.0001+interval_point[1]
            return(amendment);
        
        else:
            
            amendment[0] = interval_point[0]+0.0001
            amendment[1] = -0.0001+interval_point[1]
            return(amendment);
        
    else:
        
        k = dy_final/dx_final
        
        if k > 10:
            
            k = 10
    
    if (dx_final > 0) and (dy_final > 0):
            
        amendment[0] = interval_point[0]+0.0001
        amendment[1] = 0.01*k+interval_point[1]
        return(amendment);
            
    if (dx_final > 0) and (dy_final < 0):
            
        amendment[0] = interval_point[0]+0.0001
        amendment[1] = 0.01*k+interval_point[1]
        return(amendment);
        
    if (dx_final < 0) and (dy_final > 0):
            
        amendment[0] = interval_point[0]-0.0001
        amendment[1] = 0.01*(-k)+interval_point[1]
        return(amendment);
            
    if (dx_final < 0) and (dy_final < 0):
            
        amendment[0] = interval_point[0]-0.0001
        amendment[1] = 0.01*(-k)+interval_point[1]
        return(amendment);
        
    if (dx_final == 0) and (dy_final < 0):
            
        amendment[0] = interval_point[0]
        amendment[1] = interval_point[1]-0.0001
        return(amendment);
        
    if (dx_final == 0) and (dy_final > 0):
            
        amendment[0] = interval_point[0]
        amendment[1] = interval_point[1]+0.0001
        return(amendment);
        
    if (dx_final > 0) and (dy_final == 0):
            
        amendment[0] = interval_point[0]+0.0001
        amendment[1] = interval_point[1]
        return(amendment);
        
    if (dx_final < 0) and (dy_final == 0):
            
        amendment[0] = interval_point[0]-0.0001
        amendment[1] = interval_point[1]
        
        return(amendment);

def ent(data):#calculating the entropy
    
    size = data.shape[0]
    
    t_temp = data.copy()
    
    t_temp = t_temp.reshape((1,size*size))
    
    t_temp = (t_temp.tolist()[0])
    
    t_temp = Series(t_temp)
    
    p_data= t_temp.value_counts()/len(t_temp) # calculates the probabilities
    
    entropy=sc.stats.entropy(p_data)  # input probabilities to get the entropy 
    
    return(entropy)
#the pre-processing of polygon
#Calculating the main direction of the graph, rotating the Angle of the main direction of the graph, and calculating the 
#coordinates after rotation, find out the MBR of the rotating backward coordinate, building dime*dime matrix according to MBR, n is discrete points
def dime_structure_matrix(n,dime,shape_listt,all_point_of_shape):

    length_list = []
    for i_part_length in range(1,len(shape_listt)):
        length_list.append(Z(shape_listt[i_part_length])[0])
    
    #print(length_list)
    sum_length = sum(length_list)

    point_num_list = []#allocating interval points for each side
    for i_part_point_num in length_list:
        point_num_list.append(int(n * (i_part_point_num/(sum_length))))
#Gets the main direction of the graph and USES all the points of the graph to calculate the main direction
    #angle = azimuth_overlap_main_direction.calculate_main_direction(shape_listt[0])

    
    coordinate_list = []
    disperse_coordinate = [[]]
    for i_direction in range(1,len(shape_listt)):
        
   #rotated location
        #coordinate = azimuth_overlap_main_direction.coordinate_system(math.pi - angle,shape_listt[i_direction])
        coordinate = shape_listt[i_direction]
        
        round_coor = []
        
        for j_round in range(len(coordinate)):
        
            temp = [0,0]

            temp[0] = round((coordinate[j_round][0]), 2 )
            temp[1] = round((coordinate[j_round][1]), 2 )
        
            round_coor.append(temp)
        
        coordinate_list.append(round_coor)

        disperse_coordinate[0].extend(interval_point(point_num_list[i_direction-1],round_coor))
    
    all_point_of_shape = local_coor(all_point_of_shape)#For all points center of gravity, eliminating the impact of translation
    
    sorted_rec_point_list_x = sorted(all_point_of_shape, key=itemgetter(0))
    sorted_rec_point_list_y = sorted(all_point_of_shape, key=itemgetter(1))
    
    var_length_width_x = abs(sorted_rec_point_list_x[0][0] - sorted_rec_point_list_x[-1][0])
    
    var_length_width_y = abs(sorted_rec_point_list_y[-1][1] - sorted_rec_point_list_y[0][1])
    
    var_length_width = abs(var_length_width_y - var_length_width_x)


    left_up_x = sorted_rec_point_list_x[0][0]
    left_up_y = sorted_rec_point_list_y[-1][1] +var_length_width/2

    right_down_x = sorted_rec_point_list_x[-1][0]
    right_down_y = sorted_rec_point_list_y[0][1] - var_length_width/2

    gap = (right_down_x  - left_up_x)/dime
    
    if var_length_width_x > var_length_width_y:

        left_up_x = sorted_rec_point_list_x[0][0]
        left_up_y = sorted_rec_point_list_y[-1][1] +var_length_width/2

        right_down_x = sorted_rec_point_list_x[-1][0]
        right_down_y = sorted_rec_point_list_y[0][1] - var_length_width/2

        gap = (right_down_x  - left_up_x)/dime
        
    else:

        left_up_x = sorted_rec_point_list_x[0][0] - var_length_width/2
        left_up_y = sorted_rec_point_list_y[-1][1] 

        right_down_x = sorted_rec_point_list_x[-1][0] + var_length_width/2
        right_down_y = sorted_rec_point_list_y[0][1] 

        gap = (left_up_y - right_down_y)/dime

    return([left_up_x,left_up_y],gap,disperse_coordinate)

def dim_statistic_point_in_grid(dime,left_up,gap,disperse_coordinate):#Creating a dime*dime matrix and counting the number of points in each cell
    
    #statistical grid
    statistic_a = np.zeros(shape=(dime,dime))
    
    for i in range(len(disperse_coordinate[0])):
        
        dis_x = abs(disperse_coordinate[0][i][0] - left_up[0])
        dis_y = abs(disperse_coordinate[0][i][1] - left_up[1])

        temp_line = int(dis_y / gap)

        if temp_line >= dime:
            
            temp_line = dime-1

        temp_row = int(dis_x / gap)
        
        if temp_row >= dime:
            
            temp_row = dime-1
        
        statistic_a[temp_line][temp_row] = statistic_a[temp_line][temp_row] + 1
        
    return(statistic_a)

def rotating(data1):

    a = data1[0,:]
    
    a = np.mat(a)

    result_satck = a.T

    for hang in data1:
    
        hang = np.mat(hang)
    
        result_satck = np.hstack((hang.T,result_satck))

    result_satck = np.delete(result_satck,result_satck.shape[1]-1,axis=1)
    
    result_satck = np.array(result_satck)

    return(result_satck);

def matrix_sim(matr1,matr1_9,matr1_27,matr2,matr2_9,matr2_27):#Calculating the similarity coefficient between matrix A and matrix B in 8 directions

    mat1 = matr1.copy()
    mat1_9 = matr1_9.copy()
    mat1_27 = matr1_27.copy()
    
    mat2 = matr2.copy()
    mat2_9 = matr2_9.copy()
    mat2_27 = matr2_27.copy()
    
    sim_list = []
    
    mat2_list = []
    
    mat2_list.append(mat2)
    
    mat2_9list = []
    
    mat2_9list.append(mat2_9)
    
    mat2_27list = []
    
    mat2_27list.append(mat2_27)

    sim_list.append(mtx_similar4(mat1_9, mat2_9))
    
    for i_1 in range(3):
        
        mat2 = rotating(mat2)
        mat2_list.append(mat2)
        
        mat2_9 = rotating(mat2_9)
        mat2_9list.append(mat2_9)
        
        mat2_27 = rotating(mat2_27)
        mat2_27list.append(mat2_27)

    mat3 = mat2.T
    mat2_list.append(mat3)
    
    mat3_9 = mat2_9.T    

    mat2_9list.append(mat3_9)
    
    mat3_27 = mat2_27.T

    mat2_27list.append(mat3_27)

    sim_list.append(mtx_similar4(mat1_9, mat3_9))
    
    for i_2 in range(3):
        
        mat3 = rotating(mat3)
        mat2_list.append(mat3)
        
        mat3_9 = rotating(mat3_9)
        mat2_9list.append(mat3_9)
        
        mat3_27 = rotating(mat3_27)
        mat2_27list.append(mat3_27)

        sim_list.append(mtx_similar4(mat1_9, mat3_9))
        
    max_index = sim_list.index(max(sim_list))
  
    return(sim_list,mat2_list[max_index],mat2_9list[max_index],mat2_27list[max_index]);

#Calculating the similarity coefficient of matrix A and matrix B with 8 directions (81*81)
#def matrix_sim81(matr1,matr1_9,matr1_27,matr1_81,matr2,matr2_9,matr2_27,matr2_81):
def matrix_sim81(matr1_9,matr1_27,matr1_81,matr2_9,matr2_27,matr2_81):
    
    #mat1 = matr1.copy()
    mat1_9 = matr1_9.copy()
    mat1_27 = matr1_27.copy()
    mat1_81 = matr1_81.copy()
    
    #mat2 = matr2.copy()
    mat2_9 = matr2_9.copy()
    mat2_27 = matr2_27.copy()
    mat2_81 = matr2_81.copy()
    
    sim_list = []
    
    #force_list = []
    
    #mat2_list = []
    
    #mat2_list.append(mat2)
    
    mat2_9list = []
    
    mat2_9list.append(mat2_9)
    
    mat2_27list = []
    
    mat2_27list.append(mat2_27)
    
    mat2_81list = []
    
    mat2_81list.append(mat2_81)
    
    #3*3的相似度
    #sim_list.append(mtx_similar4(mat1, mat2))
    #9*9的相似度
    sim_list.append(mtx_similar4(mat1_9, mat2_9))
    
    #force_list.append(force_diagram(mat1_9, mat2_9))
    #27*27的相似度
    #sim_list.append(mtx_similar4(mat1_27, mat2_27))
    
    #print((mat1, mat2))
    #print(mat2)
    
    for i_1 in range(3):
        
        #mat2 = rotating(mat2)
        #mat2_list.append(mat2)
        
        mat2_9 = rotating(mat2_9)
        mat2_9list.append(mat2_9)
        
        mat2_27 = rotating(mat2_27)
        mat2_27list.append(mat2_27)
        
        mat2_81 = rotating(mat2_81)
        mat2_81list.append(mat2_81)

        sim_list.append(mtx_similar4(mat1_9, mat2_9))

    #mat3 = mat2.T
    #mat2_list.append(mat3)
    
    mat3_9 = mat2_9.T    

    mat2_9list.append(mat3_9)
    
    mat3_27 = mat2_27.T

    mat2_27list.append(mat3_27)
    
    mat3_81 = mat2_81.T
 
    mat2_81list.append(mat3_81)

    sim_list.append(mtx_similar4(mat1_9, mat3_9))

    
    for i_2 in range(3):
        
        #mat3 = rotating(mat3)
        #mat2_list.append(mat3)
        
        mat3_9 = rotating(mat3_9)
        mat2_9list.append(mat3_9)
        
        mat3_27 = rotating(mat3_27)
        mat2_27list.append(mat3_27)
        
        mat3_81 = rotating(mat3_81)
        mat2_81list.append(mat3_81)

        sim_list.append(mtx_similar4(mat1_9, mat3_9))

        
    max_index = sim_list.index(max(sim_list))
    
    #return(sim_list,mat2_list[max_index],mat2_9list[max_index],mat2_27list[max_index],mat2_81list[max_index]);
    return(sim_list,mat2_9list[max_index],mat2_27list[max_index],mat2_81list[max_index]);
    
#getting texture feature
def convolve(img,fil):
    
    img = extend_before_convol(img,fil)

    fil_heigh = fil.shape[0] #Getting the height of the convolution kernel (filter)
    fil_width = fil.shape[1] #Getting the width of the convolution kernel (filter)

    conv_heigh = img.shape[0] - fil.shape[0] + 1   
    conv_width = img.shape[1] - fil.shape[1] + 1

    conv = np.zeros((conv_heigh,conv_width),dtype = 'uint8')
    
    for i in range(conv_heigh):
        
        for j in range(conv_width):       
        
            conv[i][j] = wise_element_multi(img[i:i + fil_heigh,j:j + fil_width ],fil)
            
    return(conv)

def wise_element_sum(img,fil):#Multiplying the template by the statistical grid and calculating the contribution of each grid to the center position

    temp_accordant_sum = img + fil
    #Replacing the value less than 0 in the added matrix with 0
    b = temp_accordant_sum.copy()
    b[b < 0] = 0
    
    return(b.sum())

def wise_element_multi(img,fil):
    
    temp_accordant_multi =np.multiply(img,fil)

    b = temp_accordant_multi.copy()
    b[b < 0] = 0
    
    return(b.sum())

def maxGrayLevel(img):
    max_gray_level=0
    (height,width)=img.shape
    #print(height,width)
    for y in range(height):
        for x in range(width):
            if img[y][x] > max_gray_level:
                max_gray_level = img[y][x]

    return(max_gray_level+1)

#The gray co-occurrence matrix is obtained
def getGlcm(inputs,d_x,d_y):
    
    srcdata=inputs.copy()
    
    (height,width) = inputs.shape
    

    gray_levell = 10

    ret=[[0.0 for i in range(gray_levell)] for j in range(gray_levell)]

    max_gray_level=np.max(inputs)+1

    input_min = np.min(inputs)

    for j1 in range(height):
        for i1 in range(width):
            
            srcdata[j1][i1] =int(((srcdata[j1][i1]-input_min) / (max_gray_level-input_min))*(gray_levell))

    if d_x <0:
        
        for j in range(0,height-d_y):
            for i in range(-d_x,width):
                rows = srcdata[j][i]
                cols = srcdata[j + d_y][i+d_x]
                ret[rows][cols]+=1
        
    else:
        
        for j in range(height-d_y):
            for i in range(width-d_x):
                rows = srcdata[j][i]
                cols = srcdata[j + d_y][i+d_x]
                ret[rows][cols]+=1

    ret[0][0] = 0

    return(np.array(ret))

def soduku(mat9,mat27):
    
    shape9 = (3, 3, 3, 3)
    strides9 = mat9.itemsize * np.array([27, 3, 9, 1])
    squares9 = np.lib.stride_tricks.as_strided(mat9, shape=shape9, strides=strides9) 
    
    shape27 = (3, 3, 9, 9)
    strides27 = mat27.itemsize * np.array([243, 9, 27, 1])
    squares27 = np.lib.stride_tricks.as_strided(mat27, shape=shape27, strides=strides27)

    
    return(squares9,squares27);

def  gradient_soduku(mat33):
    
    grad_mat = mat33 - mat33[1][1]
    
    return(grad_mat);

def mtx_similar4(temp_1, temp_2):

    temp11 = temp_1.ravel()

    temp22 = temp_2.ravel()

        
    s1=pandas.Series(temp11) 
    s2=pandas.Series(temp22)
    corr=s1.corr(s2) 
        
    return(corr)

def mtx_similar3(arr1:np.ndarray, arr2:np.ndarray):

    if arr1.shape != arr2.shape:
        minx = min(arr1.shape[0],arr2.shape[0])
        miny = min(arr1.shape[1],arr2.shape[1])
        differ = arr1[:minx,:miny] - arr2[:minx,:miny]
    else:
        differ = arr1 - arr2
    dist = np.linalg.norm(differ, ord='fro')
    len1 = np.linalg.norm(arr1)
    len2 = np.linalg.norm(arr2)     
    denom = (len1 + len2) / 2
    similar = 1 - (dist / denom)
    return similar


def similarity_99(temp_199,temp_299,filter9):
    
    mat199 = temp_199.copy()
    mat299 = temp_299.copy()

    sim_array = np.zeros((1,9))
    n = 0

    for i in range(3):
        for j in range(3):

            mat199[i][j] = gradient_soduku(mat199[i][j])
            mat299[i][j] = gradient_soduku(mat299[i][j])
            
            cimgs19 = convolve(mat199[i][j],filter9)
            cimgs29 = convolve(mat299[i][j],filter9)

            sim_array[0][n] = similarity_array(cimgs19,cimgs29)
            
            n = n + 1
            
    return(sim_array);

def similarity_27(mat127,mat227,filter27):
    sim_array = np.zeros((1,9))
    n = 0

    for i in range(3):
        for j in range(3):

            cimgs127 = convolve(mat127[i][j],filter27)
    
            cimgs227 = convolve(mat227[i][j],filter27)

            sim_array[0][n] = similarity_array(cimgs127,cimgs227)
            n = n + 1
            
    return(sim_array); 

def extend_before_convol(imgs,filte):

    v_x = int(((filte.shape)[0]-1)/2)
    v_y = (imgs.shape)[0]
    h_x =((filte.shape)[0]-1)+(imgs.shape)[0]
    h_y = int(((filte.shape)[0]-1)/2)

    
    newcols = np.zeros((v_y,v_x))
    newrows = np.zeros((h_y,h_x))

    temp = np.c_[imgs,newcols]
    temp = np.c_[newcols,temp]

    temp = np.r_[temp,newrows]
    temp = np.r_[newrows,temp]

    
    return(temp)

def NmaxGrayLevel(img):
    max_gray_level=0
    (height,width)=img.shape
    print (height,width)
    for y in range(height):
        for x in range(width):
            if img[y][x] > max_gray_level:
                max_gray_level = img[y][x]
    return max_gray_level+1

def map_diffusion_matrix_into_gray_level(inputs):
    
    srcdata=inputs.copy()
    ret=[[0.0 for i in range(gray_level)] for j in range(gray_level)]
    (height,width) = inputs.shape
    
    max_gray_level=maxGrayLevel(inputs)
    #print(gray_level)
    
    for j in range(height):
        for i in range(width):
            srcdata[j][i] = srcdata[j][i]*gray_level / max_gray_level
            
    return(srcdata)

def NgetGlcm(inputs,d_x,d_y):
    srcdata=inputs.copy()
    ret=[[0.0 for i in range(gray_level)] for j in range(gray_level)]
    (height,width) = inputs.shape
    
    max_gray_level=maxGrayLevel(inputs)

    for j in range(height):
        for i in range(width):
            srcdata[j][i] = srcdata[j][i]*gray_level / max_gray_level
    
    for j in range(height-d_y):
        for i in range(width-d_x):
            rows = srcdata[j][i]
            cols = srcdata[j + d_y][i+d_x]
            ret[rows][cols]+=1.0

    for i in range(gray_level):
        for j in range(gray_level):
            ret[i][j]/=float(height*width)

    return(ret)

def Nfeature_computer(p):
    Con=0.0
    Eng=0.0
    Asm=0.0
    Idm=0.0
    p_length = len(p)
    p_width = len(p[0])
    for i in range(p_length):
        for j in range(p_width):
            Con+=(i-j)*(i-j)*p[i][j]
            Asm+=p[i][j]*p[i][j]
            Idm+=p[i][j]/(1+(i-j)*(i-j))
            if p[i][j]>0.0:
                Eng+=p[i][j]*math.log(p[i][j])
    
    Ux = 0
    Uy = 0
    
    deltaX = 0
    deltaY = 0
    
    C = 0
        
    Ux = np.sum(p,axis=0)/p.shape[0]
    
    Uy = np.sum(p,axis=1)/p.shape[1]
    
    average = np.mean(p)
    
    deltaX = np.var(Ux)
    
    deltaY = np.var(Uy)
            
    for i1 in range(p.shape[0]):
        
        for j1 in range(p.shape[1]):

            C = i1 * j1 * p[i1][j1] + C;

    C = (C - average * average)/(deltaX * deltaY)

    return ([Asm,Con,-Eng,Idm,C])


def Ntest(image_name):
    img = cv2.imread(image_name)
    try:
        img_shape=img.shape
    except:
        print('imread error')
        return

    img=cv2.resize(img,(img_shape[1]/2,img_shape[0]/2),interpolation=cv2.INTER_CUBIC)

    img_gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    glcm_0=getGlcm(img_gray, 1,0)

    asm,con,eng,idm=feature_computer(glcm_0)

    return(asm,con,eng,idm)

def divide_shape_hole(point_list,part_index):
    
    parts_vertex_list = []

    conut_n = (list(part_index))

    conut_n.append(len(point_list))

    
    for i in range(len(part_index)):
        
        part_temp = []

        for j in range(conut_n[i],conut_n[i+1]):
            
            part_temp.append(point_list[j])
            
        parts_vertex_list.append(part_temp)
    
    for j in range(len(parts_vertex_list)):
        
        del parts_vertex_list[j][-1]
        
    return(parts_vertex_list)
#To eliminate the effect of translation on results
def local_coor(point_list):
    
    sum_x = 0
    sum_y = 0
    
    for i in range(len(point_list)):
        
        sum_x = sum_x + point_list[i][0]
        sum_y = sum_y + point_list[i][1]
        
    cent_x = sum_x/len(point_list)
    cent_y = sum_y/len(point_list)
    
    local_coor_list = []
    
    for j in range(len(point_list)):
        
        temp = [0,0]
        
        temp[0] = point_list[j][0] - cent_x 
        temp[1] = point_list[j][1] - cent_y
        
        local_coor_list.append(temp)
        
    return(local_coor_list)

def visual_point_level(matrix):
    
    shape = matrix.shape
    if shape[0] == 9:

        m_list = np.resize(matrix,[1,81])
    else:
        m_list = np.resize(matrix,[1,729])
    
    m_list = m_list.tolist()
    
    m_pan = pandas.DataFrame(m_list[0])

    m_pan.columns = ['point']
 
    mins = min(m_list[0])
    maxs = max(m_list[0])

    s = np.arange(mins,maxs,(maxs-mins)/20)
    ss = np.arange(0,19).tolist()
    
    m_pan['point_level'] = pandas.cut(m_pan['point'],s,right=False,labels = ss)
    
    mcount = m_pan.groupby(by = 'point_level').count()
    
    plt.figure();
    mcount.plot.bar()
    #plt.figure()
    plt.show()
    
    return(mcount)

def similarity_array(inputss1,inputss2):
    
    glcm_10=getGlcm(inputss1, 1,0)
    glcm_11=getGlcm(inputss1, 0,1)
    glcm_12=getGlcm(inputss1, 1,1)
    glcm_13=getGlcm(inputss1, -1,1)

    glcm_20=getGlcm(inputss2, 1,0)
    glcm_21=getGlcm(inputss2, 0,1)
    glcm_22=getGlcm(inputss2, 1,1)
    glcm_23=getGlcm(inputss2, -1,1)

    ss10=Nfeature_computer(glcm_10)
    ss11=Nfeature_computer(glcm_11)
    ss12=Nfeature_computer(glcm_12)
    ss13=Nfeature_computer(glcm_13)
    
    ss20=Nfeature_computer(glcm_20)
    ss21=Nfeature_computer(glcm_21)
    ss22=Nfeature_computer(glcm_22)
    ss23=Nfeature_computer(glcm_23)
    
    temp_1 = []
    temp_2 = []
    
    temp_1.extend(ss10)
    temp_1.extend(ss11)
    temp_1.extend(ss12)
    temp_1.extend(ss13)
    temp_2.extend(ss20)
    temp_2.extend(ss21)
    temp_2.extend(ss22)
    temp_2.extend(ss23)
    
    corr_list = []
    for j in range(4):        
        temp11 = []
        temp22 = []
        
        for i in range(4):
            
            temp11.append(temp_1[4*i + j])
            temp22.append(temp_2[4*i + j])
        
        if temp11 == temp22:
            
            corr_list.append(1)
        
        elif (int(np.std(temp11)))==0 or (int(np.std(temp22)))==0:
            #print('!!!!!!!!!')
            temp_corr = mtx_similar3(np.matrix(temp11),np.matrix(temp22))
            corr_list.append(temp_corr)
            #print(temp_corr)
            
        else:
            s1=pandas.Series(temp11) 
            s2=pandas.Series(temp22)
        
            corr_list.append(s1.corr(s2)) #Calculation of correlation coefficient
            
    corr = sum(corr_list)/len(corr_list)
    
    return(corr)


#Defining the maximum grayscale series
gray_level = 10

#
def force_diagram(mat1,mat2):
    
    A = mat1.reshape(1,9)
    B = mat2.reshape(1,9)
    
    C =np.square(A-B)
    
    result = np.sum(C)/9
    
    return(result)

def IDW_template(n):
    
    circle = (n-1)/2
    
    max_distance = 1/circle

    denominator = 1/(circle*8)
    
    temp = np.zeros((n,n))
    
    for i in range(n):
        
        for j in range(n):
            
            distance = max(abs(circle - i),abs(circle - j))
            
            if distance == 0:
                
                temp[i][j] = 0
                
            else:
                
                temp[i][j] = denominator / distance
                
    return(temp)
    
def test_best_point_number(SID1,SID2,increment):
    
    similarity_list = []
    
    point_number_list = []
    
    iteration =  int(1000/increment) + 1
    
    for i in range(0,iteration):
        
        point_number_list.append(100+increment*i)
        
        similarity_list.append(shape_similarity(SID1,SID2,100+increment*i,fil3,fil3,fil9))
            
    return(similarity_list,point_number_list)

def forecasted_point_number(SID1,SID2,point_n):
    
    edge_length1 = Z(local_coor(shape_list[SID1]['point']))[1]
    
    edge_length2 = Z(local_coor(shape_list[SID2]['point']))[1]

    del(edge_length1[-1])
    del(edge_length2[-1])
    
    forecasted_point1 = int((sum(edge_length1)/min(edge_length1))*point_n)+1
    
    forecasted_point2 = int((sum(edge_length2)/min(edge_length2))*point_n)+1
    
    print(forecasted_point1,forecasted_point2)
    
    return(forecasted_point1,forecasted_point2)

def lcm(x, y):

    if x > y:
        greater = x
        
    else:
        greater = y
        
    while(True):
        
        if((greater % x == 0) and (greater % y == 0)):
            lcm = greater
            break
        greater += 1
        
    return(lcm)

def shape_complexity(shapefid):
    
    moment_shape_y = shape_moment.moment_shape(shape_list[shapefid]['point'])
                
    area_shape_y = moment_shape_y[0]
    
    shape_length = Z(shape_list[shapefid]['point'])[0]

    complexity = shape_length/area_shape_y
    
    return(complexity)

def interpolation_point(fid):
    
    point_num = 300
    
    max_cell = 0
    
    point_list = local_coor(shape_list[fid]['point'])
    
    part_index = shape_list[fid]['parts']
    
    part_list = divide_shape_hole(point_list,part_index)
    
    coordinate = fartherest_point(fid)
    
    all_point_of_shape = coordinate
    
    part_list.insert(0,point_list)
    
    while(max_cell <= 10):
        
        left_ups,gaps,disperse_coordinatess_parts = dime_structure_matrix(point_num,27,part_list,all_point_of_shape)
        
        imgs = dim_statistic_point_in_grid(27,left_ups,gaps,disperse_coordinatess_parts)
        
        max_cell = imgs.max()
        
        #print(max_cell)
        
        point_num = point_num + 10
        
    left_ups,gaps,disperse_coordinatess_parts = dime_structure_matrix(point_num,27,part_list,all_point_of_shape)
        
    imgs = dim_statistic_point_in_grid(27,left_ups,gaps,disperse_coordinatess_parts)
    
    num_gt = value_greater_than(imgs)
        
    return(num_gt,point_num)

def interpolation_point_ent(fid,size,IDW):
    
    point_num = 300
    
    max_cell = 0
    
    point_list = local_coor(shape_list[fid]['point'])
    
    part_index = shape_list[fid]['parts']
    
    part_list = divide_shape_hole(point_list,part_index)
    
    part_list.insert(0,point_list)
    
    coordinate = fartherest_point(fid)
    
    all_point_of_shape = coordinate

    ent_list = []

    point_list = []
    
    while(point_num <= 20000):
        
        left_ups,gaps,disperse_coordinatess_parts = dime_structure_matrix(point_num,size,part_list,all_point_of_shape)
        
        imgs = dim_statistic_point_in_grid(size,left_ups,gaps,disperse_coordinatess_parts)
        
        imgs = convolve(imgs,IDW)
        
        imgs = map_diffusion_matrix_into_gray_level(imgs)
        
        ent_list.append(ent(imgs))

        point_list.append(point_num)
        
        point_num = point_num + 300
        
    return(point_list,ent_list)

def value_greater_than(disperse_shape):
    
    width = disperse_shape.shape[0]
    
    gt_num = 0
    
    for i in range(width):
        
        for j in range(width):
            
            if disperse_shape[i][j] >0:
                
                gt_num = gt_num + 1
                
    return(gt_num)

def visual_point_level(matrix):
    
    shape = matrix.shape
    if shape[0] == 9:
        
        m_list = np.resize(matrix,[1,81])
    else:
        m_list = np.resize(matrix,[1,729])
    
    m_list = m_list.tolist()
    
    m_pan = pandas.DataFrame(m_list[0])

    m_pan.columns = ['point']
    
    mins = min(m_list[0])
    maxs = max(m_list[0])

    s = np.arange(mins,maxs,(maxs-mins)/20)
    ss = np.arange(0,19).tolist()
    
    m_pan['point_level'] = pandas.cut(m_pan['point'],s,right=False,labels = ss)
    
    mcount = m_pan.groupby(by = 'point_level').count()
    
    plt.figure();
    mcount.plot.bar()

    plt.show()
    
    return(mcount)

#def fartherest_point(fid):
def fartherest_point(x):

    
    #points = np.array(shape_list[fid]['point'])
    points = np.array(x)
    
    points =local_coor(points)
    
    hull = ConvexHull(points)
    
    hull_point_list = hull.vertices
    
    point_pairs = []
    
    distance = []
    
    for i in hull_point_list:
        
        for j in hull_point_list:
            
            if i == j :
                
                continue;
                
            X1 = points[i][0]
            Y1 = points[i][1]
            X2 = points[j][0]
            Y2 = points[j][1]
                
            distance.append(calculatelength(X1,Y1,X2,Y2))
            point_pairs.append([i,j])
            
    #print(distance.index(max(distance)))
    index_of_farthest = distance.index(max(distance))
    point1,point2 = point_pairs[index_of_farthest]
    #print(point1,point2)

    ratio = (points[point1][0] - points[point2][0])/(points[point1][1] - points[point2][1])
    
    if ratio >= 0:
        
        angle = math.atan((points[point1][0] - points[point2][0])/(points[point1][1] - points[point2][1]))
    
        coordinate = azimuth_overlap_main_direction.coordinate_system(abs(math.pi/2 - angle) ,points)
        
    else :
        
        angle = math.atan((points[point1][0] - points[point2][0])/(points[point1][1] - points[point2][1]))
    
        coordinate = azimuth_overlap_main_direction.coordinate_system(abs(angle) + math.pi/2 ,points)
    
    return(coordinate);
    
def muti_scale(mat):
    
    R0_MAT = mat

    R1_MAT = rotating(R0_MAT)

    R2_MAT = rotating(R1_MAT)

    R3_MAT = rotating(R2_MAT)

    mat_size = mat.shape[0]

    step = int((mat_size - (mat_size % 4)) / 4)

    muti_scale = []

    scale1 = []
    scale1.append(R0_MAT[0:(step), 0:(step)])
    scale1.append(R1_MAT[0:(step), 0:(step)])
    scale1.append(R2_MAT[0:(step), 0:(step)])
    scale1.append(R3_MAT[0:(step), 0:(step)])
    #12-scale
    scale2 = []
    scale2.append(R0_MAT[0:(step*2), 0:(step*2)])
    scale2.append(R1_MAT[0:(step*2), 0:(step*2)])
    scale2.append(R2_MAT[0:(step*2), 0:(step*2)])
    scale2.append(R3_MAT[0:(step*2), 0:(step*2)])
    #18-scale
    scale3 = []
    scale3.append(R0_MAT[0:(step*3), 0:(step*3)])
    scale3.append(R1_MAT[0:(step*3), 0:(step*3)])
    scale3.append(R2_MAT[0:(step*3), 0:(step*3)])
    scale3.append(R3_MAT[0:(step*3), 0:(step*3)])
    #24-scale
    scale4 = []
    scale4.append(R0_MAT[0:(step*4), 0:(step*4)])
    scale4.append(R1_MAT[0:(step*4), 0:(step*4)])
    scale4.append(R2_MAT[0:(step*4), 0:(step*4)])
    scale4.append(R3_MAT[0:(step*4), 0:(step*4)])
    
    muti_scale = [scale1,scale2,scale3,scale4]
    #print(muti_scale)
    return(muti_scale)

#The five texture features in different directions under the same scale are combined to return a tensor
def combine_feature_four_direction(mat_scale):
    
    feature_specific_scale = []
    
    for i in range(len(mat_scale)):
        
        for jj in range(len(mat_scale[i])):
        
            input_mat = mat_scale[i][jj]
    
            glcm_0=getGlcm(input_mat, 1,0)
            glcm_1=getGlcm(input_mat, 0,1)
            glcm_2=getGlcm(input_mat, 1,1)
            glcm_3=getGlcm(input_mat, -1,1)
            
            feature0=Nfeature_computer(glcm_0)
            feature_specific_scale.extend(feature0)
            feature1=Nfeature_computer(glcm_1)
            feature_specific_scale.extend(feature1)
            feature2=Nfeature_computer(glcm_2)
            feature_specific_scale.extend(feature2)
            feature3=Nfeature_computer(glcm_3)
            feature_specific_scale.extend(feature3)
            
            #print(jj)
        
    return(feature_specific_scale)

def fourier_trans(feature_specific):

    transformed_f = np.fft.fft(feature_specific)

    f_A = transformed_f.real

    
    f_B = transformed_f.imag
    
    amplitude_f = np.sqrt( np.square(f_A) +np.square(f_B))
    
    phase_f = np.empty((1,len(f_A)))

    
    TEMP_phase_f = (f_B/f_A)
    
    for i_phase in range(len(f_A)):
        
        phase_f[0][i_phase] = math.atan(-1*TEMP_phase_f[i_phase])

    a = amplitude_f.tolist()
    
    b = phase_f.tolist()

    c = a + b[0]
    
    d = f_A.tolist()
    
    e = f_B.tolist()
    
    f = d + e

    return(d,e);

def moll(a,b):
    
    ans = math.sqrt(math.pow(a,2) + math.pow(b,2))
    
    return ans;

def dn(A,B):
    
    Dn = []

    num = len(A)
    
    if num <= 2:
        
        print("n is too small")
        
    else :
        
        coD1 = moll(A[0],B[0])

        if coD1 == 0:
            
            coD1 = 1
        
        for k in range(1,num):
            
            coDn = moll(A[k],B[k])

            coD = coDn/coD1
            Dn.append(coD)

            
    return(Dn);
  
def dn_distance(feature_specific1,feature_specific2):
    
    A1,B1 = fourier_trans(feature_specific1)
    
    A2,B2 = fourier_trans(feature_specific2)
    
    n = len(A1)
    
    dn_dis = np.empty((n,n),np.float16)
    
    DI = []
    
    di = dn(A1,B1)
    
    dk = dn(A2,B2)

        
    num = len(dk)

    s1 = 0
    s2 = 0
    
    denominator = (sum(di)+sum(di))/2
    
    count = 0
    
    for k in range(num):
        
        count = count + math.pow(di[k]-dk[k],2)

        
        result = math.sqrt(count)

    
    return(result);

def shape_similarity_fourier(muti_scale_list1,muti_scale_list2):
    
    distance_list = []
    
    temp_feature1 = combine_feature_four_direction(muti_scale_list1)
        
    temp_feature2 = combine_feature_four_direction(muti_scale_list2)

    length = int(len(temp_feature1)/4)
    
    for i in range(4):
        
        distance_two_feature = dn_distance(temp_feature1[i*length:(i+1)*length],temp_feature2[i*length:(i+1)*length])
        
        distance_list.append(distance_two_feature)
    
    distance = sum(distance_list)/4
    
    if distance >1:
        
        distance = 1
    
    return(1-distance);

def shape_similarity_feature(muti_scale_list1,muti_scale_list2):
    
    distance_list = []
    
    temp_feature1 = combine_feature_four_direction(muti_scale_list1)
        
    temp_feature2 = combine_feature_four_direction(muti_scale_list2)
    
    feature_list1 = extract_feature(temp_feature1)
    
    feature_list2 = extract_feature(temp_feature2)
    
    for i in range(len(feature_list1)):
        
        distance_two_feature = dn_distance(feature_list1[i],feature_list2[i])
        
        distance_list.append(distance_two_feature)

    distance = sum(distance_list)

        
    return(distance);


def extract_feature(feature):
    
    feature_list = []

    f1 = []
    for j1 in range(int(len(feature)/5)):
    
        f1.append(feature[j1*5])
    
    f2 = []
    for j2 in range(int(len(feature)/5)):
    
        f2.append(feature[j2*5+1])
    
    f3 = []
    for j3 in range(int(len(feature)/5)):
    
        f3.append(feature[j3*5+2])
    
    f4 = []
    for j4 in range(int(len(feature)/5)):
    
        f4.append(feature[j4*5+3])
    
    f5 = []
    for j5 in range(int(len(feature)/5)):
    
        f5.append(feature[j5*5+4])
        
    feature_list = [f1,f2,f3,f4,f5]

    f1_rank = []
    f2_rank = []
    f3_rank = []
    f4_rank = []
    f5_rank = []

    for i in range(4):
        
        for j in range(4):
            #'''
            temp1_f1 = normalize(f1[16*i+j*4:16*i+4+j*4])
            temp2_f2 = normalize(f2[16*i+j*4:16*i+4+j*4])
            temp3_f3 = normalize(f3[16*i+j*4:16*i+4+j*4])
            temp4_f4 = normalize(f4[16*i+j*4:16*i+4+j*4])
            temp5_f5 = normalize(f5[16*i+j*4:16*i+4+j*4])
        
            f1_rank.extend(temp1_f1)
            f2_rank.extend(temp2_f2)
            f3_rank.extend(temp3_f3)
            f4_rank.extend(temp4_f4)
            f5_rank.extend(temp5_f5)
    
    feature_list = [f1_rank,f2_rank,f3_rank,f4_rank,f5_rank]

    return(feature_list)

def normalize(feature):
    
    max_element = max(feature)
    min_element = min(feature)
    
    for i in range(len(feature)):
        
        if (max_element-min_element) == 0:
            
            feature[i] = 0
            
        else:
            
            feature[i] = (feature[i]-min_element)/(max_element-min_element)
        
    return(feature)

def shape_similarity_correlation(muti_scale_list1,muti_scale_list2):
    
    distance_list = []
    
    temp_feature1 = combine_feature_four_direction(muti_scale_list1)
        
    temp_feature2 = combine_feature_four_direction(muti_scale_list2)
    
    feature_list1 = extract_feature(temp_feature1)
    
    feature_list2 = extract_feature(temp_feature2)
    
    for i in range(len(feature_list1)):
    
        s1=pandas.Series(feature_list1[i])
        s2=pandas.Series(feature_list2[i])
        corr=s1.corr(s2)
        
        distance_list.append(corr)
        
    distance = sum(distance_list)/len(distance_list)
    
    if distance >1:
        
        distance = 1
    
    return(distance);

def gray_scaling(srcdata):
    
    height,width = srcdata.shape
    
    max_gray_level=np.max(srcdata)+1
    input_min=np.min(srcdata)
    
    gray_levell =10

    for j1 in range(height):
        for i1 in range(width):

            srcdata[j1][i1] =int(((srcdata[j1][i1]-input_min) / (max_gray_level-input_min))*(gray_levell))
    
    return(srcdata)

def statistic_precision_recall(sample_type,templete_result,threshold):
    
    precision_list = []
    
    recall_list = []
    
    for i in range(0,20):

        temp_list_overall = []

        temp_list_accurate = []
        
        for j in range(0,660):
            
            if templete_result[j][i] >= threshold:
                
                temp_list_overall.append(j)

                if j in range(sample_type*20,(sample_type+1)*20):
                    
                    temp_list_accurate.append(j)
                    
        precision_temp = len(temp_list_accurate)/len(temp_list_overall)
        
        recall_temp = len(temp_list_accurate)/20
        
        precision_list.append(precision_temp)
        
        recall_list.append(recall_temp)
    
    return(sum(precision_list)/20,sum(recall_list)/20)

def shape_similarity_mut(shape_list1,shape_list2,n):

    #IDM5 is the best convolution kernel
    IDM1,IDM3,IDM5,IDM7,IDM9,IDM11 = fil_IDM5,fil_IDM5,fil_IDM5,fil_IDM5,fil_IDM5,fil_IDM5
    
    s1_part_index = shape_list1['parts']
    #The coordinates we get are the furthest point in the principal direction, after rotation
    coordinate_temp11 = fartherest_point(shape_list1['point'])
    s1_point_list = local_coor(coordinate_temp11) 

    s2_part_index = shape_list2['parts']
    coordinate_temp22 = fartherest_point(shape_list2['point'])
    s2_point_list = local_coor(coordinate_temp22)
    
    s1_part_list = divide_shape_hole(s1_point_list,s1_part_index)
    s2_part_list = divide_shape_hole(s2_point_list,s2_part_index)
    
    s1_part_list.insert(0,s1_point_list)
    s2_part_list.insert(0,s2_point_list)

    #polygon 1 9*9
    left_ups19,gaps19,disperse_coordinates19 = dime_structure_matrix(n[0],9,s1_part_list,coordinate_temp11)
    imgs19 = dim_statistic_point_in_grid(9,left_ups19,gaps19,disperse_coordinates19)
    
    #polygon 1 27*27
    left_ups127,gaps127,disperse_coordinates127 = dime_structure_matrix(n[1],27,s1_part_list,coordinate_temp11)
    imgs127 = dim_statistic_point_in_grid(27,left_ups127,gaps127,disperse_coordinates127)
    
    #polygon 1 81*81
    left_ups181,gaps181,disperse_coordinates181 = dime_structure_matrix(n[2],81,s1_part_list,coordinate_temp11)
    imgs181 = dim_statistic_point_in_grid(81,left_ups181,gaps181,disperse_coordinates181)

    
    #polygon 2 9*9
    left_ups29,gaps29,disperse_coordinates29 = dime_structure_matrix(n[0],9,s2_part_list,coordinate_temp22)
    imgs29 = dim_statistic_point_in_grid(9,left_ups29,gaps29,disperse_coordinates29)
    
    #polygon 2 27*27
    left_ups227,gaps227,disperse_coordinates227 = dime_structure_matrix(n[1],27,s2_part_list,coordinate_temp22)
    imgs227 = dim_statistic_point_in_grid(27,left_ups227,gaps227,disperse_coordinates227)
    
    #polygon 2 81*81
    left_ups281,gaps281,disperse_coordinates281 = dime_structure_matrix(n[2],81,s2_part_list,coordinate_temp22)
    imgs281 = dim_statistic_point_in_grid(81,left_ups281,gaps281,disperse_coordinates281)
    
    #sim_list,imgs23,imgs29,imgs227,imgs281 = matrix_sim81(imgs13,imgs19,imgs181,imgs127,imgs23,imgs29,imgs227,imgs281)
    sim_list,imgs29,imgs227,imgs281 = matrix_sim81(imgs19,imgs181,imgs127,imgs29,imgs227,imgs281)

    #9*9
    
    cimgs139 = convolve(imgs19,IDM3)
    cimgs239 = convolve(imgs29,IDM3)
    
    scale_fid139 = muti_scale(cimgs139)
    scale_fid239 = muti_scale(cimgs239)
    
    shape_sim93 = shape_similarity_correlation(scale_fid139,scale_fid239)

    #27*27
    cimgs1727 = convolve(imgs127,IDM7)
    cimgs2727 = convolve(imgs227,IDM7)

    
    scale_fid1727 = muti_scale(cimgs1727)
    scale_fid2727 = muti_scale(cimgs2727)
    
    shape_sim277 = shape_similarity_correlation(scale_fid1727,scale_fid2727)
    
    #81*81
    cimgs11181 = convolve(imgs181,IDM11)
    cimgs21181 = convolve(imgs281,IDM11)
    
    scale_fid15 = muti_scale(cimgs11181)
    scale_fid25 = muti_scale(cimgs21181)
    
    shape_sim81 = shape_similarity_correlation(scale_fid15,scale_fid25)

    #print(shape_sim93,shape_sim277,shape_sim81)

    return((shape_sim93 + shape_sim277  + shape_sim81) /3)