# MIT License

# Copyright (c) 2017 - 2018 Brice Vadnais

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Instruction Set Simulator to demonstrate custom instruction set architecture


""" Change asmtest.asm to the name of the assembly to be tested
    The file must be located in the same directory as this file
"""
asm_file = open('asmtest.asm', 'r')


""" Don't modify below this line for program to work"""

# Initializing Registers
pc = 0
regA = 0
regB = 0
halt = False
x = 0
sp = 0
zf = 0
gt = 0
lt = 0
pcsub = 0
# 16 bits of Addressable memory space initialized with 0s
mem_size = 2 ** 16
mem = [0] * mem_size


"""
    IMPLIED/INHERENT INSTRUCTIONS
"""


def nop(opr):
    # no operation performed - program counter is incremented only
    global pc
    pc += 1


def add_acc(opr):
    # Add Accumulators A and B together - result stored in regB
    global regA, regB, pc
    regB = regA + regB
    pc += 1


def sub_acc(val):
    # Subtract Accumulator B from A - result sored in regB
    global regB, regA, pc
    regB = regA - regB
    pc += 1


def inc_a(opr):
    # Increment Accumulator A
    global pc, regA
    regA += 1
    pc += 1


def inc_b(opr):
    # Increment Accumulator B
    global pc, regB
    regB += 1
    pc += 1


def dec_a(opr):
    # Decrement regA
    global pc, regA
    regA -= 1
    pc += 1


def dec_b(opr):
    # Decrement regB
    global pc, regB
    regB -= 1
    pc += 1


def inv_a(opr):
    # Logical Invert Accumulator A
    global pc, regA
    regA = ~regA
    pc += 1


def inv_b(opr):
    # Logical Invert Accumulator B
    global pc, regB
    regB = ~regB
    pc += 1


def cmp_acc(opr):
    # Compares accumulators to set necessary flags
    global pc, regA, regB, zf, gt, lt
    if regA - regB == 0:
        # setting zero flag
        zf = 1
    if regA > regB:
        gt = 1
    if regA < regB:
        lt = 1
    pc += 1


def hlt(opr):
    # Halts the program
    global halt
    halt = True


"""
    IMMEDIATE INSTRUCTIONS
"""


def lda_imm(opr):
    # Loads Accumulator A with 8 bit immediate value
    global regA, pc
    regA = opr['opr']
    pc += 1


def ldb_imm(opr):
    # Loads Accumulator B with 8 bit immediate value
    global regB, pc
    regB = opr['opr']
    pc += 1


def adda_imm(val):
    # Add an 8 bit immediate value to Accumulator A
    global regA, pc
    regA = regA + val['opr']
    pc += 1


def addb_imm(val):
    # Add an 8 bit immediate value to Accumulator B
    global regB, pc
    regB = regB + val['opr']
    pc += 1


def suba_imm(val):
    # Subtract an 8 bit immediate value from Accumulator A
    global regA, pc
    regA = regA - val['opr']
    pc += 1


def subb_imm(val):
    # Subtract an 8 bit immediate value from Accumulator B
    global regB, pc
    regB = regB - val['opr']
    pc += 1


def ldx_imm(opr):
    # Load Index Register with a 16 bit immediate value
    global x, pc
    x = opr['opr']
    pc += 1


def lds_imm(opr):
    # Load Stack Pointer Register with a 16 bit immediate value
    global pc, sp
    sp = opr['opr']
    pc += 1


def anda_imm(opr):
    # Logical AND Accumulator A with an 8 bit immediate value
    global regA, pc
    regA = regA & opr['opr']
    pc += 1


def andb_imm(opr):
    # Logical AND Accumulator B with an 8 bit immediate value
    global regB, pc
    regB = regB & opr['opr']
    pc += 1


def ora_imm(opr):
    # Logical OR Accumulator A with an 8 bit immediate value
    global regA, pc
    regA = regA | opr['opr']
    pc += 1


def orb_imm(opr):
    # Logical OR Accumulator B with an 8 bit immediate value
    global regB, pc
    regB = regB | opr['opr']
    pc += 1


"""
    DIRECT INSTRUCTIONS
"""


def lda_dir(opr):
    # Load Accumulator A with an 8 bit value from memory
    global regA, pc
    regA = mem[opr['opr']]
    pc += 1


