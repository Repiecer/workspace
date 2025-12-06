#include <bits/stdc++.h>
#include <vector>

using namespace std;

int main(int argc, char const *argv[])
{
    int n;
    cin >> n;
    vector<vector<int>> dp(n, vector<int>(n, 0));
    while (true)
    {
        int x, y, val;
        cin >> x >> y >> val;
        if(x == 0 && y==0 && val==0){
            break;
        }else{
            dp[x-1][y-1] = val;
        }
    }
    for (int i = 1; i < n; i++)
    {
        dp[0][i]+=dp[0][i-1];
        dp[i][0]+=dp[i-1][0];
    }
    for (int i = 1; i < n; i++)
    {
        for (int j = 1; j < n; j++)
        {
            dp[i][j] = ((dp[i-1][j] > dp[i][j-1]) ? (dp[i-1][j]+dp[i][j]) : (dp[i][j-1]+dp[i][j]));
        }
        
    }
    cout << dp[n-1][n-1] << endl;
    
    
    
    return 0;
}



