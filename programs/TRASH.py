'''
This program is used for testing functions in MPU EMULATOR.py script before implementing.
'''
class bitwise:
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
    

bitwise = bitwise()

val = bitwise.Logic_leftRotate(0b10010011)
print('leftRotate:', f'{val:08b}')
val = bitwise.Logic_rightRotate(0b10010011)
print('rightRotate:', f'{val:08b}')
val = bitwise.Logic_rightShift(0b10010011)
print('rightShift:', f'{val:08b}')
val = bitwise.Logic_leftShift(0b10010011)
print('leftShift:', f'{val:08b}')
print()
val = bitwise.Arithmetic_leftRotate(0b10010011)
print('aleftRotate:', f'{val:08b}')
val = bitwise.Arithmetic_rightRotate(0b10010011)
print('arightRotate:', f'{val:08b}')
val = bitwise.Arithmetic_rightShift(0b10010011)
print('arightShift:', f'{val:08b}')
val = bitwise.Arithmetic_leftShift(0b10010011)
print('aleftShift:', f'{val:08b}')

