#ifndef VOUCHER_DETAIL_HXX
#define VOUCHER_DETAIL_HXX
#include <string>
#include <map>

class voucher_detail_line
{
    private:
        std::string _account_number;
        float _amount;
        std::string _dimension_1;
        std::string _dimension_2;
        std::string _memo;
    public:
        voucher_detail_line(std::string, float, std::string, std::string, std::string);
        ~voucher_detail_line();
        std::string c_str();
};

class voucher_details
{
    private:
        std::map<int, voucher_detail_line> _voucher_line;
        int _seq_num;

    public:
        voucher_details();
        int add_line_item(voucher_detail_line);
        ~voucher_details();
        std::string c_str();
        //int begin();
        //int end();

};

#endif
