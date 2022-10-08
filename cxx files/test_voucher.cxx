#include<iostream>
#include "voucher.hxx"
#include "voucher_detail.hxx"

int main(int argc, char**argv)
{
    std::string schema = "finance";
    for(int i = 0; i < argc; i++)
    {
        std::string arg = std::string(argv[i]);
        //std::cout << arg << std::endl;
        if(arg.compare("-d") == 0 | arg.compare("--debug") == 0) schema = "finance_tst";
    }
    std::cout << "Using schema " << schema << std::endl;

    voucher receipt = voucher(1, "06/25/22 18:00 CDT","",100,1,1,1,"yup",2);
    std::cout << receipt.c_str() << std::endl;

}