import encodings
import libtest
import ctypes
import json

print(f"Testing the library")
print(f"Test 1:  test_empty")
libtest.test_empty()

print(f"Test 2: test_add")
print(f"{libtest.test_add(3.14, 2.14)}")

print(f"Test 3: test_passing_array")
numel = 25
data = (ctypes.c_int * numel)(*[x for x in range(numel)])

libtest.test_passing_array(data, numel)

print(f"After the call...")
for index in range(numel):
    print(data[index], end = " ")
print("")

print(f"Test 4:  get_vendors")

print(f"Before the call\n====\n")
#str = libtest.get_vendors().decode(encoding='utf8').replace('\"','"')
#print(json.dumps(str, sort_keys=True, indent=4))
#vendors = (json.loads(libtest.get_vendors().decode(encoding='utf8')))['vendors']
#for vendor in vendors:
print(libtest.get_vendors())
print(f"After the call:\n====\n")