CPPFLAGS = -I/usr/local/opt/libpqxx/include -fPIC -Wall
#-I. -I/usr/local/include
CCLINUX = g++ -std=c++2a 
CC = clang++ -stdlib=libc++ -std=c++2a
LDFLAGS = -L/usr/local/opt/libpqxx/lib -L/usr/local/opt/libpq/lib -lpqxx -lpq
LDFLAGSLINUX = -lpqxx -lpq
OUTDIR = out/

get_lookup_files : get_lookup_files.cxx
	$(CCLINUX) $(CPPFLAGS) -o $@ $? $(LDFLAGS)

map : map.cxx
	$(CCLINUX) $(CPPFLAGS) -o $@ $? $(LDFLAGS)

voucher_details.o : voucher_details.cxx
	$(CCLINUX) $(CPPFLAGS) -c $? 

voucher_detail_line.o : voucher_detail_line.cxx
	$(CCLINUX) $(CPPFLAGS) -c $? 

voucher.o : voucher.cxx
	$(CCLINUX) $(CPPFLAGS) -c $?

pgutil.o : pgutil.cxx
	$(CCLINUX) $(CPPFLAGS) -c $?

#*.o : *.cxx
#	$(CCLINUX) $(CPPFLAGS) -c $? 

libvoucher.dylib : voucher_details.o voucher_detail_line.o voucher.o pgutil.o
	$(CC) $(CPPFLAGS) -v -dynamiclib $? -o $@  $(LDFLAGS)
	cp libvoucher.dylib /usr/local/lib

libvoucher.so : voucher.o voucher_detail_line.o voucher_details.o pgutil.o
	$(CCLINUX) $(CPPFLAGS) -shared $? -o $@ $(LDFLAGSLINUX)

libpyctest.dylib : cli_test/libpyctest.dylib/libpyctest_dylib.cpp
	$(CC) $(CPPFLAGS) -v -dynamiclib $? -o $@
	cp libpyctest.dylib /usr/local/lib

test_voucher_detail : test_voucher_detail.cxx
	$(CC) $(CPPFLAGS) -o $(OUTDIR)$@ $? $(LDFLAGS)

test_voucher : test_voucher.cxx
	$(CC) $(CPPFLAGS) -o $(OUTDIR)$@ $? $(LDFLAGS)

test_pgutil : test_pgutil.cxx
	$(CCLINUX) $(CPPFLAGS) -o $(OUTDIR)$@ $? $(LDFLAGS) -L. -lvoucher

test_libpyctest : test_libpyctest.cxx
	$(CC) $(CPPFLAGS) -o $(OUTDIR)$@ $? -L. -lpyctest

ilac_console : ilac_console.cxx
	$(CC) $(CPPFLAGS) -o $(OUTDIR)$@ $? $(LDFLAGS) -L. -lvoucher


