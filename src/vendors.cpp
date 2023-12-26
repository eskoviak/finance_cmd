#include "vendors.hpp"

Vendors::Vendors(){};
Vendors::Vendors(int vendor_number, std::string vendor_short_desc, std::string vendor_address) {
    vendor_number = vendor_number;
    vendor_short_desc = vendor_short_desc;
    vendor_address = vendor_address;
};

void Vendors::set_vendor_number(int vendor_number) {};
void Vendors::set_vendor_short_desc(std::string vendor_short_desc) {};
void Vendors::set_vendor_address(std::string vendor_address) {};

int Vendors::get_vendor_number() { return vendor_number; };
std::string Vendors::get_vendor_short_desc() { return vendor_short_desc; };
std::string Vendors::get_vendor_address() { return vendor_address; };

std::string Vendors::to_string() {
  return std::to_string(vendor_number) + " | " + 
        vendor_short_desc + " | " + vendor_address;
}