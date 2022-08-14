#pragma once

#ifdef __cplusplus
extern "C" {
#endif

void test_empty(void);
float test_add(float x, float y);
void test_passing_array(int* data, int len);
void get_vendors(char * buffer, int buf_size);

#ifdef __cplusplus
}
#endif