program halexit
	call execute_command_line('bash runb.sh')
	call execute_command_line("kill -9 $(ps -A -o pid= -o args= | grep 'python3 main.py' | awk '{print $1}') 2> /dev/null") !kills the program
end program halexit
