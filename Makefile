CPPFLAGS = -I/usr/local/opt/libpqxx/include
CCFLAGS = -I/usr/local/opt/libpq/include
#-I. -I/usr/local/include
CC = clang
CPP = clang++ -stdlib=libc++ -std=c++2a
LDFLAGS = -L/usr/local/opt/libpqxx/lib -L/usr/local/opt/libpq/lib -lpqxx -lpq
OUTDIR = out/

get_lookup_files : get_lookup_files.cxx
	$(CPP) $(CPPFLAGS) -o $@ $? $(LDFLAGS)

map : map.cxx
	$(CPP) $(CPPFLAGS) -o $@ $? $(LDFLAGS)

voucher_details.o : voucher_details.cxx
	$(CPP) -c $? 

voucher_detail_line.o : voucher_detail_line.cxx
	$(CPP) -c $? 

voucher.o : voucher.cxx
	$(CPP) -c $?

pgutil.o : pgutil.cxx pgutil.hxx
	$(CPP) -c $?

%.o : %.cxx
	$(CPP) $(CPPFLAGS) -c $? 

libvoucher.dylib : voucher.o voucher_detail_line.o voucher_details.o pgutil.o
	$(CPP) $(CPPFLAGS) -v -dynamiclib $? -o $@  $(LDFLAGS)


# Failed XCode 
#libpyctest.dylib : cli_test/libpyctest.dylib/libpyctest_dylib.cpp
#	$(CPP) $(CPPFLAGS) -v -dynamiclib $? -o $@
#	cp libpyctest.dylib /usr/local/lib

libpyctest.dylib : pyctest.o
	$(CPP) $(CPPFLAGS) -dynamiclib $? -o $@

test_voucher_detail : test_voucher_detail.cxx
	$(CPP) $(CPPFLAGS) -o $(OUTDIR)$@ $? $(LDFLAGS)

test_voucher : test_voucher.cxx
	$(CPP) $(CPPFLAGS) -o $(OUTDIR)$@ $? $(LDFLAGS)

test_pgutil : test_pgutil.cxx
	$(CPP) $(CPPFLAGS) -o $(OUTDIR)$@ $? $(LDFLAGS) -L. -lvoucher

test_libpyctest : test_libpyctest.cxx
	$(CPP) $(CPPFLAGS) -o $(OUTDIR)$@ $? -L. -lpyctest

ilac_console : ilac_console.cxx
	$(CPP) $(CPPFLAGS) -o $(OUTDIR)$@ $? $(LDFLAGS) -L. -lvoucher

test_pgconn : test_pgconn.c
	$(CC) $(CCFLAGS) -o $(OUTDIR)$@ $? $(LDFLAGS)