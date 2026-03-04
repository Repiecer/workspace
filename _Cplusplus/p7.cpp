#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
typedef long long ll;

int main() {
    ll H, N;
    cin >> H >> N;
    vector<ll> P(N);
    for (int i = 0; i < N; ++i) cin >> P[i];

    // 第0天模拟
    vector<ll> pref(N + 1, 0), c(N + 1, 0);
    for (int i = 0; i < N; ++i) {
        pref[i + 1] = pref[i] + P[i];
        c[i + 1] = max(0LL, c[i] + P[i]);
        if (c[i + 1] >= H) {
            cout << "0 " << i << endl;
            return 0;
        }
    }

    ll C = c[N];               // 第0天结束高度
    ll S = pref[N];            // 一个周期的净增长

    if (S <= 0) {
        // 净增长非正，只需检查第1天
        ll cur = C;
        for (int i = 0; i < N; ++i) {
            cur = max(0LL, cur + P[i]);
            if (cur >= H) {
                cout << "1 " << i << endl;
                return 0;
            }
        }
        cout << "-1 -1" << endl;
        return 0;
    }

    // S > 0，对每个阶段计算需要的最小天数
    ll best_day = 1e18, best_stage = -1;
    for (int j = 0; j < N; ++j) {
        if (c[j + 1] >= H) continue;   // 第0天应已处理，这里不会发生
        ll need = H - pref[j + 1];      // 需要的起始高度
        ll d;
        if (need <= C) {
            d = 1;
        } else {
            d = 1 + (need - C + S - 1) / S;
        }
        if (d < best_day || (d == best_day && j < best_stage)) {
            best_day = d;
            best_stage = j;
        }
    }

    cout << best_day << " " << best_stage << endl;
    return 0;
}