#include <iostream>
#include <clocale>
using namespace std;
int main(){
system("chcp 65001");
setlocale(LC_ALL, "th_TH.UTF-8");
    int a = 123;
    int b = 654;
    string c = "สวัสดี";
    string d = "ชาวนา";
    double e = 1.23;
    double g = 4.56;
    string h = "ย";
    char i = 'l';
    bool t = true;
    bool f = false;
    cout << a + b << endl;
    if(a < b){
    cout << a << endl;
    } else {
    cout << b << endl;
    }
    cout << c + " " + d << endl;
    cout << e + g << endl;
    cout << h + i << endl;
    cout << t << " " << f << endl;
    for(int i=0;i<5;i++){
    cout << "Hello" << endl;
    }
    return 0;
}