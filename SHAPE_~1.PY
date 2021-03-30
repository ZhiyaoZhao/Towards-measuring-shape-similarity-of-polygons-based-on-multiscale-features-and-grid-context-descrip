import math


def clock_wise(point1):
    
    vector_a = point1[1]
    
    vector_b =  point1[0]
    

    vector_east = [1,0]
    

    mo_vector_a = math.sqrt(math.pow(vector_a[0],2)+math.pow(vector_a[1],2))
    mo_vector_b = math.sqrt(math.pow(vector_b[0],2)+math.pow(vector_b[1],2))
    
    mo_vector_east = math.sqrt(math.pow(vector_east[0],2)+math.pow(vector_east[1],2))
    
    cosin_angle_1 = ((vector_a[0]*vector_east[0]+vector_a[1]*vector_east[1]))/(mo_vector_a*mo_vector_east)
    cosin_angle_2 = ((vector_b[0]*vector_east[0]+vector_b[1]*vector_east[1]))/(mo_vector_b*mo_vector_east)
    
    angle_1 = math.acos(cosin_angle_1)
    
    angle_2 = math.acos(cosin_angle_2)
    
    new_rank = []
    
    if angle_1 < angle_2:
        
        new_rank.append(point1[0])
        
        index = len(point1)-1
        
        for i in range(0,len(point1)-1):
            
                new_rank.append(point1[index-i])
                
    else :
        
        new_rank = point1
        
    return(new_rank);

#######
def add_tail(new_rank):
    
    new_rank.append(new_rank[0])
    
    return(new_rank);

#######

def region_1(point_xa,point_yb):
    
    moment = []
    
    moment_00_1 = (1/2)*point_xa*point_yb
    
    moment.append(moment_00_1)
    
    moment_01_1 = (1/6)*point_xa*math.pow(point_yb,2)
    
    moment.append(moment_01_1)
    
    moment_10_1 = (1/3)*math.pow(point_xa,2)*point_yb
    
    moment.append(moment_10_1)
    
    moment_11_1 = (1/8)*math.pow(point_xa,2)*math.pow(point_yb,2)
    
    moment.append(moment_11_1)
    
    moment_02_1 = (1/12)*point_xa*math.pow(point_yb,3)
    
    moment.append(moment_02_1)
    
    moment_20_1 = (1/4)*math.pow(point_xa,3)*point_yb
    
    moment.append(moment_20_1)
    
    return(moment);

def region_2(point_xa,point_yb,point_xc,point_yd):
    
    a = point_xa
    
    b = point_yb
    
    c = point_xc
    
    d = point_yd
    
    moment = []
    
    moment_00_2 = (1/2)*(c - a)*(b + d)
    
    moment.append(moment_00_2)
    
    moment_01_2 = (1/6)*(c - a)*(math.pow(d,2)+d*b+math.pow(b,2))
    
    moment.append(moment_01_2)
    
    moment_10_2 = ((1/3)*(d-b)*(math.pow(c,2)+a*c+math.pow(a,2))+(1/2)*(b*c-a*d)*(c+a))
    
    moment.append(moment_10_2)
    
    if b==d:
        
        moment_11_2 = (1/4)*math.pow(b,2)*(math.pow(c,2)-math.pow(a,2))
        
        moment.append(moment_11_2)
        
    else :
        
        moment_11_2 = (1/(24*(d-b)))*(3*math.pow((c-a),2)*((math.pow(d,3)+b*math.pow(d,2))+math.pow(b,2)*d+math.pow(b,3))-4*(b*c-a*d)*(c-a)*(math.pow(d,2)+b*d+math.pow(b,2)))
        
        moment.append(moment_11_2)
        
    moment_02_2 = (1/12)*(c-a)*(math.pow(d,3)+b*math.pow(d,2)+math.pow(b,2)*d+math.pow(b,3))
    
    moment.append(moment_02_2)
    
    moment_20_2 = (1/4)*(d-b)*(math.pow(c,3)+a*math.pow(c,2)+math.pow(a,2)*c+math.pow(a,3))+(1/3)*(b*c-a*d)*(math.pow(c,2)+a*c+math.pow(a,2))
    
    moment.append(moment_20_2)
    
    return(moment);

def region_3(point_xc,point_yd):
    
    moment = []
    
    moment_00_3 = (1/2)*point_xc*point_yd
    
    moment.append(moment_00_3)
    
    moment_01_3 = (1/6)*point_xc*math.pow(point_yd,2)
    
    moment.append(moment_01_3)
    
    moment_10_3 = (1/3)*math.pow(point_xc,2)*point_yd
    
    moment.append(moment_10_3)
    
    moment_11_3 = (1/8)*math.pow(point_xc,2)*math.pow(point_yd,2)
    
    moment.append(moment_11_3)
    
    moment_02_3 = (1/12)*point_xc*math.pow(point_yd,3)
    
    moment.append(moment_02_3)
    
    moment_20_3 = (1/4)*math.pow(point_xc,3)*point_yd
    
    moment.append(moment_20_3)
    
    return(moment);

