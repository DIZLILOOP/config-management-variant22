import json
import sys

class Assembler:
    def __init__(self):
        self.opcodes = {
            'load': 3,
            'read': 2,
            'store': 7,
            'sqrt': 1
        }

    def assemble(self, input_file, output_file, test_mode=False):
        with open(input_file, 'r') as f:
            program = json.load(f)

        binary_code = bytearray()
        for instr in program:
            op = instr['op']
            if op == 'load':
                const = instr['const']
                code = self.encode_load(const)
                binary_code.extend(code)
            elif op == 'read':
                offset = instr['offset']
                code = self.encode_read(offset)
                binary_code.extend(code)
            elif op == 'store':
                addr = instr['addr']
                code = self.encode_store(addr)
                binary_code.extend(code)
            elif op == 'sqrt':
                addr = instr['addr']
                offset = instr['offset']
                code = self.encode_sqrt(addr, offset)
                binary_code.extend(code)
            else:
                raise ValueError(f"Unknown opcode: {op}")

        with open(output_file, 'wb') as f:
            f.write(binary_code)

        if test_mode:
            self.print_hex(binary_code)

    def encode_load(self, const):
        # A=3, B=const (биты 3-24)
        b = const & 0x3FFFFF  # 22 бита
        byte1 = (3 << 5) | ((b >> 16) & 0x1F)
        byte2 = (b >> 8) & 0xFF
        byte3 = b & 0xFF
        return bytes([byte1, byte2, byte3, 0])

    def encode_read(self, offset):
        # A=2, B=offset (биты 3-7)
        b = offset & 0x1F
        return bytes([(2 << 5) | b])

    def encode_store(self, addr):
        # A=7, B=addr (биты 3-29)
        b = addr & 0x1FFFFFF  # 27 бит
        byte1 = (7 << 5) | ((b >> 16) & 0x1F)
        byte2 = (b >> 8) & 0xFF
        byte3 = b & 0xFF
        return bytes([byte1, byte2, byte3, 0])

    def encode_sqrt(self, addr, offset):
        # A=1, B=addr (3-29), C=offset (30-34)
        b = addr & 0x1FFFFFF
        c = offset & 0x1F
        byte1 = (1 << 5) | ((b >> 24) & 0x1F)
        byte2 = (b >> 16) & 0xFF
        byte3 = (b >> 8) & 0xFF
        byte4 = b & 0xFF
        byte5 = c
        return bytes([byte1, byte2, byte3, byte4, byte5])

    def print_hex(self, data):
        print(' '.join(f'{b:02x}' for b in data))

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python assembler.py <input.asm> <output.bin> <test_mode>")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    test_mode = sys.argv[3].lower() == 'true'
    assembler = Assembler()
    assembler.assemble(input_file, output_file, test_mode)