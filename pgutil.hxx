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
	/*std::string _pguri = "postgresql://postgres@localhost/finance";*/
	std::string _pguri = "postgresql://postgres:terces##@192.168.1.15/finance";
    public:
        pgutil();
        ~pgutil();
        const std::string & pguri() const {return _pguri;};
        lookup_map get_map(std::string, Lookup);
        voucher get_voucher(int);
        voucher_details get_voucher_details(int);
    
};

#endif
