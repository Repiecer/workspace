#include <bits/stdc++.h>
using namespace std;
double ans;
int n, i;
int main()
{
	cin >> n;
	for(i = 1; ans <= n;i++)
	{
        ans += 1.0 / i;
	}
	cout << i - 1;
	return 0;
}
