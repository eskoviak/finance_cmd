#include <iostream>
#include "pyctest.hxx"
//#include "pgutil.hxx"

void test_empty(void)
{
    puts("Hello from C");
}

float test_add(float x, float y)
{
    return x+y;
}

void test_passing_array(int * data, int len)
{
    printf("Data as received from Python\n");
    for(int i = 0; i < len; ++i)
    {
        printf("%d ", data[i]);
    }
    puts("");
    for(int i = 0; i < len; ++i){
        data[i] = -i;
    }
}

/*
void get_vendors(char* buffer, int buf_size)
{
    strncpy(buffer, "{ \"vendors\" : [ { \"1000\" : \"don't remember\"}]", buf_size);
    //buffer = json.c_str();

}
*/