def triangle_T_moment(point_xa,point_yb,point_xc,point_yd):
    
    a = point_xa
    
    b = point_yb
    
    c = point_xc
    
    d = point_yd
    
    moment_1 = region_1(a,b)
    
    moment_2 = region_2(a,b,c,d)
    
    moment_3 = region_3(c,d)
    
    moment_T = []
    
    for i in range(0,6):
        
        moment = 0
        
        moment = abs(moment_1[i] + moment_2[i] - moment_3[i])
        
        moment_T.append(moment)
        
    return(moment_T);

def sign_of_triangle_t(point_xa,point_yb,point_xc,point_yd):
    
    vector_a = [point_xa,point_yb]
    
    vector_b = [point_xc,point_yd]
 
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
        
    return(sign);

def moment_shape(points):
    
    '''
    moment = [0,0,0,0,0,0]
    
    points=add_tail(points)
    
    for i in range(len(points)-1):
        
        a = points[i][0]
        b = points[i][1]
        c = points[i+1][0]
        d = points[i+1][1]
        
        moment_T =[]
        
        moment_T = triangle_T_moment(a,b,c,d)
        
        signs = 0
        
        signs = sign_of_triangle_t(a,b,c,d)
        
        #print(signs)
        
        for j in range(0,6,1):
            
            moment[j] = moment[j] + signs*moment_T[j]
            
            #print(moment[j])
    '''
#####

    moment = [0,0,0,0,0,0]

    
    for j in range(0,6):
        
        for i in range(len(points)):
            
            if i < (len(points)-1):
        
                a = points[i][0]
                b = points[i][1]
                c = points[i+1][0]
                d = points[i+1][1]

                
            else:
                
                a = points[len(points)-1][0]
                b = points[len(points)-1][1]
                c = points[0][0]
                d = points[0][1]
            
            moment_T =[]
        
            moment_T = triangle_T_moment(a,b,c,d)
            
            signs = 0
        
            signs = sign_of_triangle_t(a,b,c,d)
            
            #print(signs)
            
            moment[j] = moment[j] + signs*moment_T[j]
            
    
            
    #print(moment)        
            
    return(moment);
        
def main_angle_of_shape(moment):
    
    miu_11_s = (moment[1]*moment[2])/moment[0]
    
    miu_02_s = (moment[1]*moment[1])/moment[0]
    
    miu_20_s = (moment[2]*moment[2])/moment[0]
    
    yita11 = miu_11_s/math.pow(moment[0],2)
    
    yita20 = miu_20_s/math.pow(moment[0],2)
    
    yita02 = miu_02_s/math.pow(moment[0],2)
    
    hu1 = yita20+yita02
    
    hu2 = math.pow((yita20-yita02),2)+4*math.pow(yita11,2)
    
    if miu_02_s == miu_20_s:
        
        angle = (math.pi/4)
        
    else:
    
        angle = (1/2)*math.atan((2*miu_11_s)/(miu_20_s-miu_02_s))
    
        
    #####
    
    
    grivate_x = moment[2]/moment[0]
    
    grivate_y = moment[1]/moment[0]
    
    a = (moment[5]/moment[0])-math.pow(grivate_x,2) 
    
    b = 2*((moment[3]/moment[0])-grivate_x*grivate_y)
    
    c = (moment[4]/moment[0])-math.pow(grivate_y,2) 
    
    if a == c:
        
        angle1 = (math.pi/4)
        
    else:
    
        angle1 = (1/2)*math.atan(b/(a-c))
               
    I_min = ( miu_20_s+miu_02_s-math.sqrt(4*math.pow(miu_11_s,2)+math.pow(miu_20_s-miu_20_s,2)))/2
    
    I_max = ( miu_20_s+miu_02_s+math.sqrt(4*math.pow(miu_11_s,2)+math.pow(miu_20_s-miu_20_s,2)))/2
    
    #return(angle,angle1,I_min,I_max,grivate_x,grivate_y,hu1,hu2);
    return(angle1);
def grivate_point(point):
    
    #grivate_x = moment[2]/moment[0]
    
    #grivate_y = moment[1]/moment[0]
    
    sum_x = 0
    
    sum_y = 0
    
    for i in range(len(point)):
        
        sum_x = sum_x + point[i][0]
        
        sum_y = sum_y + point[i][1]
    
    point_gravity = [0,0]
    
    point_gravity[0] = sum_x/len(point)
    
    point_gravity[1] = sum_y/len(point)
    
    return(point_gravity);
