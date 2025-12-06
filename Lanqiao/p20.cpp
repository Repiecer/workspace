#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<vector<int>> grid(n+1, vector<int>(n+1, 0));
    
    while (true) {
        int x, y, val;
        cin >> x >> y >> val;
        if (x == 0 && y == 0 && val == 0) break;
        grid[x][y] = val;
    }
    
    vector<vector<vector<vector<int>>>> dp(n+1, 
        vector<vector<vector<int>>>(n+1,
            vector<vector<int>>(n+1,
                vector<int>(n+1, 0))));
    
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            for (int k = 1; k <= n; k++) {
                for (int l = 1; l <= n; l++) {
                    int best = max({
                        dp[i-1][j][k-1][l],
                        dp[i-1][j][k][l-1],
                        dp[i][j-1][k-1][l],
                        dp[i][j-1][k][l-1]
                    });
                    
                    if (i == k && j == l) {
                        dp[i][j][k][l] = best + grid[i][j];
                    } else {
                        dp[i][j][k][l] = best + grid[i][j] + grid[k][l];
                    }
                }
            }
        }
    }
    
    cout << dp[n][n][n][n] << endl;
    return 0;
}