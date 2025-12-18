import subprocess
import json

def test_assembler():
    print("Testing assembler...")
    program = [
        {"op": "load", "const": 8},
        {"op": "read", "offset": 25},
        {"op": "store", "addr": 218},
        {"op": "sqrt", "addr": 697, "offset": 24}
    ]
    with open('test.asm', 'w') as f:
        json.dump(program, f)

    subprocess.run(['python', 'assembler.py', 'test.asm', 'test.bin', 'true'])
    print("Assembler test completed.")

def test_interpreter():
    print("Testing interpreter...")
    subprocess.run(['python', 'interpreter.py', 'test.bin', 'dump.csv', '0', '100'])
    print("Interpreter test completed.")

if __name__ == "__main__":
    test_assembler()
    test_interpreter()