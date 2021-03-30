import cv2

import numpy as np

import math

import shapefile

import shape_moment

# -*- coding: utf-8 -*-

def take_off_same_point(point1):
    if point1[0][0] == point1[len(point1)-1][0] and point1[0][1] == point1[len(point1)-1][1]:
        del point1[len(point1)-1]
        
    return(point1);

def gravity(point1):
    
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


def min_angle_of_main_varypoint(point1):
    

    point_gravity = gravity(point1)
    point_temp = point1
    
    angle = 0

    new_point_location = []
    
    for n in range(len(point1)):
        
        point_location = [0,0]
        
        point_location[0] =point1[n][0]  - point_gravity[0]
        
        point_location[1] =point1[n][1]  - point_gravity[1]
        
        new_point_location.append(point_location)
        
    sum_x_value = 0
    
    sum_y_value = 0
    
    for m in range(len(point1)):
        
        sum_x_value =sum_x_value + new_point_location[m][0]
        
    for o in range(len(point1)):
        
        sum_y_value =sum_y_value + new_point_location[o][1]
        
    sum_x_value = round(sum_x_value,1)
    
    sum_y_value = round(sum_y_value,1)
        
    #print(sum_x_value,sum_y_value)
    
    
    
    #print(point_gravity)
        
    if sum_x_value==0 or sum_y_value==0:
        
        point_temp_np = np.array(point_temp, dtype = int)

        rect = cv2.minAreaRect(point_temp_np)
    
        angle = math.radians(rect[2])

    
        width = rect[1][0]
        
        height = rect[1][1]
    
        if width >= height:
        
            angle = (-1)*angle
        
        else:
            
            angle = (-1)*angle+(0.5*math.pi)
        
    else :
        
        if sum_x_value >0 and sum_y_value >0:
            
            angle = math.atan(sum_y_value/sum_x_value)
            
        elif sum_x_value <0 and sum_y_value >0:
        
            angle = math.pi*0.5+math.atan(abs(sum_y_value)/abs(sum_x_value))
            
        elif sum_x_value <0 and sum_y_value <0:
            
            angle = math.pi+ math.atan(abs(sum_y_value)/abs(sum_x_value))
            
        else :
            
            angle = 2*math.pi - math.atan(abs(sum_y_value)/abs(sum_x_value))
        
    #print(angle)
    y = math.sin(angle)
    x = math.cos(angle)
    #def vector_angle(x1,y1,x2,y2,x3,y3):

    #vector_invariant = [point_gravity[0]-x,point_gravity[1]-y]
    vector_invariant = [x,y]
    #print(vector_invariant)

    vector_vertex = []
    
    for i in range(len(point1)):
        
        vector_b = [0,0]
        
        vector_b = [point1[i][0] - point_gravity[0],point1[i][1] - point_gravity[1]]
        
        vector_vertex.append(vector_b)
        
    #print(vector_vertex)    
    

    mo_vector_invariant = math.sqrt(math.pow(vector_invariant[0],2)+math.pow(vector_invariant[1],2)) 
    
    mo_vector_vertex = []
    
    for j in range(len(point1)):
        
        mo_vector_b = 0
        
        mo_vector_b = math.sqrt(math.pow(vector_vertex[j][0],2)+math.pow(vector_vertex[j][1],2))
        
        mo_vector_vertex.append(mo_vector_b)
        
    angle_list = []
        
    for k in range(len(point1)):
        
        cosin_angle = 0
    
        cosin_angle = (vector_invariant[0]*vector_vertex[k][0]+vector_invariant[1]*vector_vertex[k][1])/(mo_vector_invariant*mo_vector_vertex[k])
        #print(k,cosin_angle)
        
        cosin_angle = round(cosin_angle,3)
    
        angle = math.acos(cosin_angle)
        
        angle_list.append(angle)
    
    return(angle_list.index(min(angle_list)));


