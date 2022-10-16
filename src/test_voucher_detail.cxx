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

    voucher_details details;
    int seq_num;
    //voucher_detail_line line = voucher_detail_line("050101",34.29,"Health","","");
    seq_num = details.add_line_item(voucher_detail_line("050101",34.29,"Health","","item 1"));
    seq_num = details.add_line_item(voucher_detail_line("050101",29.34,"Grocery","","item 2"));
    //std::cout << seq_num << std::endl;
    //std::cout << line.c_str() << std::endl;
    std::cout << details.c_str() << std::endl;
    return 1;
};