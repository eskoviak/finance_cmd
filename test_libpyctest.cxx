#include<iostream>
#include "pyctest.hxx"

int main(int argc, char**argv){
    pyctest pyct = pyctest(100);
    std::cout << pyct.get_int();
    return 0;
};