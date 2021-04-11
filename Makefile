# Compilers
CXX = g++

# Flags
EXTRA_CFLAGS=
CXXFLAGS = -Wall -Wextra $(EXTRA_CFLAGS)
#CXXFLAGS = $(CFLAGS)
LDFLAGS = -lm -lstdc++

# Binary file
TARGET = tiny_mc

# Files
CXX_SOURCES = tiny_mc.cpp
CXX_OBJS = $(patsubst %.cpp, %.o, $(CXX_SOURCES))

# Rules
all: $(TARGET)

$(TARGET): $(CXX_OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS)

clean:
	rm -f $(TARGET) *.o

