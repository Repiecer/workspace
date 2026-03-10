#include <bit/stdc++.h>
typedef long long ll;
using namespace std;

int main(int argc, char const *argv[])
{
	int n;
	cin >> n;
	int arr[n];
	for (int i = 0; i < n; ++i)
	{
		cin >> arr[i];
	}
	int E[n+1];
	for(int i = 1; i<n+1; i++) E[i]=E[i-1]+arr[i-1];
	

	return 0;
}
