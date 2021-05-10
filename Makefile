# Compilers
CC = gcc

# Flags
EXTRA_CFLAGS=
CFLAGS = -std=gnu11 -Wall -Wextra $(EXTRA_CFLAGS)
LDFLAGS = -lm 

ISPC=ispc
EXTRA_ISPCFLAGS=
ISPCFLAGS=-O3 --opt=fast-math $(EXTRA_ISPCFLAGS)


# Binary file
TARGET = tiny_mc

# Files
C_SOURCES = tiny_mc.c
C_OBJS = $(patsubst %.c, %.o, $(C_SOURCES))

# Rules
all: $(TARGET)

$(TARGET): $(C_OBJS) photon.o
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

photon.o: photon.ispc
	$(ISPC) $(ISPCFLAGS) -o $@ $<

clean:
	rm -f $(TARGET) *.o *.profraw

