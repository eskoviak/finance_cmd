#include<iostream>
#include "pyctest.hxx"

int main(int argc, char**argv){
    pyctest pyct = pyctest();
    std::cout << pyct.basic_string();
    return 0;
};