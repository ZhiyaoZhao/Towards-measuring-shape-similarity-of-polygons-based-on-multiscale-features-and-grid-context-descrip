import math

import shapefile

import new_point_rank

import numpy as np

import operator

import cv2

from operator import itemgetter, attrgetter


def calculate_main_direction(shape_listt):
    
    #print(shape_list[j]['point'])
    #point_gravity = shape_moment.grivate_point(shape_listt[n]['point'])
    
    point_temp = shape_listt
        
    point_temp_np = np.array(point_temp, dtype = float)
    
    point_temp_np =point_temp_np*100
        
    point_temp_np = point_temp_np.astype(np.int64)

    rect = cv2.minAreaRect(point_temp_np)
    
    angle = math.radians(rect[2])
        

    
    width = rect[1][0]
        
    height = rect[1][1]
    
    if width >= height:
        
        angle = (-1)*angle
        #angle = angle
        
    else:
            
        angle = (-1)*angle+(0.5*math.pi)
        #angle = angle+(0.5*math.pi)
        

    #angle = 180 - angle*180/math.pi
        
    return(angle)

def vector_angle(x1,y1,x2,y2,x3,y3):

    vector_a = [x2-x1,y2-y1]

    vector_b = [x3-x2,y3-y2]
    

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
    

    return(angle);


def coordinate_system(angle,shape_point_list):
    

    point_array = np.array(shape_point_list)
    

    rotate_matrix = [[math.cos(angle),-math.sin(angle)],[math.sin(angle),math.cos(angle)]]
    
    after_rotate_coordinate = np.dot(point_array,rotate_matrix)
    
    coordinate = after_rotate_coordinate.tolist()
    
    return(coordinate)


def calculate_overlapping(rotate1,rotate2):
    

    rotate1_sort_x = sorted(rotate1)
    #rotate1_sort_y = sorted(rotate1, key=itemgetter(1))
    rotate2_sort_x = sorted(rotate2)
    #rotate2_sort_y = sorted(rotate2, key=itemgetter(1))
    
    r1_min_x = rotate1_sort_x[0][0]
    r1_max_x = rotate1_sort_x[-1][0]
    
    r2_min_x = rotate2_sort_x[0][0]
    r2_max_x = rotate2_sort_x[-1][0]
    #print(r1_min_x,r2_min_x)
    #print(r1_max_x,r2_max_x)
    
    overlap = 0
    all_length = 0
    overlapping_degree = 0
    
    if r1_max_x < r2_min_x or r1_min_x > r2_max_x:
        
        overlapping_degree = 0
    
    elif r1_max_x < r2_max_x and r1_max_x > r2_min_x and  r1_min_x< r2_min_x : 
        
        overlap = r1_max_x - r2_min_x
        all_length = r2_max_x - r1_min_x
        overlapping_degree = overlap/all_length
        #print(1)
        
    elif r2_max_x < r1_max_x and r2_max_x > r1_min_x and  r2_min_x< r1_min_x: 
        
        overlap = r2_max_x - r1_min_x
        all_length = r1_max_x - r2_min_x
        overlapping_degree = overlap/all_length
        #print(2)
        
    elif r2_max_x < r1_max_x and r2_min_x > r1_min_x: 
        
        overlap = r2_max_x - r2_min_x
        all_length = r1_max_x - r1_min_x
        overlapping_degree = overlap/all_length
        #print(3)
        
    elif r2_max_x > r1_max_x and r2_min_x < r1_min_x: 
        
        overlap = r1_max_x - r1_min_x
        all_length = r2_max_x - r2_min_x
        overlapping_degree = overlap/all_length
        #print(4)
    
    
    return(overlapping_degree)   
       
def overlapping_degree(shape1,shape2):      
    
    #angle = calculate_main_direction(shape1)
    
    angle = math.pi - calculate_main_direction(shape1)
    
    #print(angle)
    
    ri_point1 = coordinate_system(angle,shape1)
    
    r2_point2 = coordinate_system(angle,shape2)
    
    degree = calculate_overlapping(ri_point1,r2_point2)
    
    return(degree)

def vector_angle(x1,y1,x2,y2,x3,y3):

    vector_a = [x2-x1,y2-y1]

    vector_b = [x3-x2,y3-y2]
    

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
    

    return(angle);


