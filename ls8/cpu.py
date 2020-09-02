"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # self.cpu = [0] * 256 # 256 = 32 * 8,
        self.pc = 0
        self.mar = [0] * 8
        self.mdr = [0] * 8 
        self.ir = [0] * 8 
        self.reg = {
            0 : [0] * 8, 
            1 : [0] * 8,
            2 : [0] * 8, 
            3 : [0] * 8, 
            4 : [0] * 8, 
            5 : [0] * 8, # reserved as the interrupt mask (IM)
            6 : [0] * 8, # reserved as the interrupt status (IS)
            7 : [0] * 8  # reserved as the stack pointer (SP)
        }
        
        self.ram = [0] * 8
        # self.ccr : [0] * 8
        # self.SP: 
        self.fl = False
        #self.ie = {}
        # TODO add initialization of stack pointer here

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, address):
        # print(self.ram[address])
        if type(address) == int:
            return self.ram[address]
    
    def ram_write(self, value, address):
        self.ram[address] = value

    def run(self):
        """Run the CPU."""
        self.trace()

       
        # self.mar = self.pc
        # self.mdr = ram[self.pc] 
        # self.ir = program[self.pc]

