import binascii

from backend.bc_utils.crypto_hash import crypto_hash
HEX_TO_BINARY_TABLE={
'0':'0000', 
'1':'0001', 
'2':'0010',
'3':'0011',
'4': '0100',
'5': '0101', 
'6':'0110', 
'7': '0111',
'8': '1000',
'9': '1001',
'a': '1010',
'b': '1011', 
'c': '1100',
'd': '1101',
'e': '1110',
'f': '1111'}

def hex_to_binary(hex_str):
    hex_str = hex_str[2:]
    bin_str = ''

    for chr in hex_str:
        bin_str += HEX_TO_BINARY_TABLE[chr]
    
    return bin_str

def main():
    number = 105
    hexx = hex(number)
    hexx = '0x1bfd2146'
    print(hexx)
    print(hex_to_binary(hexx),'\n')
    res = "{0:08b}".format(int(hexx, 16))
    print(res)
    res = int(res,16)

    print(res)

    hex_crypto = hex_to_binary(crypto_hash('test-data'))
    print(f'binary_hash: {hex_crypto}')

if __name__ == '__main__':
    main()