# Compiler Info
CXX := clang++
CXX_FLAGS :=
CXX_STD := -std=c++2b

# Includes
INCLUDES := -I/usr/local/include -I/opt/homebrew/Cellar/libpq/16.0/include

# Target and Destination
SRC := src
BUILD := build

# Sources
SRCS := $(SRC)/vendors.cpp $(SRC)/vendortest.cpp
OBJS := $(SRCS:.cpp=$(BUIID)/.o)

# Linking
LFLAGS := -L/usr/local/lib -L/opt/homebrew/Cellar/libpq/16.0/lib
LIB_FLAG := -dynamiclib
LIBS := -lpqxx -lpq

.cpp.o:
	$(CXX) $(CXX_FLAGS) $(CXX_STD) $(INCLUDES) -c $< -o $@

$(BUILD)/vendors.o : $(SRC)/vendors.cpp $(SRC)/vendors.hpp
	$(CXX) $(CXX_FLAGS) $(CXX_STD) $(INCLUDES) -c $< -o $@	

$(BUILD)/vendorstest.o : $(SRC)/vendorstest.cpp
	$(CXX) $(CXX_FLAGS) $(CXX_STD) $(INCLUDES) -c $< -o $@	

vendors_sa : $(BUILD)/vendors.o $(BUILD)/vendorstest.o
	$(CXX) $(CXX_STD) -o vendors_sa $?

# =============================================================================
# Database targets
# =============================================================================
PG_BIN  := /opt/homebrew/Cellar/postgresql@18/18.1_1/bin
PG_CONN := -h localhost -p 5432 -U postgres -d finance

.PHONY: refresh-test-db

## Recreate finance_tst schema and load last-100-voucher subset from finance.
## Reads PGPASSWORD from the environment (export it or prefix the make call).
## Usage: PGPASSWORD='<pass>' make refresh-test-db
refresh-test-db:
	PGPASSWORD="$(PGPASSWORD)" $(PG_BIN)/psql $(PG_CONN) -f db/01_recreate_finance_tst.sql
	PGPASSWORD="$(PGPASSWORD)" $(PG_BIN)/psql $(PG_CONN) -f db/02_load_finance_tst.sql
