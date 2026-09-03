#include <cmath>
#include <iomanip>
#include <ios>
#include <iostream>
#include <iterator>
#include <ostream>
#include <stack>
#include <string>

using namespace std;

bool cal_classify(string subj){
    stack<char> syms;
    for (char sym : subj) {
        if (sym == '(') {
            syms.push(sym);
        }else {
            if (syms.empty()) {
                return false;
            }else {
                syms.pop();
            }
        }
    }
    return syms.empty();
}

int main(){
    bool ans = cal_classify("()((())))");
    cout <<boolalpha<< ans <<endl;

    return 0;
}
