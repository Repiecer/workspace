#include <iostream>
#include <list>

using namespace std;

int main(int argc, char const *argv[])
{
    list<list<int>> myList;
    myList.push_back({1, 2, 3, 4, 5});
    myList.push_back({6, 7, 8, 9, 10});
    myList.push_back({11, 12, 13, 14, 15});
    for (const auto& innerList : myList) {
        auto it = innerList.begin();
        advance(it, 2); // 移动到第三个元素
        cout << *it << endl;
        advance(it, 1);
        cout << *it << endl;
    }
    return 0;
}
