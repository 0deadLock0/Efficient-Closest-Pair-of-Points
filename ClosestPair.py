"""
Efficient Closest Pair of Points in a Plane

Time Complexity: O(nlog^2(n))
Reference: https://www.cs.mcgill.ca/~cs251/ClosestPair/ClosestPairDQ.html
"""


import math
import random

#Helper Functions:
def SorT(l):
    if l==[]:
        return []
    s=len(l)
    if s==1:
        return l
    else:
        m=s//2
        sl1=[l[i] for i in range(s) if l[i]<l[m]]
        sl2=[l[i] for i in range(s) if l[i]>=l[m] and i!=m]
        return SorT(sl1) + [l[m]] + SorT(sl2)


#Main Functions:
def dist(p1, p2):
    """Find the euclidean distance between two 2-D points
        Args:
         p1: (p1_x, p1_y)
         p2: (p2_x, p2_y)
        Returns:
         Euclidean distance between p1 and p2
    """
    return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**0.5


def sort_points_by_X(points):
    """Sort a list of points by their X coordinate
        Args:
         points: List of points [(p1_x, p1_y), (p2_x, p2_y), ...]
        Returns:
         List of points sorted by X coordinate
    """
    points=SorT(points)
    return points


def sort_points_by_Y(points):
    """Sort a list of points by their Y coordinate
        Args:
         points: List of points [(p1_x, p1_y), (p2_x, p2_y), ...]
        Returns:
         List of points sorted by Y coordinate 
    """
    points=[points[i][::-1] for i in range(len(points))]
    points=SorT(points)
    points=[points[i][::-1] for i in range(len(points))]
    return points


def naive_closest_pair(plane):
    """Find the closest pair of points in the plane using the brute
       force approach
        Args:
         plane: List of points [(p1_x, p1_y), (p2_x, p2_y), ...]
        Returns:
         Distance between closest pair of points and closest pair 
         of points: [dist_bw_p1_p2, (p1_x, p1_y), (p2_x, p2_y)]
    """
    closet_pair=[dist(plane[0],plane[1]),plane[0],plane[1]]
    for p1 in plane:
        for p2 in plane[plane.index(p1)+1:]:
            if dist(p1,p2)<closet_pair[0]:
                closet_pair=[dist(p1,p2),p1,p2]
    return closet_pair


def closest_pair_in_strip(points, d):
    """Find the closest pair of points in the given strip with a 
       given upper bound. This function is called by 
       efficient_closest_pair_routine
        Args:
         points: List of points in the strip of interest.
         d: Minimum distance already found found by 
            efficient_closest_pair_routine
        Returns:
         Distance between closest pair of points and closest pair 
         of points: [dist_bw_p1_p2, (p1_x, p1_y), (p2_x, p2_y)] if
         distance between p1 and p2 is less than d. Otherwise
         return -1.
    """
    l=(points[0][-1][0]+points[1][0][0])/2
    new_points=[[],[]]
    for p in points[0]:
        if l-p[0]<d:                
            new_points[0].append(p)
    for p in points[1]:
        if p[0]-l<d:                
            new_points[1].append(p)
    if len(new_points[0])<1 or len(new_points[1])<1:
        return -1
    else:
        points=[]
        for p in new_points[0]:
            points.append(p)
        for p in new_points[1]:
            points.append(p)
        s=len(points)
        ds=[d]
        points=sort_points_by_Y(points)   
        for i in range(s):
            n=min(5,s-1-i)
            for j in range(i+1,i+n+1):
                dn=dist(points[i],points[j])
                if dn<ds[0]:
                    ds=[dn,points[i],points[j]]
        if ds[0]!=d:
            return ds
        else:
            return -1


def efficient_closest_pair_routine(points):
    """This routine calls itself recursivly to find the closest pair of
       points in the plane. 
        Args:
         points: List of points sorted by X coordinate
        Returns:
         Distance between closest pair of points and closest pair 
         of points: [dist_bw_p1_p2, (p1_x, p1_y), (p2_x, p2_y)]
    """
    l=len(points)
    if l<2:
        return [float('inf')] 
    elif l==2:
        return [dist(points[0],points[1]),points[0],points[1]]
    else:
        d1=efficient_closest_pair_routine(points[:l//2])
        d2=efficient_closest_pair_routine(points[l//2:])
        d=min(d1,d2)
        ds=closest_pair_in_strip([points[:l//2]]+[points[l//2:]],d[0])
        if ds==-1:
            return d
        else:
            return ds


def efficient_closest_pair(points):
    """Find the closest pair of points in the plane using the divide
       and conquer approach by calling efficient_closest_pair_routine.
        Args:
         plane: List of points [(p1_x, p1_y), (p2_x, p2_y), ...]
        Returns:
         Distance between closest pair of points and closest pair 
         of points: [dist_bw_p1_p2, (p1_x, p1_y), (p2_x, p2_y)]
    """
    points=sort_points_by_X(points)
    return efficient_closest_pair_routine(points)


def generate_plane(plane_size, num_pts):
    """Function to generate random points.
        Args:
         plane_size: Size of plane (X_max, Y_max)
         num_pts: Number of points to generate
        Returns:
         List of random points: [(p1_x, p1_y), (p2_x, p2_y), ...]
    """
    gen = random.sample(range(plane_size[0]*plane_size[1]), num_pts)
    random_points = [(i%plane_size[0] + 1, i//plane_size[1] + 1) for i in gen]
    return random_points


if __name__ == "__main__":  
    num_pts = 10
    plane_size = (10, 10)
    plane = generate_plane(plane_size, num_pts)
    print(plane)
    print(naive_closest_pair(plane))
    print(efficient_closest_pair(plane))