def calculatelength(X1,Y1,X2,Y2):
    
    s = math.sqrt(math.pow((X2 - X1),2) + math.pow((Y2 - Y1),2))
    
    return(s)

def normal_list(list_1):
    
    result_nor = []
    
    max_element = max(list_1)
    min_element = min(list_1)
    
    for i in range(len(list_1)):
        
        result_nor.append((list_1[i]-min_element)/(max_element-min_element))
        
    return(result_nor);


class point(): 
    def __init__(self,x,y):
        self.x=x
        self.y=y   

def cross(p1,p2,p3):
    x1=p2.x-p1.x
    y1=p2.y-p1.y
    x2=p3.x-p1.x
    y2=p3.y-p1.y
    return( x1*y2-x2*y1 )    

def IsIntersec(p1,p2,p3,p4): 


    if(max(p1.x,p2.x)>=min(p3.x,p4.x)    
    and max(p3.x,p4.x)>=min(p1.x,p2.x)   
    and max(p1.y,p2.y)>=min(p3.y,p4.y)   
    and max(p3.y,p4.y)>=min(p1.y,p2.y)): 

    
        if(cross(p1,p2,p3)*cross(p1,p2,p4)<=0
           and cross(p3,p4,p1)*cross(p3,p4,p2)<=0):
            D=1
        else:
            D=0
    else:
        D=0
    return(D)


def intersection_distance(a1,b2,c3,d4):
    
    #b1 = (y2-y1)*x1+(x1-x2)*y1
    B1 = (b2.y - a1.y)*a1.x + (a1.x - b2.x)*a1.y
    #b2 = (y4-y3)*x3+(x3-x4)*y3
    B2 = (d4.y - c3.y)*c3.x + (c3.x - d4.x)*c3.y
    #D = (x2-x1)(y4-y3) * (x4-x3)*(y2-y1)
    D = (b2.x - a1.x)*(d4.y - c3.y) - (d4.x - c3.x)*(b2.y - a1.y)
    #D1 = b2*(x2-x1) - b1(x4-x3)
    D1 = B2*(b2.x - a1.x) - B1*(d4.x - c3.x)
    #D2 = b2*(y2-y1) - b1*(y4-y3)
    D2 = B2*(b2.y - a1.y) - B1*(d4.y - c3.y)
    
    X = D1/D
    Y = D2/D
    
    intersection_point = point(X,Y)
    
    return(intersection_point)


def oblique_line(radian,shape1_list,shape2_list):
    

    bias = []

    k = math.tan(radian)

    temp_list = list(set(shape1_list).union(set(shape2_list)))
    
    #print(temp_list)
    
    for i in range(len(temp_list)):
        
        X = temp_list[i][0]
        Y = temp_list[i][1]
        
        b_temp = Y - k*X
        
        bias.append(b_temp)
        

    min_bias = min(bias)
    max_bias = max(bias)
    
    #print(bias)
    

    sorted_shape_point_list = sorted(temp_list, key=itemgetter(0))

    x_left = sorted_shape_point_list[0][0] - 1
    x_right = sorted_shape_point_list[-1][0] + 1
    
    #shape1_list.append(shape1_list[0])
    #temp_shape1 = shape1_list
    #shape2_list.append(shape2_list[0])
    #temp_shape2 = shape2_list
    
    copy_shape1 = shape1_list.copy()
    copy_shape1.append(shape1_list[0])
    temp_shape1 = copy_shape1
    #print(temp_shape1)
    
    copy_shape2 = shape2_list.copy()
    copy_shape2.append(shape2_list[0])
    temp_shape2 = copy_shape2
    

    bias_contact_two_shape = []
    

    for j in range(len(bias)):
        

        y_left = k * x_left + bias[j]
        y_right = k * x_right + bias[j]
        
        #print(temp_shape1)
        
        shape1_intersection_point = 0
        shape2_intersection_point = 0
        
        for i_1 in range(len(temp_shape1)-1):
            
            point1_l1 = point(x_left,y_left)
            point1_l2 = point(x_right,y_right)
            
            point1_S1 = point(temp_shape1[i_1][0],temp_shape1[i_1][1])
            point1_S2 = point(temp_shape1[i_1+1][0],temp_shape1[i_1+1][1])
            
            if IsIntersec(point1_l1,point1_l2,point1_S1,point1_S2):
                
                shape1_intersection_point = shape1_intersection_point + 1 
                
        for i_2 in range(len(temp_shape2)-1):
            
            point2_l1 = point(x_left,y_left)
            point2_l2 = point(x_right,y_right)
            
            point2_S1 = point(temp_shape2[i_2][0],temp_shape2[i_2][1])
            point2_S2 = point(temp_shape2[i_2+1][0],temp_shape2[i_2+1][1])
            
            if IsIntersec(point2_l1,point2_l2,point2_S1,point2_S2):
                
                shape2_intersection_point = shape2_intersection_point + 1
        

        if shape1_intersection_point > 0 and shape2_intersection_point > 0:
            
            bias_contact_two_shape.append(bias[j])
            
            #print(shape1_intersection_point,shape2_intersection_point)
    

    return(bias_contact_two_shape,k)


