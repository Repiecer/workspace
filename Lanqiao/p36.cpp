#include<bits/stdc++.h>

using namespace std;
int main(int argc, char const *argv[])
{
    double a, b, c;
    cin >>a>>b>>c;
    if ((a+b>c)&&(a+c>b)&&(b+c>a))
    {
        double p = (a+b+c)/2;
        double square = sqrt(p*(p-a)*(p-b)*(p-c));
        printf("%.2f", square);
    }else cout << "-1";

    return 0;
}
