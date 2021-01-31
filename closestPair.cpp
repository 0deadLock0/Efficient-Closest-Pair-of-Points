/*
Distance between Closest Pair of points in 2D plane
Complexity: O(n.logn)
Reference: https://www.geeksforgeeks.org/closest-pair-of-points-onlogn-implementation/ 
*/

#include <iostream>
#include <vector>
#include <utility>
#include <cmath>
#include <algorithm>
#include <cstdlib>
#include <ctime>
#include <cfloat>

using namespace std;

bool compareByY(const pair<int,int> &point1,const pair<int,int> &point2)
{
	if(point1.second<point2.second)
		return true;
	else if(point1.second==point2.second && point1.first<=point2.first)
		return true;
	else
		return false;
}

double getSquared(int num)
{
	return num*num;
}

double euclideanDistance(const pair<int,int> &point1,const pair<int,int> &point2)
{
	return sqrt(getSquared(point1.first-point2.first)+getSquared(point1.second-point2.second));
}

double stripDistance(pair<int,int> xMiddle,const vector<pair<int,int>> &pointsByY,double stripWidth)
{
	vector<pair<int,int>> stripPoints;
	for(const pair<int,int> &p:pointsByY)
	{
		if(abs(p.first-xMiddle.first)<=stripWidth)
			stripPoints.push_back(p);
	}
	if(stripPoints.empty())
		return DBL_MAX;
	double minDistance=DBL_MAX;
	int n=stripPoints.size();
	for(int i=0;i<n;++i)
	{
		int k=min(7,n-i-1);
		for(int j=1;j<=k;++j)
		{
			double distance=euclideanDistance(stripPoints[i],stripPoints[i+j]);
			minDistance=min(minDistance,distance);
		}
	}
	return minDistance;
}

double closestPairDistance(vector<pair<int,int>>::iterator xBegin,vector<pair<int,int>>::iterator xEnd,const vector<pair<int,int>> &pointsByY)
{
	if(xBegin==xEnd)
		return DBL_MAX;
	else if(xBegin+1==xEnd)
		return DBL_MAX;
	else if(xBegin+2==xEnd)
		return euclideanDistance(*xBegin,*(xBegin+1));

	vector<pair<int,int>>::iterator xMiddle=xBegin+(xEnd-xBegin)/2;
	double minDistanceL=closestPairDistance(xBegin,xMiddle,pointsByY);
	double minDistanceR=closestPairDistance(xMiddle,xEnd,pointsByY);

	double minDistance=min(minDistanceL,minDistanceR);
	double minDistanceStrip=stripDistance(*xMiddle,pointsByY,minDistance);
	minDistance=min(minDistance,minDistanceStrip);

	return minDistance;
}

double closestPairDistance(const vector<pair<int,int>> &points)
{
	vector<pair<int,int>> pointsByX(points.begin(),points.end());
	vector<pair<int,int>> pointsByY(points.begin(),points.end());

	sort(pointsByX.begin(),pointsByX.end());
	sort(pointsByY.begin(),pointsByY.end(),compareByY);

	return closestPairDistance(pointsByX.begin(),pointsByX.end(),pointsByY);
}

double closestPairDistanceBruteForce(const vector<pair<int,int>> &points)
{
	int n=points.size();
	double minDistance=DBL_MAX;
	for(int i=0;i<n;++i)
	{
		for(int j=i+1;j<n;++j)
		{
			double distance=euclideanDistance(points[i],points[j]);
			minDistance=min(minDistance,distance);
		}
	}
	return minDistance;
}

vector<pair<int,int>> getPoints(int n,int w,int h)
{
	int s=w*h;
	vector<int> sampleSpace(s);
	for(int i=0;i<s;++i)
		sampleSpace[i]=i;
	random_shuffle(sampleSpace.begin(),sampleSpace.end());
	
	vector<pair<int,int>> randomPoints(n);
	for(int i=0;i<n;++i)
		randomPoints[i]=make_pair(sampleSpace[i]%w+1,sampleSpace[i]/h+1);

	return randomPoints;
}

int main()
{
	srand(time(NULL));

	const int n=100;
	const int planeWidth=n*10;
	const int planeHieght=n*10;

	vector<pair<int,int>> points=getPoints(n,planeWidth,planeHieght);

	double bfMin=closestPairDistanceBruteForce(points);
	double dcMin=closestPairDistance(points);
	
	for(const pair<int,int> &p:points)
		cout<<"("<<p.first<<" "<<p.second<<") ";
	cout<<"\n";

	cout<<"BruteForce: "<<bfMin<<"\n";
	cout<<"Divide and Conquer: "<<dcMin<<"\n";

	return 0;
}