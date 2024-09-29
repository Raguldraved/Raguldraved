from Ra8_EMULATOR import *

emulator = Ra8_MPU()
instructionMemory = emulator.instructionMemory
dataMemory = emulator.dataMemory

machinecode_filename = 'machineCodes/factorial.txt'
lines = open(machinecode_filename).read().splitlines()

dataMemory[0x0069] = 5
dataMemory[0x0096] = 0

for index,value in enumerate(lines):
    instructionMemory[index] = int(value,16)
emulator.run(debug=True)

print('OUTPUT:')
print(dataMemory[0x0096])
print('___________________________________________________________')
