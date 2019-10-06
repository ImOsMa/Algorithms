#include <iostream>
#include <string>
#include <cstring>
using namespace std;
const int aSize = 16;
const char alph[aSize] = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'};
int getMax(string arr[],int n)
{
    string t;
    int maxn;
    t=arr[0];
    maxn=t.size();
    for(int i=0;i<n;i++)
    {
        t=arr[i];
       if(t.size()>maxn)
       {
           maxn=t.size();
       }
    }
    return maxn;
}



void CountSort(string arr[],int n,int c)
{
    int k,t;
    int ind[aSize+1][n]={0};
    int count[aSize+1]={};//подсчет
    string output[n]={};
    for(int i=0;i<n;i++)
    {
        int dig=arr[i].size()-c;
        if(dig>-1)
        {
            k=0;
            while(arr[i][dig]!=alph[k])
                k++;
            ind[k][count[k]]=i;
            count[k]++;
        }else
        {
            ind[aSize][count[aSize]]=i;
            count[aSize]++;
        }
    }
    t=0;
    for(int i=0;i<count[aSize];i++)
    {
        output[t]=arr[ind[aSize][i]];
        t++;
    }
    for(int i=0;i<=aSize-1;i++)
    {
        for(int j=0;j<count[i];j++)
        {
            output[t]=arr[ind[i][j]];
            t++;
        }
    }

    for (int i=0;i<n;i++)
    {
       arr[i]=output[i];
    }
}
void RadixSort(string arr[],int n)
{
    int m=getMax(arr,n);
    for(int i=1;i<=m;i++)
    {
        CountSort(arr,n,i);
        cout<<"Sorting by "<<m-i<<" digit:"<<endl;
        for(int i=0;i<n;i++)
            cout<<arr[i]<<endl;
        cout<<endl;
    }

}
int main()
{
    int n;
    cin>>n;

    string *t=new string[n];
    for(int i=0;i<n;i++)
    {
        cin>>t[i];
    }
    RadixSort(t,n);

    return 0;
}
