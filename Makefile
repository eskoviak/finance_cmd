# Compiler Info
CXX := clang++
CXX_FLAG :=
CXX_STD := c++2b

# Includes
INCLUDE := -I/usr/local/include -I/opt/homebrew/Cellar/libpq/16.0/include

# Target and Destination
SRC := src
BUILD := build

# Linking
LFLAGS := -L/usr/local/lib -L/opt/homebrew/Cellar/libpq/16.0/lib
LIB_FLAG := -dynamiclib
LIBS := -lpqxx -lpq

