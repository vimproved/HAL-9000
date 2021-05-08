program halexit
	logical :: ex
	character(16) :: ptk
	
	inquire(exist=ex,file=".inpid")
	if (.not.ex) then
		call execute_command_line("mkfifo .inpid")
	end if
	call execute_command_line('bash runb.sh')
	
	call execute_command_line("echo 'c' > .inpid&") !freezes if you dont do this
	open(9,file='.inpid',action='read')
	read(9,'(A)') ptk

	call execute_command_line('ps -C "python3 main.py" -o pid= > .inpid&') !gets the process id
	read(9,'(A)') ptk
	call execute_command_line('kill -9 '//trim(adjustl(ptk))) !kills the programs

	close(9)
end program halexit
