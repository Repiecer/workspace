#include<bits/stdc++.h>

using namespace std;

int main(){
	int num;
	cin >> num;
	bool p = num%2==0;
	bool q = (num > 4) && (num <=12);
	cout << (p && q) << ' ' << (p||q) <<' '<< (p!=q) << ' ' << (!p && !q);
	return 0;
}

