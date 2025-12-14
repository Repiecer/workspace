#include <bits/stdc++.h>
using namespace std;

#define FASTIO ios_base::sync_with_stdio(false); cin.tie(NULL); cout.tie(NULL);
typedef long long ll;

const int N = 2e5 + 10;

void solve() {
    int n, m;
    cin >> n >> m;
    vector<int> a(n + 1);
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
    }
    vector<int> d(n + 1, 0);
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        d[u]++;
        d[v]++;
    }
    int mx = 0;
    vector<int> res;
    for (int i = 1; i <= n; i++) {
        if (d[i] != 1) {
            mx = max(mx, a[i]);
        } else {
            res.push_back(a[i]);
        }
    }
    sort(res.begin(), res.end(), greater<int>());
    if (res.size() >= 2) {
        mx = max(mx, res[1]);
    }
    cout << mx << "\n";
}

int main() {
    FASTIO
    int t = 1;

    while (t--) {
        solve();
    }
    return 0;
}