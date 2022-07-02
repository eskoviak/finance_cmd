#include "pgutil.hxx"
#include <pqxx/pqxx>


pgutil::pgutil()
{};

pgutil::~pgutil()
{};

int pgutil::get_next_voucher_number(std::string schema)
{
    int next = 0;
    pqxx::connection c{_pguri};
    pqxx::work txn{c};
    auto const r = txn.exec("select max(voucher_number) "
        "from " + schema + ".voucher;");

    txn.commit();

    return r[0][0].as<int>() +1;
    
};

int pgutil::insert_voucher_with_id(std::string schema, entry item)
{
    pqxx::connection c{_pguri};
    pqxx::work txc{c};
    std::string stmt = "INSERT INTO " + schema + ".voucher "
        "(voucher_number, voucher_date, voucher_ref, voucher_amt, voucher_type_id, vendor_number, "
        "paymenbt_type_id, payment_ref, payment_source_id) "
        "VALUES ( " +
        std::to_string(item.header.voucher_number()) + "," +

        ")";


    return 0;
};