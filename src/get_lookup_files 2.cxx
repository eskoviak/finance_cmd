#include <iostream>
#include <fstream>
#include <pqxx/pqxx>

int main(int, char *argv[])
{
  pqxx::connection c{"postgresql://postgres@localhost/finance"};
  pqxx::work txn{c};
 
  // we will reuse the pqxx::result and std::ofstream myfile for each go
  //
  // external_accounts
  // 
  pqxx::result r = txn.exec("select external_account_id,account_name "
    "from finance.external_accounts "
    "order by account_name;");


  std::ofstream myfile;
  myfile.open("external_accounts.txt", std::ios::out | std::ios::trunc);
  myfile << "external_acount_id,account_name" << std::endl;

  for (auto const &row: r)
  {
	myfile << row[0].c_str() << "," << row[1].c_str() << std::endl;
    
  }
  myfile.close();
  
  //
  // vendors
  //
  r = txn.exec("select vendor_number,vendor_short_desc "
    "from finance.vendors "
    "order by vendor_short_desc;");

  myfile.open("vendors.txt", std::ios::out | std::ios::trunc);
  myfile << "vendor_number,vendor_short_desc" << std::endl;
  for (auto const &row: r)
  {
    myfile << row[0].c_str() << "," << row[1].c_str() << std::endl;
  }
  myfile.close();

  //
  // payment_type
  //
  r = txn.exec("select payment_type_id, payment_type_text "
    "from finance.payment_type "
    "order by payment_type_id;");

  myfile.open("payment_type.txt", std::ios::out | std::ios::trunc);
  myfile << "payment_type_id,payment_type_text" << std::endl;
  for (auto const &row: r)
  {
    myfile << row[0].c_str() << "," << row[1].c_str() << std::endl;
  }
  myfile.close();

  //
  // voucher_type
  //
    r = txn.exec("select type_code, type_text "
    "from finance.voucher_type "
    "order by type_code;");

  myfile.open("voucher_type.txt", std::ios::out | std::ios::trunc);
  myfile << "type_code, type_text" << std::endl;
  for (auto const &row: r)
  {
    myfile << row[0].c_str() << "," << row[1].c_str() << std::endl;
  }
  myfile.close();

  txn.commit();
  return 0;
}
