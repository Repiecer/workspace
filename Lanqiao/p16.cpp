#include <iostream>
using namespace std;

int main() {
    int N;
    cin >> N;
    
    int a[105];
    int sum = 0;
    for (int i = 0; i < N; i++) {
        cin >> a[i];
        sum += a[i];
    }
    
    int avg = sum / N;
    int moves = 0;
    
    for (int i = 0; i < N - 1; i++) {
        if (a[i] != avg) {
            int diff = a[i] - avg;
            a[i + 1] += diff;
            moves++;
        }
    }
    
    cout << moves << endl;
    
    return 0;
}