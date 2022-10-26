#ifndef PGUTIL_HXX
#define PGUTIL_HXX
#include <pqxx/pqxx>
#include <string>
#include "voucher.hxx"
#include "voucher_detail.hxx"

typedef std::map<int, std::string> lookup_map;
enum Lookup { vendors, payment_sources, voucher_types, payment_types };
class pgutil
{
    private:
    std::string _pguri = "postgresql://postgres:terces##@localhost:5432/finance";
    //std::string _pguri = "postgresql://edmundlskoviak@localhost/finance";

    
    public:
        pgutil();
        ~pgutil();
        const std::string & pguri() const {return _pguri;};
        lookup_map get_map(std::string, Lookup);
        voucher get_voucher(int);
        voucher_details get_voucher_details(int);

};

//extern "C" char * get_vendors_dict(void);
extern "C" const char* get_vendors_dict();

#endif
