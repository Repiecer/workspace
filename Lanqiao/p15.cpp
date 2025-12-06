#include <iostream>
#include <algorithm>
using namespace std;

int main() {
    int L, N;
    cin >> L >> N;
    
    if (N == 0) {
        cout << "0 0" << endl;
        return 0;
    }
    
    int min_time = 0, max_time = 0;
    for (int i = 0; i < N; i++) {
        int x;
        cin >> x;
        int mint = min(x, L + 1 - x);
        int maxt = max(x, L + 1 - x);
        min_time = max(min_time, mint);
        max_time = max(max_time, maxt);
    }
    
    cout << min_time << " " << max_time << endl;
    
    return 0;
}