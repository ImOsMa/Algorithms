#include <iostream>
#include <vector>
#include <algorithm>
#include <math.h>
#include <cmath>
#include <stdio.h>
using namespace std;

float maximum(float *arr, int size)
{
   float max;
   max = arr[0];
   for(int i=0; i<size; i++)
    {
        if(arr[i]>max)
        {
            max = arr[i];
        }
    }
  return max;
}
float minimum(float *arr, int size)
{
   float min;
   min = arr[0];
   for(int i=0; i<size; i++)
    {
        if(arr[i]<min)
        {
            min = arr[i];
        }
    }
  return min;
}


// Driver program to test above functions
void bucketSort(float arr[], int n, float maxel, float minel)
{
    int flag,c,q;
    int counter=0;
    float range,p;
	range=maxel-minel;
	c=0;
	p=ceil(range/(2*n-1));
    // 1) Create n empty buckets
    float b[2*n][n];
    float m[2*n][n];
    int cou[2*n];

for(int i=0;i<2*n;i++)
    {
        for(int j=0;j<n;j++)
        {
            b[i][j]=-1000;
            m[i][j]=b[i][j];
        }
    }
    for (int i=0; i<n; i++)
    {
       float bi=(arr[i]-minel)/p;
       c=trunc(bi);
       b[c][i]=arr[i];
       m[c][i]=arr[i];
    }
for(int i=0;i<2*n;i++)
{
    counter=0;
    for(int j=0;j<n;j++)
    {
        if(m[i][j]==-1000)
            counter++;
    }
    if(counter==n)
        cou[i]=1;
}
    for(int i=0;i<2*n;i++)
    {
        do {
            flag=0;
            for(int j=0;j<n-1;j++)
        {
           if(b[i][j]>b[i][j+1])
           {
               swap(b[i][j],b[i][j+1]);
               flag=j;
            }

        }
        q=flag;

        }while(q);
     }

    // 4) Concatenate all buckets into arr[]
    int index = 0;
    for (int i = 0; i <2*n; i++)
    {
        if(cou[i]!=1)
        {
            cout<<"Bucket:"<<endl;
            for (int j = 0; j < n; j++)
        {
            if(m[i][j]!=-1000)
            {
                printf("%.2f ",m[i][j]);
            }
        }
        cout<<endl;
        cout<<"Sorted bucket:"<<endl;
        for(int j=0;j<n;j++)
        {
            if(b[i][j]!=-1000 )
            {
                arr[index++] = b[i][j];
                printf("%.2f ",b[i][j]);
            }
        }
        cout<<endl;
        cout<<endl;
        }
    }


}
int main()
{
    int n;
    cin>>n;
    float *arr=new float [n];
    for(int i=0;i<n;i++)
    {
        cin>>arr[i];
    }
    cout<<"Initial array:"<<endl;
    for(int i=0;i<n;i++)
    {
        printf("%.2f ",arr[i]);
    }
    cout<<endl;
    cout<<endl;
    bucketSort(arr, n,maximum(arr,n),minimum(arr,n));
    cout <<"Final array:\n";
    for (int i=0; i<n; i++)
    {
        printf("%.2f ",arr[i]);

    }
    return 0;
}
