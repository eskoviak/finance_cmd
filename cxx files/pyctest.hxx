#pragma once

#ifdef __cplusplus
extern "C" {
#endif

struct vendor {
    int vendor_number;
    char* vendor_short_desc;
};

void test_empty(void);
float test_add(float x, float y);
void test_passing_array(int* data, int len);
void get_vendors(char * buffer, int buf_size);
struct vendor get_vendor(int vendor_number);

#ifdef __cplusplus
}
#endif