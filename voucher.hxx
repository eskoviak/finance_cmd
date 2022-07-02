#ifndef VOUCHER_HXX
#define VOUCHER_HXX
#include<string>
#include "voucher_detail.hxx"

class voucher
{
    private:
        int _voucher_number;
        std::string _timestamp;  // This will be fudged
        std::string _voucher_ref;
        float _voucher_amt;
        int _voucher_type_id;
        int _vendor_number;
        int _payment_type_id;
        std::string _payment_ref;
        int _payment_source_id;
    
    public:
        voucher(
            int,
            std::string,
            std::string,
            float,
            int,
            int,
            int,
            std::string,
            int
        );
        ~voucher();
        std::string c_str();
        const int & voucher_number() const {return _voucher_number;} ;
};

struct entry {
    voucher header;
    voucher_details lines;
};
#endif