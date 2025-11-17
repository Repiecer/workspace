#include <iostream>
#include <vector>
#include <string>
#include <list>

using namespace std;

int main(){
    list<int> myList;
    myList.push_back(10);
    myList.push_back(20);
    myList.push_back(30);
    cout << myList.back();
    return 0;
}