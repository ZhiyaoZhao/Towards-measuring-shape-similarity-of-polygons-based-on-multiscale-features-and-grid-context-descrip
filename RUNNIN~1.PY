#coding=utf-8

#including necessary package
import shapefile

import shape_similarity

#
interpolate_point = [1500,5000,10000]

#reading data
#####
#myshp = open("...\\shape similarity\\experimental data\\Similar polygons retrieving test\\Max_planck.shp", "rb")

#mydbf = open("...\\shape similarity\\experimental data\\Similar polygons retrieving test\\Max_planck.dbf", "rb")
#####
#myshp = open("...\\shape similarity\\experimental data\\Similar polygons retrieving test\\Hasenbergl.shp", "rb")

#mydbf = open("...\\shape similarity\\experimental data\\Similar polygons retrieving test\\Hasenbergl.dbf", "rb")

#Atihua dataset
#####
myshp = open("...\\shape similarity\experimental data\\Comparison with TF method and Fourier descriptor\\atihuaCopy.shp", "rb")

mydbf = open("...\\shape similarity\experimental data\\Comparison with TF method and Fourier descriptor\\atihuaCopy.dbf", "rb")
#####

#The Victory lake and the church footprint prints
#####
#myshp = open("...\\shape similarity\\experimental data\\sensitivity test\\sensitivity test.shp", "rb")

#mydbf = open("...\\shape similarity\\experimental data\\sensitivity test\\sensitivity test.dbf", "rb")
#####


shapes = shapefile.Reader(shp=myshp, dbf=mydbf)

shapep = shapes.shapes()

recordp = shapes.records()

shape_list = []

for i in range(len(shapep)):

    dic = {'osmid':[],'code':[],'fclass':[],'name':[],'typee':[],'shapetype':[],'point':[],'bbox':[],'parts':[],}
    #shape recording
    dic['osmid'] = recordp[i][0]
    dic['shapetype'] = shapep[i].shapeType
    for j in range(len(shapep[i].points)):
        dic.setdefault('point',[]).append(shapep[i].points[j])
    dic['bbox'] = shapep[i].bbox
    dic['parts'] = shapep[i].parts
    
    if (len(shapep[i].points)) > 2:
               
        shape_list.append(dic);
            
for j in range(len(shape_list)):
    
    point1 = shape_list[j]['point']
    
    delet_point_index_list = []
    
    part_list = list(shapep[j].parts)

    part_list.append(len(point1)-1)

    delet_count = 0