# Predefined symbol table with initial values
symbol_table = {
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
    "R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4, "R5": 5, 
    "R6": 6, "R7": 7, "R8": 8, "R9": 9, "R10": 10, "R11": 11,
    "R12": 12, "R13": 13, "R14": 14, "R15": 15,
    "SCREEN": 16384, "KBD": 24576
}

# Function to parse A-instruction
def parse_a_instruction(instruction, symbol_table, next_available_address):
    instruction = instruction.split("//")[0].strip()
    
    if instruction.startswith("@"):
        value = instruction[1:].strip()

        if value.isdigit():
            binary_value = format(int(value), '016b')
            return binary_value, symbol_table, next_available_address
        else:
            if value in symbol_table:
                address = symbol_table[value]
            else:
                symbol_table[value] = next_available_address
                address = next_available_address
                next_available_address += 1

            binary_value = format(address, '016b')
            return binary_value, symbol_table, next_available_address

# Function to parse C-instruction
def parse_c_instruction(instruction):
    instruction = instruction.split("//")[0].strip()

    dest_dict = {
        '': '000', 'M': '001', 'D': '010', 'MD': '011', 'A': '100', 'AM': '101', 'AD': '110', 'AMD': '111'
    }

    comp_dict = {
        '0': '0101010', '1': '0111111', '-1': '0111010', 'D': '0001100', 'A': '0000001', 'M': '1110000',
        'D+1': '0011111', 'A+1': '0000111', 'D-1': '0000011', 'A-1': '0000110', 'D+A': '0000010',
        'D-A': '0010011', 'A-D': '0000111', 'D&A': '0000000', 'D|A': '0010101'
    }

    jump_dict = {
        '': '000', 'JEQ': '001', 'JGT': '010', 'JLT': '011', 'JNE': '100', 'JGE': '101', 'JLE': '110', 'JMP': '111'
    }

    if '=' in instruction and ';' in instruction:
        dest, comp_jump = instruction.split('=')
        comp, jump = comp_jump.split(';')
    elif '=' in instruction:
        dest, comp = instruction.split('=')
        jump = ''
    elif ';' in instruction:
        dest = ''
        comp, jump = instruction.split(';')

    dest_bin = dest_dict.get(dest, '000')
    comp_bin = comp_dict.get(comp, '0000000')
    jump_bin = jump_dict.get(jump, '000')

    binary_instruction = '111' + comp_bin + dest_bin + jump_bin
    return binary_instruction

# Combine A-instruction and C-instruction parsing
def assemble(instructions, symbol_table):
    machine_code = []
    next_available_address = 16  # Start the address for new variables from 16

    for instruction in instructions:
        instruction = instruction.strip()

        if instruction.startswith("@"):  # A-instruction
            binary_instruction, symbol_table, next_available_address = parse_a_instruction(instruction, symbol_table, next_available_address)
            machine_code.append(binary_instruction)
        
        elif '=' in instruction or ';' in instruction:  # C-instruction
            binary_instruction = parse_c_instruction(instruction)
            machine_code.append(binary_instruction)

    return machine_code

# Step 1: Read the assembly file
def read_asm_file(file_path):
    with open(file_path, 'r') as file:
        instructions = []

        for line in file:
            line = line.split("//")[0].strip()
            
            if line: 
                instructions.append(line)
        
        return instructions

# Step 2: Write the machine code to a .hack file
def write_hack_file(output_path, machine_code):
    with open(output_path, 'w') as file:
        for code in machine_code:
            file.write(code + '\n')

# Example usage
assembly_file_path = 'Pong.asm'  
hack_file_path = 'Pong.hack'

# Step 1: Read the assembly code
instructions = read_asm_file(assembly_file_path)

# Step 2: Assemble the code into machine code
machine_code = assemble(instructions, symbol_table)

# Step 3: Write the machine code to the .hack file
write_hack_file(hack_file_path, machine_code)

print(f"Machine code written to {hack_file_path}")
