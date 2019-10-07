#include <iostream>
#include <string>
#include <cstring>
#include <stdlib.h>
#include <ctime>
#include <cmath>
using namespace std;
const int nmax=1000;
void merge (int a[], int p, int q, int r)
{
    int n1=q-p+1;
    int n2=r-q;
    int L[n1];
    int M[n2];
    cout<<"Left part:";
    for(int i=0;i<n1;i++)
    {
        L[i]=a[p+i];
        cout<<L[i]<<" ";
    }
    cout<<endl;
    cout<<"Right part:";
    for(int j=0;j<n2;j++)
    {
        M[j]=a[q+1+j];
        cout<<M[j]<<" ";
    }
    cout<<endl;
    int i,j,k;
    i=0;
    j=0;
    k=p;
    while(i<n1 && j<n2)
    {
        if(L[i]<=M[j])
        {
            a[k]=L[i];
            i++;
        }else
        {
            a[k]=M[j];
            j++;
        }
        k++;
    }
    while(i<n1)
    {
        a[k]=L[i];
        i++;
        k++;
    }
    while(j<n2)
    {
        a[k]=M[j];
        j++;
        k++;
    }
    cout<<"Merged parts:";
    for(int i=p;i<=r;i++)
        cout<<a[i]<<" ";
    cout<<endl;
    cout<<endl;
}
void MergeSort(int a[],int p, int r)
{
    int q;
    if(p+1>r)
        return ;
       cout<<p<<"----p---"<<endl;
    cout<<r<<"----r---"<<endl;
    q=(p+r-1)/2;
    cout<<q<<"--it's q"<<endl;
    MergeSort(a,p,q);
    MergeSort(a,q+1,r);
    merge(a,p,q,r);
}


int main()
{
    int n;
    cin>>n;
    int *arr=new int[n];
    for(int i=0;i<n;i++)
        cin>>arr[i];
    MergeSort(arr,0,n);
    cout<<"After Sort:"<<endl;
    for(int i=0;i<n;i++)
        cout<<arr[i]<<" ";
    return 0;
}
