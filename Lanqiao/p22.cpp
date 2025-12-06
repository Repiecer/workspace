#include <bits/stdc++.h>
#include <vector>

using namespace std;

int main(int argc, char const *argv[])
{
    int n, eco;
    vector<vector<int>> weights;
    cin >> n >> mon;
    for (int i = 0; i < n; i++)
    {
        int tem_sin, tem_even;
        cin >> tem_sin, tem_even;
        weights.push_back({tem_sin, tem_even});
    }
    vector<vector<int>> dp(n+1, vector<int>(eco+1, 0));
    
    return 0;
}


