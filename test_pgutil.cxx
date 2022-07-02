#include <iostream>
#include "pgutil.hxx"

int main(int argc, char**argv)
{
    std::string schema = "finance";
    for(int i = 0; i < argc; i++)
    {
        std::string arg = std::string(argv[i]);
        //std::cout << arg << std::endl;
        if(arg.compare("-d") == 0 | arg.compare("--debug") == 0) schema = "finance_tst";
    }
    //std::cout << "Using schema " << schema << std::endl;
    pgutil finance = pgutil();
    std::cout << "Next voucher_number for schema: " << schema << ": " << finance.get_next_voucher_number(schema) << std::endl;
};