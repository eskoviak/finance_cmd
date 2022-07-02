CPPFLAGS = -I/usr/local/opt/libpqxx/include 
#-I. -I/usr/local/include
#CC = g++ -std=c++2a
CC = clang++ -stdlib=libc++ -std=c++2a
LDFLAGS = -L/usr/local/opt/libpqxx/lib -L/usr/local/opt/libpq/lib -lpqxx -lpq

get_lookup_files : get_lookup_files.cxx
	$(CC) $(CPPFLAGS) -o $@ $? $(LDFLAGS)

map : map.cxx
	$(CC) $(CPPFLAGS) -o $@ $? $(LDFLAGS)

#voucher_details.o : voucher_details.cxx
#	$(CC) -c $? 

#voucher_detail_line.o : voucher_detail_line.cxx
#	$(CC) -c $? 

#voucher.o : voucher.cxx
#	$(CC) -c $?

*.o : *.cxx
	$(CC) $(CPPFLAGS) -c $? 

libvoucher.dylib : voucher_detail_line.o voucher_details.o voucher.o pgutil.o
	$(CC) $(CPPFLAGS) -v -dynamiclib $? -o $@  $(LDFLAGS)

test_voucher_detail : test_voucher_detail.cxx
	$(CC) $(CPPFLAGS) -o $@ $? $(LDFLAGS)

test_voucher : test_voucher.cxx
	$(CC) $(CPPFLAGS) -o $@ $? $(LDFLAGS)

test_pgutil : test_pgutil.cxx
	$(CC) $(CPPFLAGS) -o $@ $? $(LDFLAGS) -L. -lvoucher

