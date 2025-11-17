#include<bits/stdc++.h>
#include<vector>

using namespace std;
int main(){
	
	int routine;
	cin >> routine;
	vector<int> results(routine);
	for(int i=0;i<=routine;i++){
		int num;
		cin >> num;
		int sum = 0;
		for(int j=0;j<=num;j++){
			int temp;
			cin >> temp;
			sum += temp;
			
		}
		results.push_back(sum);
		
	}
	for(int i=0;i<=routine;i++){
		cout << results[i];
		
	}
	
	return 0;
}

