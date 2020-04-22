// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
@R0
	D=M	// copy R0
@ZERO
	D;JEQ 	// special case for multiplication of 0
@a
	M=D	// variable a which holds R0 and will act as the counter
@R2
	M=0	// initialise to zero, this is where we will get the result

(LOOP)
	@R1
	D=M

	@R2
	M=M+D	// R1 + R2
	
	@a
	M=M-1;	// Decrement counter
	D=M

	@LOOP
	D;JGT	// If counter 0, jump to end.

(END)
	@END
	0;JMP
(ZERO)
	@R2
	M=D
	@END
	0;JMP