def ldb_dir(opr):
    # Load Accumulator B with an 8 bit value from memory
    global regB, pc
    regB = mem[opr['opr']]
    pc += 1


def adda_dir(val):
    # Add an 8 bit value from memory to Accumulator A
    global regA, pc
    regA = regA + mem[val['opr']]
    pc += 1


def addb_dir(val):
    # Add an 8 bit value from memory to Accumulator B
    global regB, pc
    regB = regB + mem[val['opr']]
    pc += 1


def suba_dir(val):
    # Subtract an 8 bit value from memory from Accumulator A
    global regA, pc
    regA = regA - mem[val['opr']]
    pc += 1


def subb_dir(val):
    # Subtract an 8 bit value from memory from Accumulator B
    global regB, pc
    regB = regB - mem[val['opr']]
    pc += 1


def sta_dir(memloc):
    # Store Accumulator A to memory
    global regA, pc
    mem[memloc['opr']] = regA
    pc += 1


def stb_dir(memloc):
    # Store Accumulator B to memory
    global regB, pc
    mem[memloc['opr']] = regB
    pc += 1


def anda_dir(val):
    # Logical AND an 8 bit value from memory to Accumulator A
    global regA, pc
    regA = regA & mem[val['opr']]
    pc += 1


def andb_dir(val):
    # Logical AND an 8 bit value from memory to Accumulator B
    global regB, pc
    regB = regB & mem[val['opr']]
    pc += 1


def ora_dir(val):
    # Logical OR an 8 bit value from memory to Accumulator A
    global regA, pc
    regA = regA | mem[val['opr']]
    pc += 1


def orb_dir(val):
    # Logical OR an 8 bit value from memory to Accumulator B
    global regB, pc
    regB = regB | mem[val['opr']]
    pc += 1


"""
    STACK INSTRUCTIONS
    Pre-decrement | Post-Increment
"""


def push_a(opr):
    # Push Accumulator A to the stack
    global sp, pc, regA
    sp -= 1
    mem[sp] = regA
    pc += 1


def push_b(opr):
    # Push Accumulator B to the stack
    global sp, pc, regB
    sp -= 1
    mem[sp] = regB
    pc += 1


def pop_a(opr):
    # Pop the value off the stack and put into Accumulator A
    global sp, pc, regA
    regA = mem[sp]
    sp += 1
    pc += 1


def pop_b(opr):
    # Pop the value off the stack and put into Accumulator B
    global sp, pc, regB
    regB = mem[sp]
    sp += 1
    pc += 1


def push_imm(opr):
    # Push an 8 bit immediate value to the stack
    global sp, pc
    sp -= 1
    mem[sp] = opr['opr']
    pc += 1


def push_dir(opr):
    # Push a value from memory into the stack
    global sp, pc
    sp -= 1
    mem[sp] = mem[opr['opr']]
    pc += 1


def push_indx(opr):
    # Push a value from the Indexed Offset in memory to the stack
    global pc, sp
    sp -= 1
    mem[sp] = mem[opr['opr']]
    pc += 1


"""
    INDEXED INSTRUCTIONS
"""


def lda_indx(opr):
    # Load Accumulator A with an Indexed Offseted value from memory
    global regA, pc
    regA = mem[int(opr['opr'])]
    pc += 1


def ldb_indx(opr):
    # Load Accumulator B with an Indexed Offseted value from memory
    global regB, pc
    regB = mem[int(opr['opr'])]
    pc += 1


def sta_indx(opr):
    # Store Accumulator A in memory at Indexed Offset Location
    global regA, pc
    mem[int(opr['opr'])] = regA
    pc += 1


def stb_indx(opr):
    # Store Accumulator B in memory at Indexed Offset Location
    global regB, pc
    mem[int(opr['opr'])] = regB
    pc += 1


def adda_indx(opr):
    # Add to Accumulator A an 8 bit value from
    # Indexed Offset Location in memory
    global regA, pc
    regA = regA + mem[int(opr['opr'])]
    pc += 1


def addb_indx(opr):
    # Add to Accumulator B an 8 bit value from
    # Indexed Offset Location in memory
    global regB, pc
    regB = regB + mem[int(opr['opr'])]
    pc += 1


def suba_indx(opr):
    # Subtract from Accumulator A an 8 bit value from
    # Indexed Offset Location in memory
    global regA, pc
    regA = regA - mem[int(opr['opr'])]
    pc += 1


