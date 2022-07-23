import sys, platform, ctypes, ctypes.util

if platform.system() == "Windows":
        pass
else:
    path_libc = ctypes.util.find_library('c')
    path_libpyctest = ctypes.util.find_library('pyctest')
    path_libvoucher = ctypes.util.find_library('voucher')

try:
    libc = ctypes.CDLL(path_libc)
    libpyctest = ctypes.CDLL(path_libpyctest)
    libvoucher = ctypes.CDLL(path_libvoucher)
except OSError:
    print(f"Unable to load the system C lib")

print(f"Successfully loaded the sytem C lib from {path_libc}")
print(f"Successfully loaded the local libpyctest lib from {path_libpyctest}")
print(f"Successfully loaded the local libvoucher lib from {path_libvoucher}")

libc.puts(b"Hello from Python to C")

# Make the functions name visible at the modeule level; add typing
test_empty = libpyctest.test_empty

test_add = libpyctest.test_add
test_add.argtypes = [ctypes.c_float, ctypes.c_float]
test_add.restype = ctypes.c_float

test_passing_array = libpyctest.test_passing_array
test_passing_array.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
test_passing_array.restype = None

get_vendors = libvoucher.get_vendors_dict
get_vendors.argtypes = None
get_vendors.restype = ctypes.c_char_p

