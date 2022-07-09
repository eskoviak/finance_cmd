#include <iostream>
#include "pyctest.hxx"

pyctest::pyctest(){
    _basic_string = "(1, 'one')";    
};

std::string pyctest::basic_string() { return _basic_string;};

extern "C" void pyctest::Print()
{
    std::cout << "Hello from inside the dylib" << std::endl;
}

