import sys
import csv

class Interpreter:
    def __init__(self):
        self.memory = [0] * 65536  # объединённая память команд и данных
        self.stack = []
        self.ip = 0

    def load_program(self, program_file):
        with open(program_file, 'rb') as f:
            code = f.read()
        for i, byte in enumerate(code):
            self.memory[i] = byte
        return len(code)

    def run(self, program_length):
        while self.ip < program_length:
            opcode = self.memory[self.ip] >> 5
            if opcode == 3:  # load
                self.ip += 4
                const = self.decode_const(self.ip - 4)
                self.stack.append(const)
            elif opcode == 2:  # read
                self.ip += 1
                offset = self.memory[self.ip - 1] & 0x1F
                addr = self.stack.pop() + offset
                self.stack.append(self.memory[addr])
            elif opcode == 7:  # store
                self.ip += 4
                addr = self.decode_addr(self.ip - 4)
                val = self.stack.pop()
                self.memory[addr] = val
            elif opcode == 1:  # sqrt
                self.ip += 5
                addr, offset = self.decode_sqrt(self.ip - 5)
                val_addr = self.stack.pop() + offset
                result = int(self.memory[val_addr] ** 0.5)
                self.memory[addr] = result
            else:
                raise ValueError(f"Unknown opcode: {opcode}")

    def decode_const(self, start):
        b1 = self.memory[start] & 0x1F
        b2 = self.memory[start + 1]
        b3 = self.memory[start + 2]
        return (b1 << 16) | (b2 << 8) | b3

    def decode_addr(self, start):
        b1 = self.memory[start] & 0x1F
        b2 = self.memory[start + 1]
        b3 = self.memory[start + 2]
        return (b1 << 16) | (b2 << 8) | b3

    def decode_sqrt(self, start):
        b1 = self.memory[start] & 0x1F
        b2 = self.memory[start + 1]
        b3 = self.memory[start + 2]
        b4 = self.memory[start + 3]
        b5 = self.memory[start + 4]
        addr = (b1 << 24) | (b2 << 16) | (b3 << 8) | b4
        offset = b5
        return addr, offset

    def dump_memory(self, start, end, output_file):
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['address', 'value'])
            for addr in range(start, end + 1):
                writer.writerow([addr, self.memory[addr]])

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python interpreter.py <program.bin> <dump.csv> <start> <end>")
        sys.exit(1)
    program_file = sys.argv[1]
    dump_file = sys.argv[2]
    start = int(sys.argv[3])
    end = int(sys.argv[4])

    interpreter = Interpreter()
    length = interpreter.load_program(program_file)
    interpreter.run(length)
    interpreter.dump_memory(start, end, dump_file)
    print(f"Program executed. Memory dumped to {dump_file}")