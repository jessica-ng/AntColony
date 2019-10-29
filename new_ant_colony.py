import re
import random
import time
import numpy as np
from heapq import nlargest

print("Please enter file name")
filename=""
filename=input()
with open(filename) as file1:
    text = file1.read().replace('\n', '')
file1.close()
start=time.time()

#Functions for cleaning the text using regex
def cleaning():
    cleantext=re.findall("(?:\s|,)(\d+?\d*)",text)
    size=int(cleantext.pop(0))  
    cleantext = list(map(int,cleantext))
    return cleantext,size

cleantext,size=cleaning()

#Function for finding the distance between 2 cities
def find_distance_nodes(i,j,size,text):
    if i==j:
        return 0
    if i>j:
        [i,j]=[j,i]
    if i==1:
        return int(text[j-2])
    return int(text[int((((i-1)/2)*(size-1+size-i+1)))+j-i-1]) 

#Function for finding the distance of a path
def find_distance_path(path):
    size= len(path)
    total_distance=0
    for i in range(0,len(path)-1):
        total_distance = total_distance + find_distance_nodes(path[i],path[i+1],size-1,cleantext)
    return total_distance

#Function for choosing the next best node
def max_node(pheromone,h, current_node,size, path):
    maximum=0
    best_node=0
    for i in range(1,size+1):
        if i not in path:
            position=generate_array_position(current_node,i)
            result=pheromone[position]*h[position]**2
            if result>maximum or maximum==0:
                maximum=result
                best_node=i
    return best_node

#Function for calculating array position
def generate_array_position(i,j):
    if i>j:
        [i,j]=[j,i]
    if i==1:
        return int(j-2)
    return int((((i-1)/2)*(size-1+size-i+1)))+j-i-1

#Function for updating visibility matrix
def updating_visibility_matrix(current_city,h,P,array_size,size,path):
    j=current_city
    going_cities=[float(0)]*size
    for i in range(1,size+1):
        e=i-1
        if i not in path:
            if i>j:
                [i,j]=[j,i]
            if i!=j:
                going_cities[e]=P[int((((i-1)/2)*(size-1+size-i+1)))+j-i-1]*h[int((((i-1)/2)*(size-1+size-i+1)))+j-i-1]**2
    return going_cities

#Funtion for calculating the cumulative of the visiblity array 
def cumulative_going_cities(going_cities,size):
    cum_going_cities=going_cities
    for i in range(1,size):
        if cum_going_cities[i]!=0:
       
            for j in range(1,size):
                if i-j>-1 and cum_going_cities[i-j]!=0:
                    index=i-j
                    cum_going_cities[i]=cum_going_cities[index]+cum_going_cities[i]
                    break          
    return cum_going_cities

#Function that finds the best path in the iteration
def best_k_paths(distance):
    best_paths=np.argsort(distance)[:1]
    return best_paths[0]

#Function for updating the local pheromone
def update_local_pheromones(path,p,pheromones,Tzero):
    for i in range(0,len(path)-1):        
        num=generate_array_position(path[i],path[i+1])
        pheromones[num]=(1-0.1)*pheromones[num]+0.1*Tzero
    return pheromones

#Main function for ant colony system
def ant_colony(cleantext,size,number_of_ants,iterations):
    optimal_distance=0
    optimal_path=[]
    size_of_array=len(cleantext)
    nodes=list(range(1,size+1))
    nodes.append(1)
    lnn=find_distance_path(nodes)
    Tzero=1/(size*lnn)
    P=[Tzero]*size_of_array
    h=[1.0]*size_of_array
    #Initiating visibility matrix
    for i in range(0,len(cleantext)):
        if cleantext[i]!=0:
            h[i]=1/cleantext[i]
        else:
            h[i]=0
    for k in range(0,iterations):
        qzero=0.95
        ant=[]
        distance=[]
        #Loop to simulate n amouunt of ants finding their paths
        for i in range(0,number_of_ants):
            cities=list(range(1,size+1))      
            current_city = 1
            path=[]
            path.append(current_city)
            for i in range(0,size-1):
                going_cities=updating_visibility_matrix(current_city,h,P,size_of_array,size,path)
                sum_cum=sum(going_cities)
                for i in range(0,len(going_cities)):
                    if sum_cum==0:
                        going_cities[i]=0
                    else:
                        going_cities[i]=going_cities[i]/sum_cum
                cum_going_cities=cumulative_going_cities(going_cities,size)
                chance=random.uniform(0,1)
                if chance<=qzero:
                    next_node=max_node(P,h,current_city,size,path)
                    path.append(next_node)
                    current_city=next_node           
                elif chance>qzero:
                    copy=cum_going_cities.copy()
                    copy.append(chance)
                    copy.sort()
                    index=0
                    index=copy.index(chance)
                    current_city=cum_going_cities.index(copy[index+1])+1
                    path.append(current_city)            
            P=update_local_pheromones(path,0.1,P,Tzero)
            path.append(path[0])
            ant.append(path)
            path_distance=find_distance_path(path)
            distance.append(path_distance)
        index=best_k_paths(distance)
        best_paths=ant[index].copy()
        best_path_distance=find_distance_path(best_paths)
        if len(optimal_path)==0 or find_distance_path(best_paths)<optimal_distance:
            optimal_path=best_paths
            optimal_distance=find_distance_path(best_paths)
        #Update pheromone for path
        for j in range(0,1):
            path=ant[index]
            path_distance=find_distance_path(path)
            for i in range(0,len(path)-1):
                num=0
                num=generate_array_position(path[i],path[i+1])
                P[num]=(1-0.1)*P[num]+0.1*(1/path_distance)
    optimal=0
    optimal=find_distance_path(optimal_path)
    print('optimal', optimal)
    print(optimal_path)
    return

ant_colony(cleantext, size, 10, 6000)