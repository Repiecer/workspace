#include<bits/stdc++.h>
#include<vector>

using namespace std;

int main(){
	int a,b,c,d;
	cin >> a >> b >> c >> d;
	if(a==0){
		cout << d/b;
	}else if(b == 0){
		cout << c/a;
	}else cout << min(c/a, d/b);
	
	return 0;
}


