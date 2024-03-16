#include <iostream>
#include "vendors.hpp"

int main() {
    Vendors* v = new Vendors( 9999, "Generic Vendor", ";;;");
    std::cout << v->to_string() << std::endl;
    return 0;
}