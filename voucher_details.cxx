#include<iostream>

#include "voucher_detail.hxx"

voucher_details::voucher_details()
{
    _voucher_line = std::map<int, voucher_detail_line>();
    _seq_num = 1;
};

int voucher_details::add_line_item(voucher_detail_line item)
{
    _voucher_line.insert(std::pair<int, voucher_detail_line>(_seq_num, item));
    return _seq_num++;
};

void voucher_details::add_line_item(int split_seq_num, voucher_detail_line item)
{
    _voucher_line.insert(std::pair<int, voucher_detail_line>(split_seq_num, item));
};

voucher_details::~voucher_details()
{};

std::string voucher_details::c_str()
{
    std::string rval = "voucher_details: (";
    for(std::map<int, voucher_detail_line>::iterator it=_voucher_line.begin(); it!=_voucher_line.end(); ++it)
    {
        rval.append("split: " + std::to_string(it->first)+ "," + it->second.c_str() + "\n");
    };
    return rval + ")";
};
