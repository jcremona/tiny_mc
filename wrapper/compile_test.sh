g++ -c boost_wrapper.cpp -o boost_wrapper.o
gcc -Wall -Wextra -c test_random.c -o test_random.o
g++ test_random.o boost_wrapper.o -o test_random
