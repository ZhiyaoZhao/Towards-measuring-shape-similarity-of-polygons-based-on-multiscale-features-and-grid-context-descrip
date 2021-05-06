# codeshare

This repository is used for maintaining the FAIR ( find-able, accessible, inter-operable, and reusable) data project

#Notice
1. To read and write shapefile，we used the Pyshp(shapefile.py) that is contributed by karimbahgat and his team. You can find the source code from https://github.com/GeospatialPython/pyshp.

2. If there is some error such as "No module named 'new_point_rank'",when you are running the code. You can add the full path of file(new_point_rank.py) to the directories list. 
## Example
    >>>import sys
    >>>sys.path
    >>>sys.path.append("..\\")#the full path of the folder

#Introduce

1.You can use shape_similarity.py to calculate the shape similarity between two polygons.

2.There are three experimental datasets to test this approach.

#Usage

1. If you have installed Anaconda, you could use your Jupyter Notebook to open the ipynb file named Running_test. If you don't have Jupyter, you could use your Python complier to open the 
py file named Running_test.

2. When you open the script file, the first step is to adjust your data path according to your save path.

3. The second step is to input opreation order in the console, such as "shape_similarity.shape_similarity_mut(shape_list[0],shape_list[1],interpolate_point)". 

4. If you want to calculate shape similarity betwent the first polygon and the sixth polygon, you could input "shape_similarity.shape_similarity_mut(shape_list[0],shape_list[5],interpolate_point)".

#REFERENCE:

If you use this work in your research, please reference this paper:

--------------------------------------------------------------------------------
 Fan, Hongchao; Zhao, Zhiyao; Li, Wenwen. 2021. "Towards Measuring Shape Similarity of Polygons Based on Multiscale Features and Grid Context Descriptors"
 ISPRS Int. J. Geo-Inf. 10, no. 5: 279. https://doi.org/10.3390/ijgi10050279
