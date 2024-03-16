// -*- lsst-c++ -

/*
 * vendors.hpp -- header file for vendors clss
 * 
 * Part of {{ }}
 * Contains definintions and methods 
 *
 */

#ifndef VENDORS
#define VENDORS

#include <string>

/*
 * Wraps the vendors table
*/
class Vendors {
    private:
        int vendor_number;
        std::string vendor_short_desc;
        std::string vendor_address;

    public:
        // default constructor
        Vendors();

        // named constructor
        Vendors( int,std::string, std::string);

        // getters and setters
        void set_vendor_number(int);
        void set_vendor_short_desc(std::string);
        void set_vendor_address(std::string); 

        int get_vendor_number();
        std::string get_vendor_short_desc();
        std::string get_vendor_address();

        // helpers
        std::string to_string();
};

#endif