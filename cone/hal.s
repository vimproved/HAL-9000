.global pps
.global mfree
.section .text
exit:
	movl  $1,    %eax
	movl  $0,    %ebx
	int   $0x80

malloc:
	pushq %rbp
	movq %rax, %rsi
	movq $9,   %rax
	movq $0,   %rdi
	movq $0,   %r9
	movq $0x7, %rdx
	movq $0x21,%r10
	movq $-1,  %r8
	syscall
	popq %rbp
	ret

open:
	movq %rax,   %rdi
	movq $2,     %rax
	movq $42,    %rdx
	movq $0x1b6, %rsi
	syscall
	ret

read:
	movq %rax, %rdi
	movq %rbx, %rdx
	movq %rcx, %rsi
	movq $0,   %rax
	syscall
	ret

write:
	movq %rax, %rdi
	movq %rbx, %rdx
	movq %rcx, %rsi
	movq $1,   %rax
	syscall
	ret
mfree:
	pushq %rbp
	pushq %rbx
	pushq %r12
	pushq %r13
	pushq %r14
	pushq %r15
	movq $11, %rax
	syscall
	popq %r15
	popq %r14
	popq %r13
	popq %r12
	popq %rbx
	popq %rbp
	ret
ppserrB:
	movq  %rax,   %rdi
	movq  (%rax), %rsi
	call mfree
ppserr:
	movq $0, %rax
	movq %rbp, %rsp
	jmp ppsplaceB
pps:
	pushq %rbp
	pushq %rbx
	pushq %r12
	pushq %r13
	pushq %r14
	pushq %r15
	pushfq
	movq %rsp, %rbp
	cmp $9, %rsi
	jle ppserr
	pushq %rdi
	movb  $3,    %bh
	movq  %rdi, %rdx
	addq  %rsi, %rdx
	subq  $3,   %rdx
	ppsloopB: //first pass
		cmpq %rdx, %rdi
		jge  ppserr
		movq $0, %rax
		movq $3, %rcx
		ppsloopA:
			shlq $4,    %rax
			movb (%rdi), %bl
			subb $0x30,  %bl
			cmpb $0x10,  %bl
			jle  ppsplaceA
			subb $0x07,  %bl
			andb $0x0f,  %bl
			ppsplaceA:
			orb  %bl,    %al
			incq %rdi
		loop ppsloopA
		pushq %rax
		addq  %rax, %rdi
		decb  %bh
	jne ppsloopB
	
	addq $3, %rdx
	cmpq %rdx, %rdi
	jne  ppserr
	
	popq %rcx
	popq %rbx
	popq %rax
	
	popq  %rdx
	pushq %rcx
	pushq %rbx
	pushq %rax
	addq  %rax, %rbx
	addq  %rbx, %rcx
	pushq %rbx
	pushq %rax
	pushq %rcx
	pushq %rdx
	
	movq %rcx,   %rax
	addq $24,    %rax
	call malloc
	movq %rax,   %rbx
	popq %rdi
	popq %rcx
	movq %rcx, (%rax)
	popq %rcx
	movq %rcx, 0x08(%rax)
	popq %rcx
	movq %rcx, 0x10(%rax)
	addq $24,        %rbx
	
	movq $0,         %rsi
	movb $3,          %dh
	ppsloopD:
		popq %rcx
		addq $3,         %rdi
		cmpq $0, %rcx
		jz ppserrB
		ppsloopC:
			movb (%rdi,%rsi), %dl
			movb %dl, (%rbx,%rsi)
			incq %rsi
		loop ppsloopC
		decb %dh
	jne ppsloopD
	
	ppsplaceB:
	
	popfq
	popq %r15
	popq %r14
	popq %r13
	popq %r12
	popq %rbx
	popq %rbp
	ret
	//call exit
