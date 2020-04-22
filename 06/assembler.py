# Defining some basic dictionaries

# Computation bits for c command
comp = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
}

# Destination bits for c command
dest = {
    "null": "000",
    "M": "001",
    "D": "010",
    "A": "100",
    "MD": "011",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

# jump bits for c command
jump = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

# predefined constants
table = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576,
}


# Adding R0 .. R15
for i in range(0, 16):
    label = "R" + str(i)
    table[label] = i



# Adding Jump variables along with line numbers
def first_pass(lines):
    number = 0
    for line in lines:
        line = line.lstrip()
        if line == '' or line[:2] == '//':
            continue
        if line[0] == '(':
            table[line[1:-2]] = number
            continue
        number += 1


# Adding memory variables
def second_pass(lines):
    number = 16
    for line in lines:
        line = line.lstrip()
        if line[0:1] == '@' and line[1:-1] not in table and not line[1:-1].isnumeric():
            table[line[1:-1]] = number
            number += 1


# Returns A instruction in hack binary
def A_inst(instruction):
    if instruction[1:].isnumeric():
        number = int(instruction[1:])
    else:
        number = table[instruction[1:]]
    return str(format(number, '#018b'))[2:]


# Returns C instruction in hack binary
def C_inst(instruction):
    a, b, c = parse_c(instruction)
    return trans_c(a, b, c)


# Normalises the C instruction
def parse_c(instruction):
    if ';' in instruction and '=' in instruction:
        jumpk = instruction[-3:]
        destk = instruction[0:instruction.index('=')]
        compk = instruction[instruction.index('=')+1:instruction.index(';')]
    if ';' in instruction and '=' not in instruction:
        destk = 'null'
        jumpk = instruction[-3:]
        compk = instruction[0:instruction.index(';')]
    if '=' in instruction and ';' not in instruction:
        jumpk = 'null'
        destk = instruction[0:instruction.index('=')]
        compk = instruction[instruction.index('=')+1:]
    return compk, destk, jumpk


# builds C instruction from its components
def trans_c(compk, destk, jumpk):
    return '111' + comp[compk] + dest[destk] + jump[jumpk]


# Translates normal instruction
def inst(line):
    if line[0:1] == '@':
        return A_inst(line)
    else:
        return C_inst(line)

# Normalises lines and assembles the program
def assemble(lines):
    for line in lines:
        line = line.strip()
        if line == '' or line[:2] == '//' or line[:1] == '(':
            continue
        print(inst(line))


with open('Pong.asm') as Pong_obj:
    lines = Pong_obj.readlines()

first_pass(lines)
second_pass(lines)
# print(table['ponggame.0'])
# print(table)
assemble(lines)
