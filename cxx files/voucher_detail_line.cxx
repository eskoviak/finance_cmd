#include<map>
#include<string>

#include "voucher_detail.hxx"


voucher_detail_line::voucher_detail_line(std::string account_number,
                                         float amount,
                                         std::string dimension_1,
                                         std::string dimension_2,
                                         std::string memo)
{
    _account_number = account_number;
    _amount = amount;
    _dimension_1 = dimension_1;
    _dimension_2 = dimension_2;
    _memo = memo;

};

voucher_detail_line::~voucher_detail_line()
{};

std::string voucher_detail_line::c_str()
{
    return "(" 
        "account_number: " + _account_number +
        " amount: " + std::to_string(_amount) +
        " dim_1: " + _dimension_1 +
        " dim_2: " + _dimension_2 +
        " memo: " + _memo + ")";
};
