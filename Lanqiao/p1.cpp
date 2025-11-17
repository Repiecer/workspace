#include <iostream>
#include <vector>
#include <string>
#include <set>
#include <algorithm>
using namespace std;

using ll = long long;
using pll = pair<ll, ll>;

const ll base1 = 131;
const ll base2 = 13131;
const ll mod1 = 1e9 + 7;
const ll mod2 = 1e9 + 9;

int n;
vector<string> words;

// 检查是否存在长度为 len 的公共子串
bool check(int len) {
    if (len == 0) return true;
    
    // 从第一个单词中提取所有长度为 len 的子串的哈希值
    set<pll> common;
    string &s0 = words[0];
    int m = s0.length();
    
    ll h1 = 0, h2 = 0, p1 = 1, p2 = 1;
    for (int i = 0; i < len; i++) {
        h1 = (h1 * base1 + s0[i]) % mod1;
        h2 = (h2 * base2 + s0[i]) % mod2;
        if (i > 0) {
            p1 = (p1 * base1) % mod1;
            p2 = (p2 * base2) % mod2;
        }
    }
    common.insert({h1, h2});
    
    for (int i = len; i < m; i++) {
        h1 = ((h1 - s0[i - len] * p1 % mod1 + mod1) * base1 + s0[i]) % mod1;
        h2 = ((h2 - s0[i - len] * p2 % mod2 + mod2) * base2 + s0[i]) % mod2;
        common.insert({h1, h2});
    }
    
    // 检查其他单词
    for (int k = 1; k < n; k++) {
        set<pll> current;
        string &s = words[k];
        int L = s.length();
        
        ll h1 = 0, h2 = 0;
        for (int i = 0; i < len; i++) {
            h1 = (h1 * base1 + s[i]) % mod1;
            h2 = (h2 * base2 + s[i]) % mod2;
        }
        if (common.count({h1, h2})) {
            current.insert({h1, h2});
        }
        
        for (int i = len; i < L; i++) {
            h1 = ((h1 - s[i - len] * p1 % mod1 + mod1) * base1 + s[i]) % mod1;
            h2 = ((h2 - s[i - len] * p2 % mod2 + mod2) * base2 + s[i]) % mod2;
            if (common.count({h1, h2})) {
                current.insert({h1, h2});
            }
        }
        
        if (current.empty()) return false;
        common = move(current); // 更新公共集合为当前单词的匹配集合
    }
    
    return true;
}

int main() {
    cin >> n;
    words.resize(n);
    int min_len = 2005;
    for (int i = 0; i < n; i++) {
        cin >> words[i];
        if (words[i].length() < min_len) {
            min_len = words[i].length();
        }
    }
    
    int left = 0, right = min_len, ans = 0;
    while (left <= right) {
        int mid = (left + right) / 2;
        if (check(mid)) {
            ans = mid;
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    
    cout << ans << endl;
    
    return 0;
}