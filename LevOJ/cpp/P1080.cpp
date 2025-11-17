#include<bits/stdc++.h>


using namespace std;

int main(){
    for(int i=100;i<=999;i++){
		int hundreds = i/100;
		int tens = (i/10)%10;
		int units = i%10;
		int sum = pow(hundreds,3)+pow(tens, 3)+pow(units, 3);
		if(sum==i){
			cout << i << endl;
			//TODO
		}
		//TODO
	}
    return 0;
}

