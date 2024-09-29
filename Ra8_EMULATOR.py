class Ra8_MPU():
    def __init__(self) -> None: 

        #Accumulator and other 8 bit general purpose registers
        self.A = 0 
        self.B = 0
        self.C = 0
        self.D = 0
        self.E = 0
        self.H = 0
        self.L = 0
        self.M = 0
        self.instructionRegister = 0x00

        self.register_map = {
            0:'A',
            1:'B',
            2:'C',
            3:'D',
            4:'E',
            5:'H',
            6:'L',
            7:'M',
            8:'instructionRegister'
        }

        #Special 16 bit registers that hold the addresses to the memory
        self.stackPointer = 0xFFFF
        self.programCounter = 0x0000

        #Flags register
        self.flags = {
            'Z':False,#zero flag
            'S':False,#sign flag
            'P':False,#parity flag
            'C':False,#carry flag
        }

        #Setting up the MPU memory
        self.instructionMemory = [0] * 65536
        self.dataMemory = [0] * 65536

        #boolean variables
        self._halted = False
        self._handleflags = False

        #Setting up objects
        self.stack = Stack(self.dataMemory,self.stackPointer)
        self.bitwise = bitwise()

    def setFlag(self,flag,value:bool):
        if flag in self.flags:
            self.flags[flag] = value
    
    def resetFlag(self):
        self.flags = {
            'Z':False,
            'S':False,
            'P':False,
            'C':False,
        }

    def masterReset(self): #Resets all the registers and memory data to its inital values
        self.A = 0
        self.B = 0
        self.C = 0
        self.D = 0
        self.E = 0
        self.H = 0
        self.L = 0
        self.M = 0
        self.instructionRegister = 0x00
        self.programCounter = 0x0000
        self.stackPointer = 0xffff

        self.flags = {
            'Z':False,
            'S':False,
            'P':False,
            'C':False,
        }

        self.instructionMemory = [0] * 65536
        self.dataMemory = [0] * 65536

        self._halted = False
        self._handleflags = False

        self._halted = False
        self._handleflags = False

    ######FETCH,DECODEANDEXECUTE FUNCTIONS MUST BE PLACED IN A WHILE LOOP WITH CORRECT ORDER########
    '''  
    Todo:
    1: Check if every instructions , handling porgramCounter values and flags are set properly
    2. Find a way to handle 16bit data and addresses
    '''   

    def fetch(self): #Fetches and stores instruction in the instructionRegister
        self.instructionRegister = self.instructionMemory[self.programCounter]
        self.programCounter += 1

    def decodeANDexecute(self):
        currentInstruction = self.instructionRegister #Identifier to address the instruction register
        
        if currentInstruction == 0x00: #NOPE instruction (no operation)
            pass

        elif currentInstruction == 0x0001: #HLT instruction (halt)
            self._halted = True 
        
        elif currentInstruction in range(0x0002,0x003a): #MOV instructions
            hex1 = currentInstruction
            hex1 = hex1 - 0x02    #expression to decode the registers from the hex instruction
            Xreg = hex1 // 7
            Yreg = hex1 % 7
            if Yreg >= Xreg:
                Yreg += 1
            Value_to_be_moved = getattr(self,(self.register_map[Yreg]))#gets the value from the source register 
            setattr(self,(self.register_map[Xreg]),Value_to_be_moved)#load the value to the destination register
            #print(f'The value moved from {self.register_map[Yreg]} to {self.register_map[Xreg]} is {getattr(self,(self.register_map[Xreg]))}')
        
        elif currentInstruction in range(0x003a,0x0041): #MVI instructions
            hex = currentInstruction - 0x0039
            register = self.register_map[hex] 
            immediate_value = self.instructionMemory[self.programCounter]
            setattr(self,register,immediate_value)
            self.programCounter += 1
            #print(f'The immediate value {immediate_value} has been moved to {self.register_map[hex]}')
        
        elif currentInstruction == 0x0041: #LDA instruction (load accumulator from memory)
            high_byte = self.instructionMemory[self.programCounter + 1]
            low_byte = self.instructionMemory[self.programCounter]
            address = (high_byte << 8) | low_byte
            self.A = self.dataMemory[address]
            self.programCounter += 2

        elif currentInstruction == 0x0042: #LDI instruction (load accumulator with immediate value)
            data = self.instructionMemory[self.programCounter]
            self.A = data
            self.programCounter += 1

        elif currentInstruction in range(0x0043,0x0047): #STR instructions (store B,C,D,E register values to memory)
            regindex = currentInstruction - 0x0042
            high_byte = self.instructionMemory[self.programCounter + 1]
            low_byte = self.isntructionMemory[self.programCounter]
            address = (high_byte << 8) | low_byte      
            self.dataMemory[address] = getattr(self,(self.register_map[regindex]))
            self.programCounter +=2

        elif currentInstruction == 0x0047: #STA instruction (store accumulator value to the given memory address)
            high_byte = self.instructionMemory[self.programCounter + 1]
            low_byte = self.instructionMemory[self.programCounter]
            address = (high_byte << 8) | low_byte
            self.dataMemory[address] = self.A
            self.programCounter += 2
        
        elif currentInstruction in range(0x005a,0x005e): #ADD instructions
            regindex = currentInstruction - 0x0059
            regValue = getattr(self,(self.register_map[regindex]))
            self.A = self.A + regValue
            self.handleFlag(self.A)

        elif currentInstruction == 0x005e: #ADI instruction (Add immediate value to the accumulator)
            value = self.instructionMemory[self.programCounter]
            self.A  += value
            self.programCounter += 1
            self.handleFlag(self.A)

        elif currentInstruction in range(0x005f,0x0063): #SUB instructions
            regindex = currentInstruction - 0x005e
            regValue = getattr(self,(self.register_map[regindex]))
            self.A -= regValue
            self.handleFlag(self.A)

        elif currentInstruction == 0x0063: #SUI instruction (Sub immediate value to the accumulator)
            value = self.instructionMemory[self.programCounter]
            self.A -= value
            self.programCounter += 1
            self.handleFlag(self.A)

        elif currentInstruction in range(0x0064,0x0068): #MUL instructions
            regindex = currentInstruction - 0x0063
            regValue = getattr(self,(self.register_map[regindex]))
            self.A = self.A * regValue
            self.handleFlag(self.A)

        elif currentInstruction == 0x0068: #MUI instruction (Multiply immediate value to the accumulator)
            value = self.instructionMemory[self.programCounter]
            self.A = self.A * value
            self.programCounter += 1 
            self.handleFlag(self.A)

        elif currentInstruction in range(0x0069,0x006d): #DIV instructions
            try:
                regindex = currentInstruction - 0x0068
                regValue = getattr(self,(self.register_map[regindex]))
                self.A = self.A // regValue
                self.handleFlag(self.A)
            except ZeroDivisionError:
                self.A = 0
                self.handleFlag(self.A)

        elif currentInstruction == 0x006d: #DII instruction (Divide immediate value to the accumulator)
            try:    
                value = self.instructionMemory[self.programCounter]
                self.A = self.A // value
                self.programCounter += 1 
                self.handleFlag(self.A)
            except ZeroDivisionError:
                self.A = 0 
                self.handleFlag(self.A)

        elif currentInstruction == 0x0082: #CMC instruction (Complement the carry flag)
            carry_flag = self.flags['C'] 
            carry_flag = not carry_flag 

        elif currentInstruction == 0x0083: #STC instruction (Sets the carry flag to 1)
            self.setFlag('C',True)

        elif currentInstruction == 0x0084: #CLC instruction (Resets the carry flag to 0)
            self.setFlag('C',False)

        elif currentInstruction == 0x0085: #CMA instruction (Complements self.A value withour changing the flags)          
            self.A = not self.A

        elif currentInstruction in range(0x006e,0x0072): #AND instructions
            regindex = currentInstruction - 0x006d
            regValue = getattr(self,(self.register_map[regindex]))
            self.A = self.A & regValue

        elif currentInstruction == 0x0072: #ANI instruction (logical AND operation on the Immediate value to the self.A)
            value = self.instructionMemory[self.programCounter]
            self.A = self.A & value
            self.programCounter += 1

        elif currentInstruction in range(0x0073,0x0077): #OR instructions
            regindex = currentInstruction - 0x0072
            regValue = getattr(self,(self.register_map[regindex]))
            self.A = self.A | regValue

        elif currentInstruction == 0x0077: #ORI instruction (logical OR operation on the immediate value to the self.A)
            value = self.instructionMemory[self.programCounter]
            self.A = self.A | value
            self.programCounter += 1

        elif currentInstruction in range(0x0078,0x007c): #XOR instructions
            regindex = currentInstruction - 0x0077
            regValue = getattr(self,(self.register_map[regindex]))
            self.A = self.A ^ regValue

        elif currentInstruction == 0x007c: #XRI instruction (logical XOR operation on the immediate value to the self.A)
            value = self.instructionMemory[self.programCounter]
            self.A = self.A ^ value
            self.programCounter += 1

        elif currentInstruction in range(0x0048,0X004d): #PUSH instructions
            regindex = currentInstruction - 0x0048
            regValue = getattr(self,(self.register_map[regindex]))
            self.stack.Push(regValue)
            self.programCounter += 1

        elif currentInstruction in range(0x004d,0x052): #POP instructions
            regindex = currentInstruction = 0x0050
            register = self.register_map[regindex]
            data = self.stack.Pop()
            setattr(self,register,data)
            self.programCounter += 1
                   
        elif currentInstruction in range(0x0086,0x008e): #Unconditional and Conditional jump instructions
            Type = currentInstruction - 0x0085
            match (Type):
                case 1: #JMP instruction (Unconditional jump to the specified instruction memory address)
                    high_byte = self.instructionMemory[self.programCounter + 1]
                    low_byte = self.instructionMemory[self.programCounter]
                    address = (high_byte << 8) | low_byte
                    self.programCounter = address
                case 2: 
                    if self.flags['C'] == True: #JC instruction (jump if carry)
                        high_byte = self.instructionMemory[self.programCounter + 1]
                        low_byte = self.instructionMemory[self.programCounter]
                        address = (high_byte << 8) | low_byte
                        self.programCounter = address
                case 3:
                    if self.flags['C'] == False: #JNC instruction (jump if carry)
                        high_byte = self.instructionMemory[self.programCounter + 1]
                        low_byte = self.instructionMemory[self.programCounter]
                        address = (high_byte << 8) | low_byte
                        self.programCounter = address
                case 4:
                    if self.flags['Z'] == True: #JZ instruction
                        high_byte = self.instructionMemory[self.programCounter + 1]
                        low_byte = self.instructionMemory[self.programCounter]
                        address = (high_byte << 8) | low_byte
                        self.programCounter = address
                case 5:
                    if self.flags['Z'] == False: #JNZ instruction
                        high_byte = self.instructionMemory[self.programCounter + 1]
                        low_byte = self.instructionMemory[self.programCounter]
                        address = (high_byte << 8) | low_byte
                        self.programCounter = address
                case 6:
                    if self.flags['S'] == False: #JP instruction
                        high_byte = self.instructionMemory[self.programCounter + 1]
                        low_byte = self.instructionMemory[self.programCounter]
                        address = (high_byte << 8) | low_byte
                        self.programCounter = address
                case 7:
                    if self.flags['S'] == True: #JM instruction 
                        high_byte = self.instructionMemory[self.programCounter + 1]
                        low_byte = self.instructionMemory[self.programCounter]
                        address = (high_byte << 8) | low_byte
                        self.programCounter = address
                case 8:
                    if self.flags['P'] == True: #JE instructipm (jump if even)
                        high_byte = self.instructionMemory[self.programCounter + 1]
                        low_byte = self.instructionMemory[self.programCounter]
                        address = (high_byte << 8) | low_byte
                        self.programCounter = address

        elif currentInstruction in range(0x008e,0x0093): #Conditional and Unconditional call subroutine instructions
            Type = currentInstruction - 0x008d
            inst_highBYTE = (currentInstruction >> 8) & 0x00ff
            inst_lowBYTE = (currentInstruction & 0xff)
            self.stack.Push(inst_highBYTE)
            self.stack.Push(inst_lowBYTE)
            match (Type):
                case 1:
                    high_byte = self.instructionMemory[self.programCounter + 1]
                    low_byte = self.instructionMemory[self.programCounter]
                    address = (high_byte << 8) | low_byte
                    self.programCounter = address
                case 2: 
                    if self.flags['C'] == True: #CC instruction 
                        high_byte = self.instructionMemory[self.programCounter + 1]
                        low_byte = self.instructionMemory[self.programCounter]
                        address = (high_byte << 8) | low_byte
                        self.programCounter = address
                case 3:
                    if self.flags['C'] == False: #CNC instruction 
                        high_byte = self.instructionMemory[self.programCounter + 1]
                        low_byte = self.instructionMemory[self.programCounter]
                        address = (high_byte << 8) | low_byte
                        self.programCounter = address
                case 4:
                    if self.flags['Z'] == True: #CZ instruction
                        high_byte = self.instructionMemory[self.programCounter + 1]
                        low_byte = self.instructionMemory[self.programCounter]
                        address = (high_byte << 8) | low_byte
                        self.programCounter = address
                case 5:
                    if self.flags['Z'] == False: #CNZ instruction
                        high_byte = self.instructionMemory[self.programCounter + 1]
                        low_byte = self.instructionMemory[self.programCounter]
                        address = (high_byte << 8) | low_byte
                        self.programCounter = address

        elif currentInstruction in range(0x0093,0x0098): #Conditional and Unconditional return from subroutine instructions
            low_byte = self.stack.Pop()
            high_byte = self.stack.Pop()
            returnAddress = address = (high_byte << 8) | low_byte
            Type = currentInstruction - 0x0092
            match (Type):
                case 1: #Unconditional RET instructions
                    self.programcounter = returnAddress
                case 2: 
                    if self.flags['C'] == True: #RC instruction 
                        self.programcounter = returnAddress
                case 3:
                    if self.flags['C'] == False: #RNC instruction 
                        self.programcounter = returnAddress
                case 4:
                    if self.flags['Z'] == True: #RZ instruction
                        self.programcounter = returnAddress
                case 5:
                    if self.flags['Z'] == False: #RNZ instructioN
                        self.programcounter = returnAddress

        elif currentInstruction == 0x0098: #INC instruction
            self.A += 1

        elif currentInstruction == 0x0099: #DCR instruction
            self.A -= 1

        elif currentInstruction in range(0x0052,0x005a): #Bitwise Rotate and Shift instructions          
            Type = currentInstruction - 0x0051
            match (Type):
                case 1:#RS instructions
                    self.bitwise.Logic_rightShift(self.A) 
                case 2:#RSI instructions
                    self.bitwise.Arithmetic_rightShift(self.A) 
                case 3:#LS instructions
                    self.bitwise.Logic_leftShift(self.A) 
                case 4:#LSI instructions
                    self.bitwise.Arithmetic_leftShift(self.A) 
                case 5:#RL instructions
                    self.bitwise.Logic_leftRotate(self.A) 
                case 6:#RLI instructions
                    self.bitwise.Arithmetic_leftRotate(self.A)  
                case 7:#RR instructions
                    self.bitwise.Logic_rightRotate(self.A)  
                case 8:#RRI instructions
                    self.bitwise.Arithmetic_rightRotate(self.A)
            self.programCounter +=1  

        elif currentInstruction in range(0x007d,0x0081): #CMP instructions
            regindex = currentInstruction - 0xd007e
            regValue = getattr(self,(self.register_map[regindex]))
            temp = self.A - regValue
            self.handleFlag(temp)

        elif currentInstruction == 0x0081: #CMI instruction
            value = self.dataMemory[self.programCounter]
            temp = self.A - regValue
            self.handleFlag(temp)
            programCounter += 1

    def handleFlag(self,target): #Takes a value and sets appropriate flags
        self.resetFlag()
        if target >= 256:
            self.setFlag('C',True)
        else:
            self.setFlag('C',False)
        if target == 0:
            self.setFlag('Z',True)
        else:
            self.setFlag('Z',False)
        if target < 0:
            self.setFlag('S',True)
        else:
            self.setFlag('S',False)
        if target % 2:
            self.setFlag('P',False)
        else:
            self.setFlag('P',True)

    def run(self,debug = False):
        cycle = 0
        while 1:
            if self._halted:
                break
            else:
                if debug:
                    print(f'programCounter: {hex(self.programCounter)}')

                self.fetch()
                self.decodeANDexecute()

                if debug:
                    cycle += 1
                    print(f'currentCycle: {cycle}')
                    print(f'current Instruction: {hex(self.instructionRegister)}')
                    print('----------------------------------------------------------')
                    print(f'Flags:| {self.flags}')
                    print(f'Register A: {self.A}')
                    print(f'Register B: {self.B}')
                    print(f'Register C: {self.C}')
                    print(f'Register D: {self.D}')
                    print(f'Register E: {self.E}')
                    print(f'Register H: {self.H}')
                    print(f'Register L: {self.L}')
                    print(f'Register M: {self.M}')
                    print(f'Halted?: {self._halted}')
                    print(f'programCounter after execution: {hex(self.programCounter)}')
                    print(f'stackPointer: {hex(self.stackPointer)}')
                    print(f'stackTop: {hex(self.stack.topElement(),)}') 
                    print(f'stackPreviousElement: {hex(self.stack.previousElement())}')           
                    print('___________________________________________________________')

