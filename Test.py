from Ra8_EMULATOR import *

emulator = Ra8_MPU()
instructionMemory = emulator.instructionMemory
dataMemory = emulator.dataMemory

machinecode_filename = 'Additional programs/addition.txt'
lines = open(machinecode_filename).read().splitlines()

dataMemory[0x0032] = 4
dataMemory[0x0033] = 2

for index,value in enumerate(lines):
    instructionMemory[index] = int(value,16)
    index +=  1

emulator.fetch()
print(emulator.instructionRegister)
emulator.run()
print(emulator.dataMemory[0x0032])