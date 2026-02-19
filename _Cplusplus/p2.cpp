#include <bits/stdc++.h>
 using namespace std;

int main(int argc, char const *argv[])
{
	int arr[5];
	for (int i = 0; i < 5; ++i)
	{
		cin >> arr[i];
	}
	int sum = 0;
	for (int i = 0; i < 5; ++i)
	{
		sum+=arr[i];
	}
	cout << sum << endl;
	return 0;
}
