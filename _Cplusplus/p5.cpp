#include <bits/stdc++.h>
using namespace std;
const int MAXN = 100005;
int bit[MAXN * 2];
int n, m;

void update(int idx, int delta) {
    while (idx <= n + 1) {
        bit[idx] += delta;
        idx += idx & -idx;
    }
}

int query(int idx) {
    int sum = 0;
    while (idx > 0) {
        sum += bit[idx];
        idx -= idx & -idx;
    }
    return sum;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n >> m;
    while (m--) {
        int t;
        cin >> t;

        if (t == 1) {
            // 区间反转操作
            int L, R;
            cin >> L >> R;

            update(L, 1);
            update(R + 1, -1);
        }
        else {
            int i;
            cin >> i;
            int times = query(i);
            cout << (times & 1) << '\n';
        }
    }
    return 0;
}
