#include <iostream>
#include <vector>
using namespace std;

vector<vector<int>> generateSpiralMatrix(int n) {
    vector<vector<int>> matrix(n, vector<int>(n, 0));
    
    // 定义四个方向：右、下、左、上
    int directions[4][2] = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}};
    int currentDirection = 0; // 从向右开始
    
    int num = 1;
    int row = 0, col = 0;
    
    while (num <= n * n) {
        matrix[row][col] = num++;
        
        // 计算下一个位置
        int nextRow = row + directions[currentDirection][0];
        int nextCol = col + directions[currentDirection][1];
        
        // 如果下一个位置超出边界或者已经被占据，则改变方向
        if (nextRow < 0 || nextRow >= n || nextCol < 0 || nextCol >= n || matrix[nextRow][nextCol] != 0) {
            currentDirection = (currentDirection + 1) % 4; // 转向：右下左上循环
            nextRow = row + directions[currentDirection][0];
            nextCol = col + directions[currentDirection][1];
        }
        
        row = nextRow;
        col = nextCol;
    }
    
    return matrix;
}

void printMatrix(const vector<vector<int>>& matrix) {
    for (const auto& row : matrix) {
        for (int num : row) {
            cout << num << " ";
        }
        cout << endl;
    }
}

int main() {
    int n;
    cin >> n;
    vector<vector<int>> spiralMatrix = generateSpiralMatrix(n);
    printMatrix(spiralMatrix);
    
    return 0;
}