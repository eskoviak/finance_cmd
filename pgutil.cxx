#include "pgutil.hxx"
#include "voucher.hxx"
#include <pqxx/pqxx>

pgutil::pgutil()
{};

pgutil::~pgutil()
{};


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
    pqxx::connection c{pguri()};
    pqxx::work txn{c};
    pqxx::result r = txn.exec(stmt);

    for(auto row = r.begin(); row != r.end(); row++)
    {        
        map.insert(std::pair<int, std::string>(row[0].as<int>(),row[1].as<std::string>()));
    }
    
    return map;

};

voucher pgutil::get_voucher(int voucher_number)
{
    
    std::string stmt = 
        "SELECT voucher_date, voucher_ref, voucher_amt, voucher_type_id, vendor_number, "
        "  payment_type_id, payment_ref, payment_source_id "
        "FROM finance.voucher "
        "WHERE voucher_number = " + std::to_string(voucher_number) + ";";
    pqxx::connection c{pguri()};
    pqxx::work txn{c};
    pqxx::row row = txn.exec1(stmt);
    return voucher(voucher_number, row[0].as<std::string>(), row[1].as<std::string>(), row[2].as<float>(), row[3].as<int>(),
      row[4].as<int>(), row[5].as<int>(),row[6].as<std::string>(),row[7].as<int>());
};

voucher_details pgutil::get_voucher_details(int voucher_number){
    std::string stmt =
        "SELECT split_seq_number, account_number, amount, dimension_1, dimension_2, memo "
        "FROM finance.voucher_detail "
        "WHERE voucher_number = " + std::to_string(voucher_number) + ";";
    pqxx::connection c{pguri()};
    pqxx::work txn{c};
    pqxx::result r = txn.exec(stmt);
    voucher_details vd = voucher_details();
    for(auto const &row: r)
    {
        voucher_detail_line vdl = voucher_detail_line(row[1].as<std::string>(), row[2].as<float>(), 
            row[3].as<std::string>(),row[4].as<std::string>(),row[5].as<std::string>() );
        vd.add_line_item(row[0].as<int>(), vdl);
    }
    return vd;
};