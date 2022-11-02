#include <iostream>
#include <iomanip>
#include <cstdio>
#include "ilac.hxx"

int main(int argc, char **argv)
{
    char ch;
    std::string voucher_number;
    int line_size = 80;
    char line[line_size];
    std::string sval;
    float fval;
    int ival;
    bool quit = false;
    console c = console();
    voucher v = voucher();
    while (!quit)
    {
        std::cout << "\n\n\n\n\n\n\n\n\n";
        std::cout << "ILAC CLI\n========\n(p)rint voucher\n(e)nter voucher\n\n(q)uit\n\nEnter Choice >";
        std::cin >> ch;
        switch (ch)
        {
            case 'p':
            case 'P':
                std::cout << "Enter voucher number: ";
                std::cin >> voucher_number;
                c.display_voucher(std::stoi(voucher_number));
                std::cout << "Enter to continue... ";
                std::cin >> ch;
                continue;
            case 'e':
                std::cout << "Enter the transaction date and time: ";
                //std::cin.getline(line, line_size);
                std::getline( std::cin, sval);
                v.timestamp(sval);
                //std::cout << "Enter the transaction reference: ";
                //std::cin.getline(line, line_size);
                //v.voucher_ref(std::string(line));
                std::cout << v.c_str();
                std::cout << "Enter to continue... ";
                std::cin >> ch;
                continue;
            case 'q':
            case 'Q':
                quit = true;
                continue;
        }
    }

    return 0;
}

void console::display_voucher(int voucher_number)
{
    pgutil finance = pgutil();
    voucher v = finance.get_voucher(voucher_number);
    voucher_details vd = finance.get_voucher_details(voucher_number);

    std::cout.setf(std::ios::fixed, std::ios::floatfield);
    std::cout.precision(2);

    std::cout << std::setfill('=') << std::setw(50) << '=' << std::endl;
    std::cout << "#              Date\n";
    std::cout << std::setfill(' ') << std::setw(5) << std::to_string(voucher_number) << pad10 << v.timestamp() + "\n\n";
    std::cout << "Voucher Reference\n";
    std::cout << v.voucher_ref() << std::endl
              << std::endl;
    std::cout << "Amt                 Type          Vendor\n";
    std::cout << std::setw(10) << v.voucher_amt() << pad10 << std::setw(4);
    std::cout << std::to_string(v.voucher_type()) << pad10 << std::setw(6);
    std::cout << std::to_string(v.vendor_number()) << std::endl
              << std::endl;
    std::cout << "Pmt Type          Pmt Src\n";
    std::cout << std::setw(8) << std::to_string(v.payment_type()) << pad10 << std::to_string(v.payment_source()) << std::endl
              << std::endl;
    std::cout << "Payment Reference\n";
    std::cout << v.payment_ref() << std::endl
              << std::endl;
    std::cout << "--------- DETAIL ----------\n\n";
    for (auto const &item : vd.voucher_line())
    {
        std::cout << std::setw(5) << item.first << pad5 << std::setw(10) << std::left << "Account" << pad5 << std::setw(10) << std::left << "Ammount" << std::endl;
        std::cout << pad10 << std::setw(10) << item.second.account_number() << pad5 << item.second.amount() << std::endl;
        std::cout << pad10 << std::setw(20) << std::left << "Dimension 1" << pad10 << std::left << "Dimension 2" << std::endl;
        std::cout << pad10 << std::setw(20) << item.second.dim_1() << pad10 << item.second.dim_2() << std::endl;
        std::cout << pad10 << "Memo\n";
        std::cout << pad10 << item.second.memo() << std::endl;
    }
    std::cout << std::setfill('=') << std::setw(50) << '=' << std::endl;
}