class Stack: #To perform stack operations
    def __init__(self,dta,sp) -> None:

        self.dataMemory = dta
        self.stackPointer = sp
        
    def Push(self,data):
        self.dataMemory[self.stackPointer] = data
        self.stackPointer -= 1

    def Pop(self):
        self.stackPointer += 1
        data = self.dataMemory[self.stackPointer]
        self.dataMemory[self.stackPointer] = 0x0000
        #print(data) #comment this line when not needed
        return data

    def topElement(self):
        if self.stackPointer < 0xffff:
            data = self.dataMemory[self.stackPointer + 1]
            #print(data) #comment this line when not needed
            return data
        else:
            data = 0x0000
            #print(data) #comment this line when not needed
            return data 
    
    def previousElement(self):
        if self.stackPointer < 0xffff:
            data = self.dataMemory[self.stackPointer + 2]
            #print(data) #comment this line when not needed
            return data
        else:
            data = 0x0000
            #print(data) #comment this line when not needed
            return data 

class bitwise: #To perform bitwise operations
    def Logic_rightShift(self,value:int):
        val = (value >> 1) & 0xff
        return val
    
    def Logic_leftShift(self,value:int):
        val = (value << 1) & 0xff
        return val 
    
    def Logic_rightRotate(self,value:int):
        val = ((value >> 1)|(value << 7)) & 0xff
        return  val
    
    def Logic_leftRotate(self,value:int):
        val = ((value << 1)|(value >>7)) & 0xff
        return val

    def Arithmetic_rightShift(self,value:int):
        msb = value & 0x80
        lower7bits = value & 0x7f
        val = (lower7bits >> 1) & 0x7f
        result = msb | val
        return result

    def Arithmetic_leftShift(self,value:int):
        msb = value & 0x80
        lower7bits = value & 0x7f
        val = (lower7bits << 1) & 0x7f
        result = msb | val
        return result
    
    def Arithmetic_rightRotate(self,value:int):
        msb = value & 0x80
        lower7bits = value & 0x7f
        val = ((lower7bits >> 1)|(lower7bits << 6)) & 0x7f
        result = msb | val
        return result
    
    def Arithmetic_leftRotate(self,value:int):
        msb = value & 0x80
        lower7bits = value & 0x7f
        val = ((lower7bits << 1)|(lower7bits >> 6)) & 0x7f
        result = msb | val
        return result

