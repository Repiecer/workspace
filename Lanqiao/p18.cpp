#include <bits/stdc++.h>
using namespace std;

int main() {
    int b_x, b_y, h_x, h_y;
    cin >> b_x >> b_y >> h_x >> h_y;
    
    vector<vector<long long>> dp(b_x + 1, vector<long long>(b_y + 1, 0));
    
    vector<vector<int>> horse_delta = {
        {2, 1}, {1, 2}, {-1, 2}, {-2, 1}, 
        {1, -2}, {2, -1}, {-1, -2}, {-2, -1}
    };
    
    vector<vector<bool>> blocked(b_x + 1, vector<bool>(b_y + 1, false));
    
    if (h_x <= b_x && h_y <= b_y) {
        blocked[h_x][h_y] = true;
    }
    
    for (auto d : horse_delta) {
        int nx = h_x + d[0];
        int ny = h_y + d[1];
        if (nx >= 0 && nx <= b_x && ny >= 0 && ny <= b_y) {
            blocked[nx][ny] = true;
        }
    }
    
    if (!blocked[0][0]) {
        dp[0][0] = 1;
    }
    
    for (int i = 0; i <= b_x; i++) {
        for (int j = 0; j <= b_y; j++) {
            if (blocked[i][j]) continue;
            
            if (i > 0 && !blocked[i-1][j]) {
                dp[i][j] += dp[i-1][j];
            }
            
            if (j > 0 && !blocked[i][j-1]) {
                dp[i][j] += dp[i][j-1];
            }
        }
    }
    
    cout << dp[b_x][b_y] << endl;
    return 0;
}