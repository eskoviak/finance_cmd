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
