class MemoryBus:
    def __init__(self):
        self.memory = {}

    def initialize_memory(self, data):
        print("[MemoryBus] Initializing memory...")
        for line in data:
            if ',' in line:
                addr_bin, val = line.strip().split(',')
                addr = int(addr_bin.strip(), 2)  # Interpret address as binary
                val = int(val.strip())
                self.memory[addr] = val
                print(f"  [MemoryBus] Address {addr} (bin {addr_bin}) set to {val}")


    def read(self, address):
        return self.memory.get(address, 0)

    def write(self, address, value):
        self.memory[address] = value


class Cache:
    def __init__(self):
        self.enabled = False

    def configure(self, value):
        self.enabled = bool(int(value))
        print(f"[Cache] Cache {'enabled' if self.enabled else 'disabled'}")


class CPU:
    def __init__(self, memory_bus, cache):
        self.registers = {f"R{i}": 0 for i in range(32)}
        self.pc = 0
        self.running = True
        self.instructions = []
        self.memory_bus = memory_bus
        self.cache = cache

    def load_instructions(self, instruction_lines):
        self.instructions = [line.strip().split(',') for line in instruction_lines]

    def run(self):
        print("[CPU] Starting execution...\n")
        while self.running and self.pc < len(self.instructions):
            instr = self.instructions[self.pc]
            opcode = instr[0].upper()
            print(f"[CPU] PC={self.pc} | Executing: {','.join(instr)}")

            if opcode == "CACHE":
                self.cache.configure(instr[1])

            elif opcode == "ADDI":
                dest, src, imm = instr[1], instr[2], int(instr[3])
                self.registers[dest] = self.registers[src] + imm
                print(f"  → {dest} = {self.registers[src]} + {imm} = {self.registers[dest]}")

            elif opcode == "ADD":
                dest, src1, src2 = instr[1], instr[2], instr[3]
                self.registers[dest] = self.registers[src1] + self.registers[src2]
                print(f"  → {dest} = {self.registers[src1]} + {self.registers[src2]} = {self.registers[dest]}")

            elif opcode == "J":
                target = int(instr[1])
                print(f"  → Jumping to instruction {target}")
                self.pc = target
                continue

            elif opcode == "HALT":
                print("  → HALT received. Stopping CPU.")
                self.running = False

            else:
                print(f"  !! Unknown instruction: {opcode}")

            self.pc += 1


class BusController:
    def __init__(self, instruction_file, memory_file=None):
        self.instruction_file = instruction_file
        self.memory_file = memory_file
        self.memory_bus = MemoryBus()
        self.cache = Cache()
        self.cpu = CPU(self.memory_bus, self.cache)

    def load_files(self):
        print("[BusController] Loading instruction and memory files...")
        with open(self.instruction_file, 'r') as f:
            instructions = [line for line in f if line.strip()]

        memory_data = []
        if self.memory_file:
            with open(self.memory_file, 'r') as f:
                memory_data = [line for line in f if line.strip()]

        return instructions, memory_data

    def run(self):
        instructions, memory_data = self.load_files()
        self.memory_bus.initialize_memory(memory_data)
        self.cpu.load_instructions(instructions)
        self.cpu.run()



controller = BusController("instruction_input.txt", "data_input.txt")
controller.run()