def subb_indx(opr):
    # Subtract from Accumulator B an 8 bit value from
    # Indexed Offset Location in memory
    global regB, pc
    regB = regB - mem[int(opr['opr'])]
    pc += 1


def anda_indx(opr):
    # Logical AND Accumulator A with an 8 bit value from
    # Indexed Offset Location in memory
    global regA, pc
    regA = regA & mem[int(opr['opr'])]
    pc += 1


def andb_indx(opr):
    # Logical AND Accumulator B an 8 bit value from
    # Indexed Offset Location in memory
    global regB, pc
    regB = regB & mem[int(opr['opr'])]
    pc += 1


def ora_indx(opr):
    # Logical OR Accumulator A an 8 bit value from
    # Indexed Offset Location in memory
    global regA, pc
    regA = regA | mem[int(opr['opr'])]
    pc += 1


def orb_indx(opr):
    # Logical OR Accumulator B an 8 bit value from
    # Indexed Offset Location in memory
    global regB, pc
    regB = regB | mem[int(opr['opr'])]
    pc += 1


def inc_x(opr):
    # Increment Index Register value
    global pc, x
    x += 1
    pc += 1


def dec_x(opr):
    # Decrement Index Register value
    global pc, x
    x -= 1
    pc += 1


"""
    JUMP INSTRUCTIONS
"""


def jmp_imm(pcloc):
    # Jump to 16 bit Immediate Address
    global pc
    pc = int(pcloc['opr'])


def jmp_neq(pcloc):
    # Jump when Accumulator A != Accumulator B
    global pc
    if zf != 1:
        pc = int(pcloc['opr'])
    else:
        pc += 1


def jmp_eq(pcloc):
    # Jump when A = B
    global pc
    if zf == 1:
        pc = int(pcloc['opr'])
    else:
        pc += 1


def jmp_gt(pcloc):
    # Jump when A > B
    global pc
    if gt == 1:
        pc = int(pcloc['opr'])
    else:
        pc += 1


def jmp_lt(pcloc):
    # Jump when A < B
    global pc
    if lt == 1:
        pc = int(pcloc['opr'])
    else:
        pc += 1


def jmp_gte(pcloc):
    # Jump when A >= B
    global pc
    if zf == 1 or gt == 1:
        pc = int(pcloc['opr'])
    else:
        pc += 1


def jmp_lte(pcloc):
    # Jump when A <= B
    global pc
    if zf == 1 or lt == 1:
        pc = int(pcloc['opr'])
    else:
        pc += 1


def jmp_sub(pcloc):
    # Jump to Subroutine
    global pc, pcsub
    pc += 1
    pcsub = pc
    pc = int(pcloc['opr'])


def ret_sub(pcloc):
    # Return from Subroutine
    global pc, pcsub
    pc = pcsub


"""
    Currently Unsupported on Processor
    Left to demonstrate bitwise multiplication and division
"""


def mul_acc(opr):
    global regA, regB, regC, pc
    regC = 0x00
    a = regA
    b = regB
    while b != 0:
        regC += a * (b & 1)
        a <<= 1
        b >>= 1
    pc += 1


def div_acc(opr):
    global regB, regA, regC, pc
    denom = regB
    numer = regA
    mask = 0x1
    q = 0x00
    while denom <= numer:
        denom <<= 1
        mask <<= 1
    while mask > 1:
        denom >>= 1
        mask >>= 1
        if numer >= denom:
            numer -= denom
            q |= mask
    regC = q
    pc += 1

# preparing the asm file


labels = []
memory = []
newlabels = []

for lines in asm_file:
    if lines.startswith("#") or lines.startswith("\n"):
        continue
    asm_code = lines.split()
    for op in asm_code:
        memory.append(op)
len_memory = len(memory)
i_items = 0

while i_items < len_memory:
    if memory[i_items].endswith(":"):
        labels.append(memory[i_items])
        labels.append(i_items)
        memory.remove(memory[i_items])
        len_memory = len_memory - 1
    i_items += 1
for stuff in labels:
    if isinstance(stuff, int):
        newlabels.append(stuff)
    else:
        newlabels.append(stuff[:-1])

label_dict = dict(newlabels[i:i + 2] for i in range(0, len(newlabels), 2))


