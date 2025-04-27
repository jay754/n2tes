def handle_push(segment, index, asm_file):
    """Handles the 'push' command for various memory segments."""
    if segment == "constant":
        # For push constant X: push the value X onto the stack
        asm_file.write(f"// push constant {index}\n")
        asm_file.write(f"@{index}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
    elif segment in ["local", "argument", "this", "that"]:
        # For push from segments like local, argument, this, that
        segment_dict = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT"
        }
        asm_file.write(f"// push {segment} {index}\n")
        asm_file.write(f"@{segment_dict[segment]}\nD=M\n@{index}\nA=D+A\nD=M\n")
        asm_file.write(f"@SP\nA=M\nM=D\n@SP\nM=M+1\n")
    elif segment == "static":
        # For push static X
        asm_file.write(f"// push static {index}\n")
        asm_file.write(f"@{index}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
    elif segment == "temp":
        # For push temp X
        asm_file.write(f"// push temp {index}\n")
        asm_file.write(f"@5\nD=A\n@{index}\nA=D+A\nD=M\n")
        asm_file.write(f"@SP\nA=M\nM=D\n@SP\nM=M+1\n")
    elif segment == "pointer":
        # For push pointer X (pointer 0 is 'this', pointer 1 is 'that')
        segment_dict = {
            0: "THIS",
            1: "THAT"
        }
        asm_file.write(f"// push pointer {index}\n")
        asm_file.write(f"@{segment_dict[index]}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")


def handle_pop(segment, index, asm_file):
    """Handles the 'pop' command for various memory segments."""
    if segment in ["local", "argument", "this", "that"]:
        # For pop to segments like local, argument, this, that
        segment_dict = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT"
        }
        
        asm_file.write(f"// pop {segment} {index}\n")
        asm_file.write(f"@{segment_dict[segment]}\nD=M\n@{index}\nA=D+A\nD=A\n@R13\nM=D\n")
        asm_file.write(f"@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n")
    elif segment == "static":
        # For pop to static X
        asm_file.write(f"// pop static {index}\n")
        asm_file.write(f"@SP\nM=M-1\nA=M\nD=M\n@{index}\nM=D\n")
    elif segment == "temp":
        # For pop to temp X
        asm_file.write(f"// pop temp {index}\n")
        asm_file.write(f"@5\nD=A\n@{index}\nA=D+A\nD=A\n@R13\nM=D\n")
        asm_file.write(f"@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n")
    elif segment == "pointer":
        # For pop to pointer X (pointer 0 is 'this', pointer 1 is 'that')
        segment_dict = {
            0: "THIS",
            1: "THAT"
        }

        asm_file.write(f"// pop pointer {index}\n")
        asm_file.write(f"@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n")
    else:
        raise ValueError(f"Unknown segment for pop: {segment}")

def handle_arithmetic(command, asm_file):
    """Handles arithmetic operations like add, sub, neg, eq, gt, lt, and, or, not."""
    
    if command == "add":
        asm_file.write("// add\n")
        asm_file.write("""
        @SP
        M=M-1       // Decrement SP to point to the top value
        A=M         // Set A to point to the current top of the stack (second value)
        D=M         // Store the second value in D
        
        @SP
        M=M-1       // Decrement SP again to point to the next value
        A=M         // Set A to point to the next value (first value)
        M=D+M       // Add the values and store the result
        
        @SP
        M=M+1       // Increment SP to point to the next available space
        """)
    
    elif command == "sub":
        asm_file.write("// sub\n")
        asm_file.write("""
        @SP
        M=M-1       // Decrement SP to point to the top value
        A=M         // Set A to point to the current top of the stack (second value)
        D=M         // Store the second value in D
        
        @SP
        M=M-1       // Decrement SP again to point to the next value
        A=M         // Set A to point to the next value (first value)
        M=M-D       // Subtract the values and store the result
        
        @SP
        M=M+1       // Increment SP to point to the next available space
        """)

    elif command == "neg":
        asm_file.write("// neg\n")
        asm_file.write("""
        @SP
        M=M-1       // Decrement SP to point to the top value
        A=M         // Set A to point to the current top of the stack
        M=-M        // Negate the value
        
        @SP
        M=M+1       // Increment SP to point to the next available space
        """)

    elif command == "and":
        asm_file.write("// and\n")
        asm_file.write("""
        @SP
        M=M-1       // Decrement SP to point to the top value
        A=M         // Set A to point to the current top of the stack (second value)
        D=M         // Store the second value in D
        
        @SP
        M=M-1       // Decrement SP again to point to the next value
        A=M         // Set A to point to the next value (first value)
        M=D&M       // Perform AND and store the result
        
        @SP
        M=M+1       // Increment SP to point to the next available space
        """)
        
    elif command == "or":
        asm_file.write("// or\n")
        asm_file.write("""
        @SP
        M=M-1       // Decrement SP to point to the top value
        A=M         // Set A to point to the current top of the stack (second value)
        D=M         // Store the second value in D
        
        @SP
        M=M-1       // Decrement SP again to point to the next value
        A=M         // Set A to point to the next value (first value)
        M=D|M       // Perform OR and store the result
        
        @SP
        M=M+1       // Increment SP to point to the next available space
        """)
    
    elif command == "not":
        asm_file.write("// not\n")
        asm_file.write("""
        @SP
        M=M-1       // Decrement SP to point to the top value
        A=M         // Set A to point to the current top of the stack
        M=!M        // Perform bitwise NOT
        
        @SP
        M=M+1       // Increment SP to point to the next available space
        """)

def translate(input_file, output_file):
    """Reads the VM file and generates Hack assembly code."""
    with open(input_file, 'r') as vm_file, open(output_file, 'w') as asm_file:
        
        # Initialize stack pointer to 256
        asm_file.write("// Initialize stack pointer\n")
        asm_file.write("@256\nD=A\n@SP\nM=D\n\n")

        for line in vm_file:
            line = line.strip().split('//')[0]  # Remove comments and whitespace
            if not line:
                continue  # Skip empty lines

            tokens = line.split()  # Split the line into tokens
            command = tokens[0]

            # Handle arithmetic commands
            if command in ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]:
                handle_arithmetic(command, asm_file)
            # Handle push/pop commands
            elif command == "push":
                handle_push(tokens[1], tokens[2], asm_file)
            elif command == "pop":
                handle_pop(tokens[1], tokens[2], asm_file)

# Example usage
input_file = "main.vm"   # Input VM file
output_file = "main.asm"  # Output Hack assembly file
translate(input_file, output_file)
