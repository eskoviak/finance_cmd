#include <string>

class pyctest
{
    private:
        std::string _basic_string;
    int _my_int;
    public:
        pyctest();
        std::string basic_string();
        void Print();
        const int get_int();
};
