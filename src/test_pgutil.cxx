#include <iostream>
#include <exception>
#include "pgutil.hxx"

class assertion_exception : public std::exception
{
    virtual const char* what() const throw()
    {
        return "Assertion Failure";
    };
} assertfail;

int main(int argc, char**argv)
{
    // Housekeeping
    std::string msg;
    auto print_header = [&msg]() { std::cout << msg << std::endl;};
    auto print_fail = [&msg]() { std::cout << "Test Fail: " + msg << std::endl;};
    auto print_pass = []() { std::cout << "Test Passed!" << std::endl;};

    // Test Setup
    std::string schema = "finance";
    for(int i = 0; i < argc; i++)
    {
        std::string arg = std::string(argv[i]);
        //std::cout << arg << std::endl;
        if(arg.compare("-d") == 0 | arg.compare("--debug") == 0) schema = "finance_tst";
    }
    pgutil finance = pgutil();

    try
    {   
 
        msg = "Test 0:  Print pguri for " + schema;
        print_header();
        std::cout << finance.pguri() << std::endl;
 
        msg = "Test 1:  Get vendors map for schema " + schema;
        print_header();
        lookup_map vendors = finance.get_map(schema, Lookup::vendors);
        if(vendors.empty()){
            msg = "vendor map is empty";
            print_fail();
            throw assertfail;
        } else if (vendors[1000] != "Fresh Thyme AV") {
            msg = "vendor[1000] NOT EQUAL \"Fresh Thyme AV\"";
            print_fail();
            throw assertfail;
        } else {
            print_pass();
        }

        msg = "Test 2: Get payment_source map for schema " + schema;
        print_header();
        lookup_map payment_sources = finance.get_map(schema, Lookup::payment_sources);
        if(payment_sources.empty()){
            msg = "Map is empty";
            print_fail();
            throw assertfail;
        } else if (payment_sources[22008] != "Amex Card") {
            msg = "payment_sources[22008] NOT EQUAL \"Amex Card\"";
            print_fail();
            throw assertfail;
        } else {
            print_pass();
        }

        msg = "Test 3:  Get voucher_type map for schema " + schema;
        print_header();
        lookup_map voucher_types = finance.get_map(schema, Lookup::voucher_types);
        if(voucher_types.empty())
        {
            msg = "Map is empty";
            print_fail();
            throw assertfail;    
        }
        else if (voucher_types[1].compare("Electronic receipt") != 0)
        {
            msg = "voucher_types[1] NOT EQUAL \"Electronic receipt\"";
            print_fail();
            throw assertfail;
        }
        else
        {
            print_pass();
        }

        msg = "Test 4:  Get payment_type map for schema " + schema;
        print_header();
        lookup_map payment_types = finance.get_map(schema, Lookup::payment_types);
        if(payment_types.empty())
        {
            msg = "Map is empty";
            print_fail();
            throw assertfail;
        }
        else if (payment_types[10].compare("Debit Card") != 0)
        {
            msg = "payment_types[10] NOT EQUAL \"Debit Card\"";
            print_fail();
            throw assertfail;
        }
        else
        {
            print_pass();
        }
        
        msg = "Test 5: Get voucher from database ";
        print_header();
        voucher v = finance.get_voucher(1002);
        std::cout << v.c_str() << std::endl;
        print_pass();

        msg = "Test 6:  Get voucher_detail from database ";
        print_header();
        voucher_details vd = finance.get_voucher_details(1002);
        std::cout << vd.c_str() << std::endl;
        print_pass();

        msg = "Test 7:  get_vendors_dict without search phrase";
        print_header();
        std::cout << get_vendors_dict() << std::endl;
        print_pass();

    }
    catch (std::exception& e)
    {
        std::cout << e.what() << std::endl;
    };

}; 

