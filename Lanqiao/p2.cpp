#include <iostream>
#include <vector>
#include <string>
#include <list>

using namespace std;

int main(){
    int n;
    cin >> n;
    int a, b, c, d, position_x, position_y;
    list<list<int>> matrix;
    for (int i = 0; i < n; i++)
    {
        cin >> a >> b >> c >> d;
        matrix.push_front({a, b, c, d});
    }
    cin >> position_x >> position_y;
    int index = 0;
    for (const auto& innerList: matrix){
        auto it = innerList.begin();
        int x = innerList.front();
        
    }
    
    return 0;
}