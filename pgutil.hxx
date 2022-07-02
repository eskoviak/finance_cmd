#ifndef PGUTIL_HXX
#define PGUTIL_HXX
#include <pqxx/pqxx>
#include <string>
#include "voucher.hxx"

class pgutil
{
    private:
        std::string _pguri = "postgresql://postgres@localhost/finance";
    public:
        pgutil();
        ~pgutil();
        int get_next_voucher_number(std::string schema);
        int insert_voucher_with_id(std::string schema, entry);

};

#endif