#include<string>
#include "voucher.hxx"

voucher::voucher(
        int voucher_number,
        std::string voucher_date,
        std::string voucher_ref,
        float voucher_amt,
        int voucher_type_id,
        int vendor_number,
        int payment_type_id,
        std::string payment_ref,
        int payment_source_id
)
{
    _voucher_number = voucher_number;
    _timestamp = voucher_date;
    _voucher_ref = voucher_ref;
    _voucher_amt = voucher_amt;
    _voucher_type_id = voucher_type_id;
    _vendor_number = vendor_number;
    _payment_type_id = payment_type_id;
    _payment_ref = payment_ref;
    _payment_source_id = payment_source_id;
};

voucher::voucher() {};

voucher::~voucher()
{};

std::string voucher::c_str()
{
    return "Voucher (" 
        " voucher_number: " + std::to_string(_voucher_number) +
        " timestamp: " + _timestamp +
        " voucher_ref: " + _voucher_ref +
        " voucher_amt: " + std::to_string(_voucher_amt) +
        " voucher_type_id: " + std::to_string(_voucher_type_id) +
        " vendor_number: " + std::to_string(_vendor_number) +
        " payment_type_id: " + std::to_string(_payment_type_id) +
        " payment_ref: " + _payment_ref +
        " payment_source_id: " + std::to_string(_payment_source_id) + ")";

};
