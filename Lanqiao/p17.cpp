#include <bits/stdc++.h>
using namespace std;

int b_x, b_y, h_x, h_y;
long long ans = 0;
vector<vector<int>> delta = {{2, 1}, {1, 2}, {-1, 2}, {-2, 1}, {1, -2}, {2, -1}, {-1, -2}, {-2, -1}};
vector<vector<bool>> horse;

bool isValid(int x, int y) {
    return x >= 0 && x <= b_x && y >= 0 && y <= b_y;
}

void dfs(int x, int y) {
    if (x > b_x || y > b_y) return;
    
    if (horse[x][y]) return;
    
    if (x == b_x && y == b_y) {
        ans++;
        return;
    }
    
    dfs(x + 1, y);
    dfs(x, y + 1);
}

int main() {
    cin >> b_x >> b_y >> h_x >> h_y;
    
    horse.resize(b_x + 1, vector<bool>(b_y + 1, false));
    horse[h_x][h_y] = true;
    
    for (int i = 0; i < delta.size(); i++) {
        int nx = h_x + delta[i][0];
        int ny = h_y + delta[i][1];
        if (isValid(nx, ny)) {
            horse[nx][ny] = true;
        }
    }
    
    dfs(0, 0);
    cout << ans << endl;
    return 0;
}