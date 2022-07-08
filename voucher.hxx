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

        voucher();

        ~voucher();

        std::string c_str();
        
        const int & voucher_number() const {return _voucher_number;} ;
        const std::string & timestamp() const {return _timestamp;} ;
        void timestamp(std::string value) { _timestamp = value;};
        const std::string & voucher_ref() const {return _voucher_ref;} ;
        void voucher_ref(std::string value) {_voucher_ref = value;};
        const float & voucher_amt() const { return  _voucher_amt; } ;
        void voucher_amt( float value) { _voucher_amt = value; };
        const int & voucher_type() const { return _voucher_type_id; } ;
        void voucher_type(int value) { _voucher_type_id = value;} ;
        const int & vendor_number() const { return _vendor_number; } ;
        void vendor_number(int value) { _vendor_number = value;};
        const int & payment_type() const { return _payment_type_id; } ;
        void payment_type(int value) { _payment_type_id = value; };
        const std::string payment_ref() const { return _payment_ref; } ;
        void payment_ref( std::string value) { _payment_ref = value;};
        const int payment_source() const { return _payment_source_id; } ;
        void payment_source( int value) {_payment_source_id = value;};
}; 
#endif