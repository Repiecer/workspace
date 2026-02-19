#include <bits/stdc++.h>
using namespace std;

int main(int argc, char const *argv[])
{

	int n, k;
	cin >> n >> k;
	int arr[n];
	int srr[n];
	for (int i = 0; i < n; ++i)
	{
		cin >> arr[i];
	}
	if (k==1)
	{
		cout << ((1+n)*n)/2 << endl;
	}
	srr[0] = arr[0];
	for (int i = 1; i < n; ++i)
	{
		srr[i] = srr[i-1]+arr[i];
	}
	int ans=0;
	for (int i = 0; i < n; ++i)
	{
		for (int j = i; j < n; ++j)
		{
			if (i==0)
			{
				if (srr[j]%k==0)
				{
					ans++;
				}
			}else{
				if ((srr[j]-srr[i-1])%k==0)
				{
					ans++;
				}
			}

		}
	}
	cout << ans << endl;
	return 0;
}