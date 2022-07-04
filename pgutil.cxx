#include "pgutil.hxx"
#include <pqxx/pqxx>


pgutil::pgutil()
{};

pgutil::~pgutil()
{};

int pgutil::get_next_voucher_number(std::string schema)
{
    int next = 0;
    pqxx::connection c{pgutil::pguri()};
    pqxx::work txn{c};
    auto const r = txn.exec("select max(voucher_number) "
        "from " + schema + ".voucher;");

    txn.commit();

    return r[0][0].as<int>() +1;
    
};

int pgutil::insert_voucher_with_id(std::string schema, entry item)
{
    pqxx::connection c{pgutil::pguri()};
    pqxx::work txc{c};
    std::string stmt = "INSERT INTO " + schema + ".voucher "
        "(voucher_number, voucher_date, voucher_ref, voucher_amt, voucher_type_id, vendor_number, "
        "paymenbt_type_id, payment_ref, payment_source_id) "
        "VALUES ( " +
        std::to_string(item.header.voucher_number()) + "," +

        ")";


    return 0;
};

lookup_map pgutil::get_map(std::string schema, Lookup lookup_type)
{
    lookup_map map;
    std::string stmt;
    switch (lookup_type)
    {
    case vendors:
        stmt = "SELECT vendor_number, vendor_short_desc "
          "FROM " + schema + ".vendors "
          "ORDER BY vendor_short_desc;";
        break;
    case payment_sources:
        stmt = "SELECT external_account_id, account_name " 
          "FROM " + schema + ".external_accounts " 
          "WHERE external_account_id IN (15957,19998, 26624, 22301, 22008, 25957, 16195, 25598, 13031, 11416)"
          "ORDER BY account_name;";
        break;
    case payment_types:
        stmt = "SELECT payment_type_id, payment_type_text "
          "FROM " + schema + ".payment_type "
          "ORDER BY payment_type_id;";
        break;
    case voucher_types:
        stmt = "SELECT type_code, type_text "
          "FROM " + schema + ".voucher_type "
          "ORDER BY type_code;";
        break;
    default:

        break;
    }
    pqxx::connection c{"postgresql://postgres@localhost/finance"};
    pqxx::work txn{c};
    pqxx::result r = txn.exec(stmt);

    for(auto const &row:r)
    {
        map.insert(std::pair<int, std::string>(row[0].as<int>(), row[1].as<std::string>()));
    }
    return map;

}

