'''
This program is used for testing functions in MPU EMULATOR.py script before implementing.
'''

class Stack: #testing the stack class
    def __init__(self) -> None:
        self.dataMemory = [0] * 65536
        self.stackPointer = 0xffff
        

    def _Push(self,data):
        self.dataMemory[self.stackPointer] = data
        self.stackPointer -= 1

    def _Pop(self):
        data = self.dataMemory[self.stackPointer + 1]
        self.stackPointer += 1
        print(data) #comment this line when not needed
        return data

    def _topElement(self):
        
        if self.stackPointer < 0xffff:
            data = hex(self.dataMemory[self.stackPointer + 1])
            print(data) #comment this line when not needed
            return data
        else:
            data = hex(0x0000)
            print(data) #comment this line when not needed
            return data  
        
        
stack = Stack()

stack._topElement()



