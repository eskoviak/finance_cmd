CPPFLAGS = -I/usr/local/opt/libpqxx/include 
#-I. -I/usr/local/include
#CC = g++ -std=c++2a
CC = clang++ -stdlib=libc++ -std=c++2a
LDFLAGS = -L/usr/local/opt/libpqxx/lib -L/usr/local/opt/libpq/lib -lpqxx -lpq
OUTDIR = out/

get_lookup_files : get_lookup_files.cxx
	$(CC) $(CPPFLAGS) -o $@ $? $(LDFLAGS)

map : map.cxx
	$(CC) $(CPPFLAGS) -o $@ $? $(LDFLAGS)

voucher_details.o : voucher_details.cxx
	$(CC) -c $? 

voucher_detail_line.o : voucher_detail_line.cxx
	$(CC) -c $? 

voucher.o : voucher.cxx
	$(CC) -c $?

pgutil.o : pgutil.cxx pgutil.hxx
	$(CC) -c $?

%.o : %.cxx
	$(CC) $(CPPFLAGS) -c $? 

libvoucher.dylib : voucher.o voucher_detail_line.o voucher_details.o pgutil.o
	$(CC) $(CPPFLAGS) -v -dynamiclib $? -o $@  $(LDFLAGS)


# Failed XCode 
#libpyctest.dylib : cli_test/libpyctest.dylib/libpyctest_dylib.cpp
#	$(CC) $(CPPFLAGS) -v -dynamiclib $? -o $@
#	cp libpyctest.dylib /usr/local/lib

libpyctest.dylib : pyctest.o
	$(CC) $(CPPFLAGS) -dynamiclib $? -o $@

test_voucher_detail : test_voucher_detail.cxx
	$(CC) $(CPPFLAGS) -o $(OUTDIR)$@ $? $(LDFLAGS)

test_voucher : test_voucher.cxx
	$(CC) $(CPPFLAGS) -o $(OUTDIR)$@ $? $(LDFLAGS)

test_pgutil : test_pgutil.cxx
	$(CC) $(CPPFLAGS) -o $(OUTDIR)$@ $? $(LDFLAGS) -L. -lvoucher

test_libpyctest : test_libpyctest.cxx
	$(CC) $(CPPFLAGS) -o $(OUTDIR)$@ $? -L. -lpyctest

ilac_console : ilac_console.cxx
	$(CC) $(CPPFLAGS) -o $(OUTDIR)$@ $? $(LDFLAGS) -L. -lvoucher