def intersection_of_line(slope,bias,shape1_list,shape2_list):
    

    copy_shape1 = shape1_list.copy()
    copy_shape1.append(shape1_list[0])
    temp_shape1 = copy_shape1
    #print(temp_shape1)
    
    copy_shape2 = shape2_list.copy()
    copy_shape2.append(shape2_list[0])
    temp_shape2 = copy_shape2
    

    temp_list = list(set(shape1_list).union(set(shape2_list)))

    sorted_shape_point_list = sorted(temp_list, key=itemgetter(0))

    x_left = sorted_shape_point_list[0][0] - 1
    x_right = sorted_shape_point_list[-1][0] + 1
    

    y_left = slope * x_left + bias
    y_right = slope * x_right + bias
    
    
    ##########################shape1#######################
    shape1_intersect_list = []
    
    distance1 = 0
    
    for i_1 in range(len(temp_shape1)-1):
            
        point1_l1 = point(x_left,y_left)
        point1_l2 = point(x_right,y_right)
        
        point1_S1 = point(temp_shape1[i_1][0],temp_shape1[i_1][1])
        point1_S2 = point(temp_shape1[i_1+1][0],temp_shape1[i_1+1][1])
        
        #print(point1_l1,point1_l2,point1_S1,point1_S2)
        #print(IsIntersec(point1_l1,point1_l2,point1_S1,point1_S2))
        
        #print(point1_S2.y-point1_S1.y)
        #print(point1_S2.x-point1_S1.x)
        
        if (point1_S2.x-point1_S1.x) == 0:
            
            if math.atan(slope) == 0.5*math.pi:
            
                continue;
            
        elif slope == (point1_S2.y-point1_S1.y)/(point1_S2.x-point1_S1.x):
            
            continue;
        
        if IsIntersec(point1_l1,point1_l2,point1_S1,point1_S2):
            
            intersect_point1 = intersection_distance(point1_l1,point1_l2,point1_S1,point1_S2)
        
            if intersect_point1 in shape1_intersect_list:
            
                continue;
        
            else:
        
                shape1_intersect_list.append(intersect_point1)
    #print(shape1_intersect_list)    
    if (len(shape1_intersect_list))%2==0:
        
        for i_11 in range(int(len(shape1_intersect_list)/2)):
            
            X1 = shape1_intersect_list[2*i_11].x
            Y1 = shape1_intersect_list[2*i_11].y
            X2 = shape1_intersect_list[2*i_11+1].x
            Y2 = shape1_intersect_list[2*i_11+1].y
            
            distance1 = distance1 + calculatelength(X1,Y1,X2,Y2)
            
    else :
        
        if len(shape1_intersect_list) == 1:
        
            distance1 = 0
        
        else :
            
            print("on the vertex")
    
    ##########################shape2#######################
    shape2_intersect_list = []
    
    distance2 = 0
    
    for i_2 in range(len(temp_shape2)-1):
            
        point2_l1 = point(x_left,y_left)
        point2_l2 = point(x_right,y_right)
        
        point2_S1 = point(temp_shape2[i_2][0],temp_shape2[i_2][1])
        point2_S2 = point(temp_shape2[i_2+1][0],temp_shape2[i_2+1][1])
        
        if (point2_S2.x-point2_S1.x) == 0:
            
            if math.atan(slope) == 0.5*math.pi:
            
                continue;
            
        elif slope == (point2_S2.y-point2_S1.y)/(point2_S2.x-point2_S1.x):
            
            continue;
        
        if IsIntersec(point2_l1,point2_l2,point2_S1,point2_S2):
        
            intersect_point2 = intersection_distance(point2_l1,point2_l2,point2_S1,point2_S2)
        
            if intersect_point2 in shape2_intersect_list:
            
                continue;
        
            else:
        
                shape2_intersect_list.append(intersect_point2)
        
    if (len(shape2_intersect_list))%2==0:
        
        for i_22 in range(int(len(shape2_intersect_list)/2)):
            
            X2_1 = shape2_intersect_list[2*i_22].x
            Y2_1 = shape1_intersect_list[2*i_22].y
            X2_2 = shape1_intersect_list[2*i_22+1].x
            Y2_2 = shape1_intersect_list[2*i_22+1].y
            
            distance2 = distance1 + calculatelength(X2_1,Y2_1,X2_2,Y2_2)
            
    else :
        
        if len(shape2_intersect_list) == 1:
        
            distance2 = 0
        
        else :
            
            print("on the vertex")
            
    return(distance1+distance2)


