"""CPU functionality."""

import sys,os
from pathlib import Path


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:

    def __init__(self):
        self.head = None
        self.tail = None

    def __iter__(self):
        node = self.head
        while node:
            yield node
            node = node.next


class Stack(LinkedList):

    def __init__(self):

        self.size = 0
        self.storage = LinkedList()
        # self.head = self.storage.head
        self.head = self.storage.head #(stack pointer)
        self.tail = self.storage.tail
        self.next = None
        if self.size == 0:
            self.sp = 0xF4
        else:
            self.sp = self.head
    def __len__(self):

        return self.size

    def push(self, value):
        self.value = value


        # new_node = Node(self.value)
        # new_node.next = self.head
        # self.head = new_node



        # create a node to add
        new_node = Node(value)
        # check if list is empty
        if self.head is None and self.tail is None:
          self.head = new_node
          self.tail = new_node

        else:
          # new_node should point to current head
          new_node.next = self.head
          # move head to new node
          self.head = new_node

        self.size += 1



    def pop(self):

        # # edge case - empty linked list
        # if self.head == None:
        #     return
        #
        # # Store head node
        # temp = self.head
        #
        # # If head needs to be removed
        # self.head = temp.next
        # temp = None
        #self.size -= 1

        # if list is empty, do nothing
        if not self.head:
          return None
        # if list only has one element, set head and tail to None
        if self.head.next is None:
          head_value = self.head.value
          self.head = None
          self.tail = None
          self.size -= 1
          return head_value
        # otherwise we have more elements in the list
        else:
            head_value = self.head.value
            self.head = self.head.next
            self.size = self.size - 1

            return head_value
    
        
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
        self.fl = [0] * 8              # 0 for false and 1 for true
        self.mar = self.pc
        self.reg[7] = 0xF4             # '0b11110100' or 244
        self.ram = [0] * 2048           # 256 bytes * 8 bits/byte = 2048bits
        self.running = True
        self.stack = Stack()
        # self.ccr : [0] * 8
        # self.ie = {}

    



    def __len__(self):

        return self.size

    def push(self, value):
        self.value = value


    def load(self, filename):
        """Load a program into memory."""

        address = 0



        # this does not work on Windows because of backlashes vs forward slashes.
        # program = open(f"../ls8/examples/{filename}", "r").readlines()

        # another way: using with open
        # with open(os.path.join(f'{sys.path[0]}/examples/', filename), 'r') as program:

        # New way - using pathlib (compatible with Mac, Win and Linux):

        data_folder = Path("./examples")

        filename = data_folder / filename

        program = open(filename)

        out = []
        # program =
        for i in program:
            out.append(bin(int(i[:8],2)))
        for instruction in out:

            self.ram[address] = instruction
            address += 1
        # print(out)

    def alu(self, op, reg_a = 0, reg_b = 0):
        """ALU operations."""
        #print(f'reg_a: {reg_a}')
        #print(f'reg_b: {reg_b}')
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            self.pc += 3

        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
            self.pc += 3

        elif op == "MUL":
            # print(int(self.reg[int(reg_a,2)],2), end=' ')
            # print('*', end=' ')
            # print(int(self.reg[int(reg_b,2)],2), end=" ")
            # print('=', end=" ")
            a = int(self.reg[int(reg_a,2)],2)
            b = int(self.reg[int(reg_b,2)],2)
            self.reg[int(reg_a,2)] = a * b
            # print(self.reg[int(reg_a,2)])
            # print(f'{self.reg[int(reg_a,2)]}')
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
            # print(f'reg_a:{reg_a}')
            # print(f'reg_b:{reg_b}')
            self.reg[int(reg_a,2)] = reg_b

            # print(self.reg[reg_a])
            self.pc += 3
            # print(f'LDI done')

        elif op == "PRN":
            # print(type(self.reg[int(reg_a,2)]))
            if type(self.reg[int(reg_a,2)]) == str:
                print(int(self.reg[int(reg_a,2)],2))
            else:
                print(self.reg[int(reg_a,2)])
                # print(int(self.reg[int(reg_a,2)],2))
            self.pc += 2
            # print('PRN done')

        elif op == "HLT":
            
            self.pc += 1
            # print('HLT done')
        elif op == "PUSH":
            self.stack.push(int(reg_a,2))
            self.pc += 1
        
        elif op == "POP":
            self.stack.pop(int(reg_a,2))
            self.pc += 1




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
            self.ram_read(self.pc + 2),

        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, address):
        # print(f'address: {address}')

        self.mar = address
      

        self.ir = self.ram[address]
        # print(self.ir)
       
        return self.ir

    def ram_write(self, value, address):
        self.mdr = value
        self.mar = address
        self.ram[address] = value

    def next_operation(self):
        instruction = self.ram_read(self.pc)
        self.pc += int(instruction,2) >> 5

    def run(self):
        """Run the CPU."""

        #self.trace()


        # print(self.mar)
        # print(self.ram[self.pc])
        # print(bin(int(str(self.reg[7]),10)))

        self.mdr = self.ram[self.pc]

        # binary_program = [i for i in self.ram]
        # decimal_program = [int(str(i),2) for i in self.ram]
        # print(binary_program)
        # print(decimal_program)
        # print(self.pc)

        # dont delete this one
        # print(bin(int(self.ram_read(self.pc),2)))


        while bin(int(self.ram_read(self.pc),2)) != '0b00000001':
            

            


            # print(bin(int(self.ram_read(self.pc),2) >> 5)[-1])
            if bin(int(self.ram_read(self.pc),2) >> 5)[-1] == '1':
                # print('here')
                # print(self.ram_read(self.pc))

                # if self.ram_read(self.pc) == 0b1:
                #     sys.exit(0)

                # handled by alu()

                handled_by_alu = True
                # print(f'handled by alu')

                instruction = self.ram_read(self.pc)
                operand_a = self.ram_read(self.pc+1)
                operand_b = self.ram_read(self.pc+2)
                # print(f'instruction: {bin(instruction)}')
                # print(f'instruction >> 5: {bin(instruction>>5)}')

                if instruction[-4:] == '0000':
                    op = 'ADD'
                    instruction = self.ram_read(self.pc)
                    operand_a = self.ram_read(self.pc+1)
                    operand_b = self.ram_read(self.pc+2)
                    # print(f'instruction: {bin(instruction)}')
                    # print(f'instruction >> 5: {bin(instruction>>5)}')

                    self.alu('ADD', operand_a, operand_b)
                #print('here')
                #print(instruction[-4:])
                if instruction[-4:] == '0010':

                    op = 'MUL'
                    #print('here')
                    instruction = self.ram_read(self.pc)
                    operand_a = self.ram_read(self.pc+1)
                    operand_b = self.ram_read(self.pc+2)
                    #print(f'instruction: {bin(instruction)}')
                    #print(f'instruction >> 5: {bin(instruction>>5)}')
                    self.alu('MUL', operand_a, operand_b)

                # if bin(instruction)[-4:] == '1000':
                #     op = 'AND'

                instruction = self.ram_read(self.pc)
                # type(instruction)
            if bin(int(self.ram_read(self.pc),2) >> 5)[-1] == '0':
                # not handled by alu()
                # print(instruction)
                
                handled_by_alu = False


                #print(f'not handled by alu')
                instruction = bin(int(self.ram_read(self.pc),2))
                #print(bin(int(instruction,2))[-4:])
                if bin(int(instruction,2))[-4:] == '0010':
                    op = 'LDI'
                    operand_a = self.ram_read(self.pc+1)
                    operand_b = self.ram_read(self.pc+2)

                    self.non_alu('LDI', operand_a, operand_b)


                    #print(self.reg[operand_a] == operand_b)

                # print(bin(int(self.ram_read(self.pc),2)))
                instruction = bin(int(self.ram_read(self.pc),2))
                if bin(int(instruction,2))[-4:] == '0111':
                    op = 'PRN'
                    operand_a = self.ram_read(self.pc+1)
                    self.non_alu('PRN', operand_a)
                    # print('PRN executed')


                # print(instruction)
                # print(self.ram_read(self.pc))

                instruction = bin(int(self.ram_read(self.pc),2))
                if instruction == '0b1':
                    # print(instruction)    
                    op = 'HLT'
                    operand_a = self.ram_read(self.pc+1)
                    # print('here')
                    # print(operand_a)
                    # print('here')
                    self.non_alu('HLT', operand_a)
                    # print('HLT executed')
                    

                    sys.exit()















        # print(instruction >> 5 & 0b1)
