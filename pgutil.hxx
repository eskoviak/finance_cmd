#ifndef PGUTIL_HXX
#define PGUTIL_HXX
#include <pqxx/pqxx>
#include <string>
#include "voucher.hxx"

typedef std::map<int, std::string> lookup_map;
enum Lookup { vendors, payment_sources, voucher_types, payment_types };
class pgutil
{
    private:
        std::string _pguri = "postgresql://postgres@localhost/finance";
    public:
        pgutil();
        ~pgutil();
        int get_next_voucher_number(std::string schema);
        int insert_voucher_with_id(std::string schema, entry);
        const std::string & pguri() const {return _pguri;};
        lookup_map get_map(std::string, Lookup);
        //std::map<int, std::string> get_payment_type_map(std::string);
        //std::map<int, std::string> get_payment_source_map(std::string);
        //std::map<int, std::string> get_voucher_type_map(std::string);    

    
        
        // needs work
        //pqxx::work get_txn() { 
        //    pqxx::connection c {_pguri};
        //    return pqxx::work{c};
        //}; 

};

#endif