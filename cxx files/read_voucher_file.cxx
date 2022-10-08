#include <iostream>
#include "csv.h"
#include "voucher.hxx"


int main (int argc, char**argv)
{
    std::string schema = "finance_tst";
    io::CSVReader<10> voucherc ("voucher.csv");
    voucherc.read_header(io::ignore_extra_column, "entered",
            "voucher_number",
            "voucher_date",
            "voucher_ref",
            "voucher_amt",
            "voucher_type_id",
            "vendor_number",
            "payment_type_id",
            "payment_ref",
            "payment_source_id");
    std::string voucher_date,voucher_ref,payment_ref;
    int entered,voucher_number,voucher_type_id,vendor_number,payment_type_id,payment_source_id;
    float voucher_amt;

    io::CSVReader<7> voucherd ("voucher_detail.csv");
    voucherd.read_header(io::ignore_extra_column,
        "entered",
        "id",
        "voucher_num",
        "account_number",
        "amount",
        "dimension_1",
        "dimension_2");
    int intered, id;
    float amount;
    std::string account_number, dimension_1, dimension_2;

    while(voucherc.read_row(entered,voucher_number,voucher_date,voucher_ref,voucher_amt,voucher_type_id,vendor_number,payment_type_id,payment_ref,payment_source_id))
    {
        
    }
}