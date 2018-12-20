all:TAR

CC=g++
CPPFLAGS=-Wall -std=c++11 -ggdb
LDFLAGS=-pthread

TAR:TAR.o
	    $(CC) $(LDFLAGS) -o $@ $^

TAR.o:TAR.cpp
	    $(CC) $(CPPFLAGS) -o $@ -c $^


.PHONY:
	    clean

clean:
	    rm TAR.o TAR
