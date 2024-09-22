class Ra8_MPU:
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
        self.programCounter = 0x000

        #Flags register
        self.flags = {
            'Z':False,#zero flag
            'S':False,#sign flag
            'P':False,#parity flag
            'C':False,#carry flag
            'O':False #overflow flag
        }

        #Setting up the MPU memory
        self.instructionMemory = [0] * 65536
        self.dataMemory = [0] * 65536

        self._halted = False
        self._handleflags = False

    def setFlag(self,flag,value:bool):
        if flag in self.flags:
            self.flags[flag] = value
    
    def getFlag(self,flag): #If the given flag is in the flags register it returns its value
        return self.flags.get(flag,0) #if the flag is not in the register then a default value of 0 will be returned 
    
    def reset(self): #Resets all the register and memory data to its inital values
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
            'O':False
        }

        self.instructionMemory = [0] * 65536
        self.dataMemory = [0] * 65536

        self._halted = False
        self._handleflags = False

    ######FETCH,DECODEANDEXECUTE and HANDLECARRY FUNCTIONS MUST BE PLACED IN A WHILE LOOP WITH CORRECT ORDER########
    ''' 
    Todo:
    1: Adding method to set flags at the end of every operation

        Note:_handleflags must be set to false when fetching instructions
        and must be set to true when necessay in the decodeandexecute function
    '''   

    def fetch(self): #Fetches and stores instruction in the instructionRegister
        self.instructionRegister = self.instructionMemory[self.programCounter]
        self.programCounter += 1

    def handleFlag():
        pass

    def decodeANDexecute(self):
        currentInstruction = self.instructionRegister #Identifier to address the instruction register
        
        if currentInstruction == 0x00: #NOPE instruction (no operation)
            pass

        elif currentInstruction == 0x0001: #HLT instruction (halt)
            self.halted = True 
        
        elif currentInstruction in range(0x0002,0x003a): #MOV instruction
            hex = currentInstruction
            hex = hex - 0x02    #expression to decode the registers from the hex instruction
            Xreg = hex // 7
            Yreg = hex % 7
            if Yreg >= Xreg:
                Yreg += 1
            Value_to_be_moved = getattr(self,(self.register_map[Yreg]))#gets the value from the source register 
            setattr(self,(self.register_map[Xreg]),Value_to_be_moved)#load the value to the destination register
            #print(f'The value moved from {self.register_map[Yreg]} to {self.register_map[Xreg]} is {getattr(self,(self.register_map[Xreg]))}')
        
        elif currentInstruction in range(0x003a,0x0041): #MVI instruction
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

        elif currentInstruction in range(0x0043,0x0047): #STR instruction (store B,C,D,E register values to memory)
            regindex = currentInstruction - 0x0042
            high_byte = self.instructionMemory[self.programCounter + 1]
            low_byte = self.isntructionMemory[self.programCounter]
            address = (high_byte << 8) | low_byte      
            self.dataMemory[address] = getattr(self,(self.register_map[regindex]))
            self.programCounter +=2

        elif currentInstruction == 0x0049: #STA instruction (store accumulator value to the given memory address)
            high_byte = self.instructionMemory[self.programCounter + 1]
            low_byte = self.instructionMemory[self.programCounter]
            address = (high_byte << 8) | low_byte
            self.dataMemory[address] = self.A
            self.programCounter += 2
        
        elif currentInstruction in range(0x005c,0x0060): #ADD instruction
            regindex = currentInstruction - 0x005b
            regValue = getattr(self,(self.register_map[regindex]))
            accumultor = self.A
            accumulator += regValue

        elif currentInstruction == 0x0060: #ADI instructions (Add immediate value to the accumulator)
            accumulator = self.A
            value = self.instructionMemory[self.programCounter]
            accumulator  += value
            self.programCounter += 1

        elif currentInstruction in range(0x0061,0x0065): #SUB instruction
            regindex = currentInstruction - 0x0060
            regValue = getattr(self,(self.register_map[regindex]))
            accumultor = self.A
            accumulator -= regValue

        elif currentInstruction == 0x0065: #SUI instructions (Sub immediate value to the accumulator)
            accumulator = self.A
            value = self.instructionMemory[self.programCounter]
            accumulator -= value
            self.programCounter += 1

        elif currentInstruction in range(0x0066,0x006a): #MUL instruction
            regindex = currentInstruction - 0x0065
            regValue = getattr(self,(self.register_map[regindex]))
            accumultor = self.A
            accumulator = accumulator * regValue

        elif currentInstruction == 0x006a: #MUI instructions (Multiply immediate value to the accumulator)
            accumulator = self.A
            value = self.instructionMemory[self.programCounter]
            accumulator = accumulator * value
            self.programCounter += 1 

        elif currentInstruction in range(0x006b,0x006f): #DIV instruction
            regindex = currentInstruction - 0x005a
            regValue = getattr(self,(self.register_map[regindex]))
            accumultor = self.A
            accumulator = accumulator // regValue

        elif currentInstruction == 0x006f: #DII instructions (Divide immediate value to the accumulator)
            accumulator = self.A
            value = self.instructionMemory[self.programCounter]
            accumulator = accumulator // value
            self.programCounter += 1 
        
        elif currentInstruction == 0x0084: #CMC instruction (Complement the carry flag)
            carry_flag = self.flags['C'] 
            carry_flag = not carry_flag 

        elif currentInstruction == 0x0085: #STC instruction (Sets the carry flag to 1)
            self.setFlag('C',True)

        elif currentInstruction == 0x0086: #CLC instruction (Resets the carry flag to 0)
            self.setFlag('C',False)

        elif currentInstruction == 0x0087: #CMA instruction (Complements accumulator value withour changing the flags)          
            accumulator = self.A
            accumulator = not accumulator

        elif currentInstruction in range(0x0070,0x0074): #AND instruction
            regindex = currentInstruction - 0x006F
            regValue = getattr(self,(self.register_map[regindex]))
            accumultor = self.A
            accumulator = accumulator & regValue

        elif currentInstruction == 0x0074: #ANI instructions (logical AND operation on the Immediate value to the accumulator)
            accumulator = self.A
            value = self.instructionMemory[self.programCounter]
            accumulator = accumulator & value
            self.programCounter += 1

        elif currentInstruction in range(0x0075,0x0079): #OR instruction
            regindex = currentInstruction - 0x0074
            regValue = getattr(self,(self.register_map[regindex]))
            accumultor = self.A
            accumulator = accumulator | regValue

        elif currentInstruction == 0x0079: #ORI instructions (logical OR operation on the immediate value to the accumulator)
            accumulator = self.A
            value = self.instructionMemory[self.programCounter]
            accumulator = accumulator | value
            self.programCounter += 1

        elif currentInstruction in range(0x007A,0x007E): #XOR instruction
            regindex = currentInstruction - 0x0079
            regValue = getattr(self,(self.register_map[regindex]))
            accumultor = self.A
            accumulator = accumulator ^ regValue

        elif currentInstruction == 0x007E: #XRI instructions (logical XOR operation on the immediate value to the accumulator)
            accumulator = self.A
            value = self.instructionMemory[self.programCounter]
            accumulator = accumulator ^ value
            self.programCounter += 1

        elif currentInstruction in range(0x0088,0x0091): #Unconditional and Conditional jump instructions
            Type = currentInstruction - 0x0087
            match Type:
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
                    if self.flags['Z'] == True:
                        high_byte = self.instructionMemory[self.programCounter + 1]
                        low_byte = self.instructionMemory[self.programCounter]
                        address = (high_byte << 8) | low_byte
                        self.programCounter = address
                case 5:
                    if self.flags['Z'] == False:
                        high_byte = self.instructionMemory[self.programCounter + 1]
                        low_byte = self.instructionMemory[self.programCounter]
                        address = (high_byte << 8) | low_byte
                        self.programCounter = address
                case 6:
                    if self.flags['S'] == False:
                        high_byte = self.instructionMemory[self.programCounter + 1]
                        low_byte = self.instructionMemory[self.programCounter]
                        address = (high_byte << 8) | low_byte
                        self.programCounter = address
                case 7:
                    if self.flags['S'] == True:
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
                case 9:
                    if self.flags['P'] == False: #JO instructions (jump if odd_)
                        high_byte = self.instructionMemory[self.programCounter + 1]
                        low_byte = self.instructionMemory[self.programCounter]
                        address = (high_byte << 8) | low_byte
                        self.programCounter = address

MPU = Ra8_MPU()