def intergrate_distance(angle_num,insert_num,shape1_list,shape2_list):
    
    distacne_list = []
    

    angle_vari = 2*math.pi/angle_num
    
    for i in range(angle_num):
        
        distance_temp = 0
        
        bias_list,k = oblique_line(i*angle_vari,shape1_list,shape2_list)
        
        #print(bias_list,k)
        

        if len(bias_list) <=1:
            
            distacne_list.append(0)
            
            continue;
            
        else:
            
            max_bias = max(bias_list)
            min_bias = min(bias_list)
        
            insert_vari = (max_bias - min_bias)/insert_num
            
            #print(insert_vari)
            Bias = (max_bias+min_bias)/2
            
            if judge_function(i*angle_vari,Bias,shape1_list,shape2_list):
        
                for j in range(insert_num):
            
                    temp_bias = min_bias + insert_vari * j 
            
                    distance_temp = distance_temp + intersection_of_line(k,temp_bias,shape1_list,shape2_list)
        
                distacne_list.append(distance_temp)
            
            else:
                
                distacne_list.append(0)
            
    return(distacne_list)


def judge_function(angle,bias,shape1_list,shape2_list):
    

    copy_shape1 = shape1_list.copy()
    copy_shape1.append(shape1_list[0])
    temp_shape1 = copy_shape1
    #print(temp_shape1)
    
    copy_shape2 = shape2_list.copy()
    copy_shape2.append(shape2_list[0])
    temp_shape2 = copy_shape2
    

    temp_list = list(set(shape1_list).union(set(shape2_list)))

    sorted_shape_point_list = sorted(temp_list, key=itemgetter(0))

    x_left = sorted_shape_point_list[0][0] - 1
    x_right = sorted_shape_point_list[-1][0] + 1
    
    slope = math.tan(angle)

    y_left = slope * x_left + bias
    y_right = slope * x_right + bias
    

    shape1_intersect_list = []
    
    distance1 = 0
    
    for i_1 in range(len(temp_shape1)-1):
        
        temp_intersect_point1 = [0,0]
            
        point1_l1 = point(x_left,y_left)
        point1_l2 = point(x_right,y_right)
        
        point1_S1 = point(temp_shape1[i_1][0],temp_shape1[i_1][1])
        point1_S2 = point(temp_shape1[i_1+1][0],temp_shape1[i_1+1][1])
        
        #print(point1_l1,point1_l2,point1_S1,point1_S2)
        #print(IsIntersec(point1_l1,point1_l2,point1_S1,point1_S2))
        
        #print(point1_S2.y-point1_S1.y)
        #print(point1_S2.x-point1_S1.x)
        
        if (point1_S2.x-point1_S1.x) == 0:
            
            if math.atan(slope) == 0.5*math.pi:
            
                continue;
            
        elif slope == (point1_S2.y-point1_S1.y)/(point1_S2.x-point1_S1.x):
            
            continue;
        
        if IsIntersec(point1_l1,point1_l2,point1_S1,point1_S2):
            
            intersect_point1 = intersection_distance(point1_l1,point1_l2,point1_S1,point1_S2)
        
            if intersect_point1 in shape1_intersect_list:
            
                continue;
        
            else:
                
                temp_intersect_point1[0] = intersect_point1.x
                temp_intersect_point1[1] = intersect_point1.y
        
                shape1_intersect_list.append(temp_intersect_point1)
            

    shape2_intersect_list = []
    
    distance2 = 0
    
    for i_2 in range(len(temp_shape2)-1):
        
        temp_intersect_point2 = [0,0]
            
        point2_l1 = point(x_left,y_left)
        point2_l2 = point(x_right,y_right)
        
        point2_S1 = point(temp_shape2[i_2][0],temp_shape2[i_2][1])
        point2_S2 = point(temp_shape2[i_2+1][0],temp_shape2[i_2+1][1])
        
        if (point2_S2.x-point2_S1.x) == 0:
            
            if math.atan(slope) == 0.5*math.pi:
            
                continue;
            
        elif slope == (point2_S2.y-point2_S1.y)/(point2_S2.x-point2_S1.x):
            
            continue;
        
        if IsIntersec(point2_l1,point2_l2,point2_S1,point2_S2):
        
            intersect_point2 = intersection_distance(point2_l1,point2_l2,point2_S1,point2_S2)
        
            if intersect_point2 in shape2_intersect_list:
            
                continue;
        
            else:
                
                temp_intersect_point2[0] = intersect_point2.x
                temp_intersect_point2[1] = intersect_point2.y
        
                shape2_intersect_list.append(temp_intersect_point2)
    

    sort_a_x = sorted(shape1_intersect_list, key=itemgetter(0))
    sort_a_y = sorted(shape1_intersect_list, key=itemgetter(1))
    
    #print(sort_a_x,sort_a_y)
    
    max_a_x = sort_a_x[-1][0]
    min_a_x = sort_a_x[0][0]
    max_a_y = sort_a_x[-1][1]
    min_a_y = sort_a_x[0][1]
    
    sort_b_x = sorted(shape2_intersect_list, key=itemgetter(0))
    sort_b_y = sorted(shape2_intersect_list, key=itemgetter(1))
    max_b_x = sort_b_x[-1][0]
    min_b_x = sort_b_x[0][0]
    max_b_y = sort_b_x[-1][1]
    min_b_y = sort_b_x[0][1]
    
    #print(min_a_x,max_a_x)
    
    
    
    judge_result = 0
    

    if angle<(math.pi*0.5) and angle>=0:
        
        if min_a_x < min_b_x:
            
            judge_result = 1
            
    elif angle<(math.pi) and angle>=math.pi*0.5:
        
        if min_a_y < min_b_y:
            
            judge_result = 1
            
    elif angle<(math.pi*1.5) and angle>=(math.pi):
        
        if min_a_x > min_b_x:
            
            judge_result = 1
    
    elif angle<(math.pi*2) and angle>=math.pi*1.5:
        
        if min_a_y > min_b_y:
            
            judge_result = 1
    
    return(judge_result)

   
def azimuth_angle(shape_argument,shape_reference):

    f_histogram = intergrate_distance(360,100,shape_argument,shape_reference)
    
    x_list= []
    y_list= []
    
    for i in range(len(f_histogram)):
        
        radian = math.radians(i)
        
        if f_histogram[i] == 0:
            
            continue;
            
        else:
            


            temp_x = f_histogram[i] * math.cos(radian)
            temp_y = f_histogram[i] * math.sin(radian)
            
            x_list.append(temp_x)
            y_list.append(temp_y)
        
    sum_x = sum(x_list)
    sum_y = sum(y_list)
    

    if sum_x > 0 and sum_y > 0:
        
        azi_angle = math.atan(sum_x/sum_y)
    

    elif sum_x < 0 and sum_y > 0:
        
        azi_angle =  math.pi + math.atan(sum_x/sum_y) 
        

    elif sum_x < 0 and sum_y < 0:
        
        azi_angle =  math.pi + math.atan(sum_x/sum_y)
        

    elif sum_x > 0 and sum_y < 0:
        
        azi_angle = 2 * math.pi + math.atan(sum_x/sum_y)
        
    return(azi_angle)