# look up table for assembly of program
lut = {'lda': {'imm': lda_imm, 'dir': lda_dir, 'indx': lda_indx},
       'ldb': {'imm': ldb_imm, 'dir': ldb_dir, 'indx': ldb_indx},
       'add': add_acc,
       'sub': sub_acc,
       'hlt': hlt,
       'inva': inv_a,
       'invb': inv_b,
       'jmp': {'imm': jmp_imm, 'dir': jmp_imm},
       'sta': {'imm': sta_dir, 'dir': sta_dir, 'indx': sta_indx},
       'stb': {'imm': stb_dir, 'dir': stb_dir, 'indx': stb_indx},
       'adda': {'imm': adda_imm, 'dir': adda_dir, 'indx': adda_indx},
       'addb': {'imm': addb_imm, 'dir': addb_dir, 'indx': addb_indx},
       'suba': {'imm': suba_imm, 'dir': suba_dir, 'indx': suba_indx},
       'subb': {'imm': suba_imm, 'dir': subb_dir, 'indx': subb_indx},
       'anda': {'imm': anda_imm, 'dir': anda_dir, 'indx': anda_indx},
       'andb': {'imm': andb_imm, 'dir': andb_dir, 'indx': andb_indx},
       'ora': {'imm': ora_imm, 'dir': ora_dir, 'indx': ora_indx},
       'orb': {'imm': orb_imm, 'dir': orb_dir, 'indx': orb_indx},
       'ldx': {'imm': ldx_imm},
       'lds': {'imm': lds_imm},
       'psha': push_a,
       'pshb': push_b,
       'popa': pop_a,
       'popb': pop_b,
       'psh': {'imm': push_imm, 'dir': push_dir, 'indx': push_indx},
       'inca': inc_a,
       'incb': inc_b,
       'deca': dec_a,
       'decb': dec_b,
       'nop': nop,
       'mul': mul_acc,
       'div': div_acc,
       'cmp': cmp_acc,
       'jne': {'dir': jmp_neq},
       'jeq': {'dir': jmp_eq},
       'jgt': {'dir': jmp_gt},
       'jlt': {'dir': jmp_lt},
       'jgte': {'dir': jmp_gte},
       'jlte': {'dir': jmp_lte},
       'jsr': {'dir': jmp_sub},
       'rfs': ret_sub,
       'incx': inc_x,
       'decx': dec_x
       }

for i in range(len(memory)):
    if memory[i] in lut:
        mem[i] = {}
        mem[i]['opc'] = lut[memory[i]]
        if memory[i] == 'hlt':
            mem[i]['opr'] = pc
        # print(mem,i )
    elif memory[i].startswith('0x'):
        mem[i - 1].update({'opc': mem[i - 1]['opc']['imm'],
                           'opr': int(memory[i], 16)})
        # print(mem,i)
    elif memory[i].startswith('['):
        memory[i] = memory[i].strip('[]')
        if memory[i].startswith('X') or memory[i].startswith('x'):
            tmpindx = memory[i].split('+')
            mem[i - 1].update({'opc': mem[i - 1]['opc']
                               ['indx'], 'opr': tmpindx[1]})
        elif memory[i].startswith('0x'):
            mem[i - 1].update({'opc': mem[i - 1]['opc']
                               ['dir'], 'opr': int(memory[i], 16)})
        elif isinstance(memory[i], str):
            mem[i - 1].update({'opc': mem[i - 1]['opc']
                               ['dir'], 'opr': label_dict[memory[i]]})
        else:
            continue
    else:
        continue


# execute the code
while pc < len(mem):
    if mem[pc] == 0:
        pc += 1
        continue
    elif halt is True:
        break
    elif "_indx" in str(mem[pc]['opc']):
        mem[int(pc)]['opr'] = int(mem[pc]['opr']) + x
        print("PC: %X  A: %X  B: %X  X:%X SP:%X" %
              (pc, regA, regB, x, sp))
        Inx = mem[pc]
        Opx = Inx['opc']
        Opx(Inx)
    else:
        print("PC: %X  A: %X  B: %X  X:%X SP:%X" %
              (pc, regA, regB, x, sp))
        Inx = mem[pc]
        Opx = Inx['opc']
        Opx(Inx)


for iii in range(len(mem)):

    if mem[iii] == 0:
        continue
    elif type(mem[iii]) == dict:
        print("%x %s" % (iii, mem[iii]))
    elif type(mem[iii]) == int:
        print("%x %s" % (iii, format(mem[iii], '02X')))
    else:
        continue
