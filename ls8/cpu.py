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
        # self.reg = {
        #     0 : [0], 
        #     1 : [0],
        #     2 : [0], 
        #     3 : [0], 
        #     4 : [0], 
        #     5 : [0], # reserved as the interrupt mask (IM)
        #     6 : [0], # reserved as the interrupt status (IS)
        #     7 : [0]  # reserved as the stack pointer (SP)
        # }
        self.reg = [0] * 8
        
        # boot
        self.fl = [0] * 8 # 0 for false and 1 for true
        self.mar = self.pc
        self.reg[7] = 0xF4
        self.ram = [0] * 2048 # 256 bytes * 8 bits/byte = 2048bits

        # self.ccr : [0] * 8
        # self.ie = {}

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


    def alu(self, op, reg_a = 0, reg_b = 0):
        """ALU operations."""
        
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            self.pc += 3

        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
            self.pc += 3

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
            self.pc += 3

        elif op == "DIV":
            if self.reg[reg_b] == 0:
                print("error: cannot divide by zero")
            self.reg[reg_a] /= self.reg[reg_b]
            self.pc += 3

        elif op == "CMP":
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl[-3] = 1
                self.pc += 3
            else:
                self.fl[-3] = 0
                self.pc += 3


            if self.reg[reg_a] > self.reg[reg_b]:
                self.fl[-2] = 1
                self.pc += 3

            else:
                self.fl[-2] = 0
                self.pc += 3


            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl[-1] = 1
                self.pc += 3

            else:
                self.fl[-1] = 0
                self.pc += 3

        


        else:
            raise Exception("Unsupported ALU operation")
            

    def non_alu(self, op, reg_a = 0, reg_b = 0):
        
        if op == "LDI":
                            
            self.reg[reg_a] = reg_b
            
            # print(self.reg[reg_a])
            self.pc += 3
            print(f'LDI done')

        elif op == "PRN":
            print(self.reg[reg_a])
            self.pc += 2
            print('PRN done')

        elif op == "HLT":
            # running = False
            self.pc += 1
            # print('HLT done')

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
        # if type(address) == int:
        #     return self.ram[address]
        # print(self.ram[address])
        self.mar = address
        self.ir = self.ram[address]
        return self.ir
    
    def ram_write(self, value, address):
        self.mdr = value
        self.mar = address
        self.ram[address] = value

    def run(self):
        """Run the CPU."""

        # self.trace()

       
        # print(self.mar)
        # print(self.ram[self.pc])
        # print(self.reg[7])
       
        # self.mdr = ram[self.pc] 
        binary_program = [bin(i) for i in self.ram]
        decimal_program = [i for i in self.ram]
        # print(binary_program)
        # print(decimal_program)
        instruction = self.ram_read(self.pc)
        operand_a = self.ram_read(self.pc+1)
        operand_b = self.ram_read(self.pc+2)
        # print(instruction >> 5 & 0b1)
        print(instruction >> 5 == 1)

        handle_by_alu = False
        op = ''
        print(f'instruction: {bin(instruction)}')
        running = True
        while running:
            if instruction >> 5 == 0:
                # handled by alu()
                handled_by_alu = True
                if bin(instruction)[-4:] == '0000':
                    op = 'ADD'
                    self.alu('ADD', operand_a, operand_b)
                elif bin(instruction)[-4:] == '0010':
                    op = 'MUL'
                    self.alu('MUL', operand_a, operand_b)

                elif bin(instruction)[-4:] == '1000':
                    op = 'AND'
            else:
                # not handled by alu()
                handled_by_alu = False
                if bin(instruction)[-4:] == '0010':
                    op = 'LDI'
                    self.non_alu('LDI', operand_a, operand_b)
                    print(self.reg[operand_a] == operand_b)
                elif bin(instruction)[-4:] == '0111':
                    op = 'PRN'
                    self.non_alu('PRN', operand_a)

                elif bin(instruction)[-4:] == '0001':
                    op = 'HLT'
                    self.non_alu('HLT', operand_a)


                

        

        # print(instruction >> 5 & 0b1)
        
        # handle_alu = instruction >> 5 & 0b1
        # if handle_alu == 1:
        #     pass
        #     # self.alu()
        # elif handle_alu ==0:
        #     pass

        # print(instruction & 5)
       
