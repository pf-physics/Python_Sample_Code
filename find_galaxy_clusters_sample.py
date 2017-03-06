# -*- coding: utf-8 -*-
"""
Created on Mon Feb 06 23:31:47 2017

@author: Sacha Perry-Fagant

The purpose of this file is look at a large file of galaxies and assign them
to the cluster that they are closest to.
The coordinates of the galaxies must be compared using a specific formula and
Some of the coordinates have to be converted before they are used.
Result: ClusterList, a list of Cluster objects, each has a list of Galaxy objects.
The data set containing the galaxies should be in the float/double format.
The list of clusters should be in the format of string (This facilitates the unit conversion)
"""
import numpy as np
from collections import namedtuple
#Info is all the original data held in the file for that cluster. In case it must be accessed later
class Cluster(object):
    def __init__(self,ra,dec,index,info):
        self.ra=ra
        self.dec=dec
        self.info=info
        self.index=index
        self.galaxies=[]

#Info is all the original data held in the file
class Galaxy(object):
        def __init__(self,index,distance,cluster,info):
            self.info=info
            self.index=index
            self.cluster=cluster
            self.distance=distance

#Converts from degrees, minutes, seconds to radians
def dms_to_radians(d):    
    rad= (float(d[0])+float(d[1])/60+float(d[2])/3600)*np.pi/180
    return rad

#Converts from hours minutes seconds to radians
def hours_to_radians(d):    
    rad= np.pi/180*(float(d[0])*15+float(d[1])/4+float(d[2])/240)
    return rad



#Takes as input the original cluster data
#Fills cluster list with cluster objects
def findClusters(allClusters):
    clusterList=[]
    for i in range(len(allClusters)):
        data=allClusters[i]
        ra=hours_to_radians(data[1].split(":"))
        dec=dms_to_radians(data[2].split(":"))
        cluster = Cluster(ra,dec,index=i,info=data)
        clusterList.append(cluster)
    return clusterList


#Finds the cluster index closest to the given galaxy and the distance
#Takes in radians
def findDistance(ra1,ra2,dec1,dec2):
    result = np.sin(dec1)*np.sin(dec2)+np.cos(dec1)*np.cos(dec2)*np.cos(ra1-ra2)
    return np.arccos(result)

#given coordinates, it finds the cloest cluster
#It returns the cluster's index, and the distance to that cluster
Result = namedtuple('Result', ['cluster', 'distance'])
def findClosest(ra1,dec1):
    ra2=clusterList[0].ra
    dec2=clusterList[0].dec
    minD=findDistance(ra1,ra2,dec1,dec2)
    minCluster=0
    i=0
    for x in clusterList:
        ra2=x.ra
        dec2=x.dec            
        dist=findDistance(ra1,ra2,dec1,dec2)
        if minD>dist:
            minD=dist
            minCluster=i
        i+=1
    r= Result(minCluster, minD)
    return r

'''
galaxyList is all the galaxies with the values converted to floats/decimals.
Assumes the ra/dec values are in degrees and need to be converted to radians
Simply assigns every galaxy to a cluster.
'''
def assignGalaxies():
    for i in range(len(galaxyList)):
        x=galaxyList[i]
        ra=float(x[0])/180*np.pi #converting to radians
        dec=float(x[1])/180*np.pi
        info=findClosest(ra,dec)
        index=info.cluster #The index of the cluster
        distance=info.distance #The distance to the cluster
        cluster=clusterList[index]
        galaxy=Galaxy(index=i,cluster=cluster,distance=distance,info=x)
        cluster.galaxies.append(galaxy)
        #Appends the galaxy to the cluster it belongs to 


#Put whatever you've named the file with the clusters
#It takes in the original cluster info, values are strings
clusterList=findClusters(LOCKMAN_zI1)
assignGalaxies()