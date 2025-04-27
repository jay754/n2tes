// Initialize stack pointer
@256
D=A
@SP
M=D  // Set stack pointer (SP) to 256

// push constant 10
@10
D=A
@SP
A=M
M=D
@SP
M=M+1  // Increment SP after pushing 10

// push constant 20
@20
D=A
@SP
A=M
M=D
@SP
M=M+1  // Increment SP after pushing 20

// pop local 0
@LCL
D=M         // Get the base address of LCL
@0          // Load the index (0)
A=D+A       // Compute the address of local[0]
D=A         // Store the computed address in D
@R13        // Store it in temporary register R13
M=D

@SP
M=M-1       // Decrement SP to point to the top value (20)
A=M         // Set A to the current top of the stack
D=M         // Store the value to be popped in D
@R13        // Get the address of local[0]
A=M         // Set A to point to local[0]
M=D         // Store the popped value at local[0]
