from Ra8_EMULATOR import *

emulator = Ra8_MPU()
instructionMemory = emulator.instructionMemory
dataMemory = emulator.dataMemory

machinecode_filename = 'Additional programs/addition.txt'
lines = open(machinecode_filename).read().splitlines()

dataMemory[0x0032] = 2
dataMemory[0x0033] = 6

for index,value in enumerate(lines):
    instructionMemory[index] = int(value,16)
    
emulator.run()
print(emulator.flags)
print(emulator.A)