def left_point_is_anticlockwise(point1):
    
    '''
    index = min_angle_of_main_varypoint(point1)
    
    if index == (len(point1)-1):
        
        right_point = point1[0]
        
    else :
        
        right_point = point1[(index+1)]
        
    vector_a = right_point
    
    vector_b =  point1[index]
    

    vector_east = [1,0]
    

    mo_vector_a = math.sqrt(math.pow(vector_a[0],2)+math.pow(vector_a[1],2))
    mo_vector_b = math.sqrt(math.pow(vector_b[0],2)+math.pow(vector_b[1],2))
    
    mo_vector_east = math.sqrt(math.pow(vector_east[0],2)+math.pow(vector_east[1],2))
    
    cosin_angle_1 = ((vector_a[0]*vector_east[0]+vector_a[1]*vector_east[1]))/(mo_vector_a*mo_vector_east)
    cosin_angle_2 = ((vector_b[0]*vector_east[0]+vector_b[1]*vector_east[1]))/(mo_vector_b*mo_vector_east)
    
    angle_1 = math.acos(cosin_angle_1)
    
    angle_2 = math.acos(cosin_angle_2)
    
    sign = 0
    
    if angle_1 >= angle_2:
        
        sign = 1
        
    else :
        
        sign = -1
    '''

    point_only_x = []
    
    for i in range(len(point1)):
        
        x = point1[i][0]
        
        point_only_x.append(x)
        
    
    
    #min_x = min(point_only_x)
    
    min_x_index = point_only_x.index(min(point_only_x))
    
    #print(min_x_index)
    
    before_point = []
    
    next_point = []
    

    
    if min_x_index == 0:
        
        before_point_value= point1[(len(point1)-1)]
        
        next_point_value= point1[1]
        
        before_point.append(before_point_value)
        
        next_point.append(next_point_value)
              
    elif min_x_index==(len(point1)-1):
        
        before_point_value= point1[min_x_index-1]
        
        next_point_value= point1[0]
        
        before_point.append(before_point_value)
        
        next_point.append(next_point_value)
        
    else :
        
        before_point_value= point1[min_x_index-1]
        
        next_point_value= point1[min_x_index+1]
        
        before_point.append(before_point_value)
        
        #print(before_point_value)
        
        next_point.append(next_point_value)
        
        #print(next_point_value)
        
    #print(before_point,next_point)
        

    
    line_before=(before_point[0][0]-point1[min_x_index][0],before_point[0][1]-point1[min_x_index][1])
    
    line_next=(next_point[0][0]-point1[min_x_index][0],next_point[0][1]-point1[min_x_index][1])
    
    #print( line_before,line_next)
    
    tan_before =0
    
    tan_next = 0
    
    if line_before[0]==0:
        
        if line_before[1] > 0:
            
            tan_before = float("inf")
            
        if line_before[1] < 0:
            
            tan_before = -float("inf")
        #print(tan_before)
    else:
    
        tan_before = round(line_before[1]/line_before[0],2)
        
        
    if line_next[0]==0:
        
        if line_next[1] > 0:
            
            tan_next = float("inf")
            
        if line_next[1] < 0:
            
            tan_next = -float("inf")
        
        #tan_next = float("inf")
    else :
        
        tan_next = round(line_next[1]/line_next[0],2)
        
    #print(tan_before,tan_next)
    
    sign = 0
    
    if tan_before > tan_next:
        
        sign = 1
        
    elif tan_before < tan_next:
        
        sign = -1
        
    else :
        
        if (line_before[0]==0 and line_next[0]==0 and line_before[1]>0 )or(line_before[1]==0 and line_next[1]==0 and line_before[0]>0 ) :
            
            sign = 1
            
        else:
            
            sign = -1       
        
    
    return(sign);

def re_rank(point1):
    

    key = left_point_is_anticlockwise(point1)
    
    #index = min_angle_of_main_varypoint(point1)
    index = 0
    
    new_rank = []
    
    if key < 0:
        
        left = index
        
        right = (len(point1)-1)
        
        for i in range(0,index+1):
            
            new_rank.append(point1[left])
            
            left = left-1
            
        for j in range(index+1,len(point1)):
            
            new_rank.append(point1[right])
            
            right = right -1
            
    else: 
        
        for j in range(index,len(point1)):
            
            new_rank.append(point1[j])
            
        for i in range(0,index):
            
            new_rank.append(point1[i])
        
    
    return(new_rank);


def add_tail(new_rank):
    
    new_rank.append(new_rank[0])
    
    return(new_rank);


        
