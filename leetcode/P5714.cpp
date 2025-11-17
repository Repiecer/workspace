#include<bits/stdc++.h>


using namespace std;

int main(){
	float weight;
	
	float heigth;
	cin >> weight >> heigth;
	float bmi = weight/(heigth*heigth);
	if(bmi<18.5){
		cout << "Underweight";
	}else if(bmi >=18.5 && bmi <24){
		cout << "Normal";
		//TODO
	}else{
		cout << bmi << endl;
		cout << "Overweight";
	}
	return 0;
}

