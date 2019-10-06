#include <vector>
#include <iostream>
#include <cmath>
using namespace std;

void QuickSort(int a[], int l, int r, int n){
if (l + 1 >= r) return;
int pivot = (r - 1 + l) / 2;
int i, tmp, mid;
int mas[n] ={};
tmp = l;
cout<<endl;
cout<<endl;
cout<<"Pivot index: " << pivot << " , pivot element: " << a[pivot] << endl;
i=l;
while(i<r)
{
   if (a[i] <= a[pivot] && i != pivot)
{
mas[tmp] = a[i];
tmp++;
}
i++;
}
mas[tmp] = a[pivot];
mid = tmp;
tmp++;
i=l;
while(i<r)
{
    if (a[i] > a[pivot] && i != pivot)
{
mas[tmp] = a[i];
tmp++;
}
i++;
}
for (i = l; i < r; i++)
{
    a[i] = mas[i];
}
cout << "Array after partition: ";
for (i = 0; i < n; i++)
{
    cout << a[i] << " ";
}

QuickSort(a, l, mid, n);
QuickSort(a, mid + 1, r, n);
}

int main()
{
int n;
cin>>n;
int *arr=new int[n];
for (int i = 0; i < n; i++)
{
    cin >> arr[i];
}
cout << "Initial array:" << endl;
for (int i = 0; i < n; i++)
{
    cout << arr[i] << " ";
}
QuickSort(arr, 0, n, n);
return 0;
}
