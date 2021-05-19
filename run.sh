gfortran runhal.f90
kill -9 $(ps -A -o pid= -o args= | grep "a.out" | awk '{print $1}') 2> /dev/null
kill -9 $(ps -A -o pid= -o args= | grep "bash runb.sh" | awk '{print $1}') 2> /dev/null
kill -9 $(ps -A -o pid= -o args= | grep "python3 main.py" | awk '{print $1}') 2> /dev/null
./a.out
