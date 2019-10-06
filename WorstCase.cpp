#include <iostream>
#include <string>
#include <cstring>
using namespace std;

void maxi(int arr[],int f, int l)
{
    int max,it,tmp;
    max=arr[f];
    it=f;
    for (int i=f;i<l-1;i++)
    {
        if(arr[i]<arr[i+1])
        {
            swap(arr[i],arr[i+1]);
            max=arr[i];
        }
    }
    //tmp=arr[(f+l)/2];
    //arr[(f+l)/2]=max;
    //arr[it]=tmp;
}
int main()
{
    int n;
    cin>>n;

    int *t=new int[n];
    for(int i=0;i<n;i++)
    {
        t[i]=i+1;
    }
    maxi(t,0,n);
    for(int i=0;i<n;i++)
    {
        cout<<t[i]<<" ";
    }

    return 0;
}
