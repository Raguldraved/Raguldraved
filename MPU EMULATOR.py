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
            'Z':0,
            'S':0,
            'P':0,
            'C':0,
            'O':0
        }

        #Setting up the MPU memory
        self.instructionMemory = [0] * 65536
        self.dataMemory = [0] * 65536

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
            'Z':0,
            'S':0,
            'P':0,
            'C':0,
            'O':0
        }
        self.instructionMemory = [0] * 65536
        self.dataMemory = [0] * 65536

    def fetch(self): #Fetches and stores instruction in the instructionRegister
        self.instructionRegister = self.instructionMemory[self.programCounter]
        self.programCounter += 1

    def decodeANDexecute(self):
        currentInstruction = self.instructionRegister #Identifier to address the instruction register
        
        if currentInstruction == 0x00: #NOPE instruction (no operation)
            pass
        
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
            hex = hex - 0x003a
            register = self.register_map[hex] 
            immediate_value = self.instructionMemory[self.programCounter]
            setattr(self,register,immediate_value)
            self.programCounter += 1
            print(f'The immediate value {value} has been moved to {self.register_map[hex]}')
        
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
            
        elif currentInstruction == 0x0049: #STA instruction (store accumulator value to the given memory address)
            high_byte = self.instructionMemory[self.programCounter + 1]
            low_byte = self.instructionMemory[self.programCounter]
            address = (high_byte << 8) | low_byte
            self.dataMemory[address] = self.A
            self.programCounter += 2


MPU = Ra8_MPU()

