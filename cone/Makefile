.POSIX:
.SUFFIXES:

main       = aa.out
.PHONY: all

all: $(main)

$(main):
	export PYTHONPATH=$PYTHONPATH:$PATH
	gcc -fPIC -shared -L/usr/local/lib -I/usr/include/ -I/usr/include/python3.9 -lpython3.9 -o b.so hal.c hal.s -g -O0
