#include<bits/stdc++.h>
#include<vector>
#include<algorithm>

using namespace std;

int main(){
	int routine;
	cin >> routine;
	
	vector<int> input(routine);
	for(int i=0;i<=routine-1;i++){
		int temp;
		cin >> temp;
		input[i] = temp;
	};
	cout << *max_element(input.begin(), input.end());	
	return 0;
}


