#include <bits/stdc++.h>

using namespace std;

int main(int argc, char const *argv[])
{
	int n;
	cin >> n;
	float a, b;
	a = 2;
	b = 1;
	float sum = a/b;
	for (int i = 0; i < n-1; ++i)
	{
		a, b = a+b, (-1)*a;
		cout << a/b << endl;
		sum+=a/b;
	}
	cout << sum;

	return 0;
}