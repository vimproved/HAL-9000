.POSIX:
.SUFFIXES:

main       = aa.out
.PHONY: all

all: $(main)

$(main):
	export PYTHONPATH=$PYTHONPATH:/home/soup/notdownloads/HAL-9000-loup/cone/
	gcc -fPIC -shared -L/usr/local/lib -I/usr/include/ -I/usr/include/python3.9 -lpython3.9 -o b.so hal.c hal.s -g -O0
