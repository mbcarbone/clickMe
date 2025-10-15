import os

def generate_flag():
    """
    Emulates the virtual machine from decrypted_library.dll to generate the flag
    from the 'anonymous' bytecode file.
    """
    # Initialize the memory buffers used by the VM. They are 256 bytes long.
    data1 = bytearray(256)
    data2 = bytearray(256)
    data3 = bytearray(256)
    flag_buffer = bytearray(256)

    # Securely read the bytecode file.
    bytecode_file = 'anonymous'
    if not os.path.exists(bytecode_file):
        print(f"Error: Bytecode file '{bytecode_file}' not found.")
        return

    with open(bytecode_file, 'rb') as f:
        bytecode = f.read()

    # Initialize the instruction pointer (ip) to the start of the bytecode.
    ip = 0
    bytecode_len = len(bytecode)

    # Loop through the bytecode and execute the VM instructions.
    while ip < bytecode_len:
        opcode = bytecode[ip]

        match opcode:
            case 1:  # Store value in data1
                if ip + 2 < bytecode_len:
                    index, value = bytecode[ip + 1], bytecode[ip + 2]
                    data1[index] = value
                ip += 3
            case 2:  # Store value in data2
                if ip + 2 < bytecode_len:
                    index, value = bytecode[ip + 1], bytecode[ip + 2]
                    data2[index] = value
                ip += 3
            case 3:  # Add or Subtract based on index parity
                if ip + 2 < bytecode_len:
                    index, value = bytecode[ip + 1], bytecode[ip + 2]
                    if (index % 2) == 0:  # Even index
                        result = data1[index] + value
                    else:  # Odd index
                        result = data1[index] - value
                    data3[index] = result & 0xFF # Ensure result is a single byte
                ip += 3
            case 4:  # XOR operation to build the flag
                if ip + 1 < bytecode_len:
                    index = bytecode[ip + 1]
                    # This is the core XOR logic from the disassembly
                    xor_val = data2[index & 3]
                    flag_buffer[index] = data3[index] ^ xor_val
                ip += 2
            case 5:  # Halt and finish
                print("Halt instruction (5) reached. Flag generation complete.")
                break
            case _:  # Unknown opcode
                print(f"Unknown opcode {opcode} at position {ip}. Halting.")
                break
    
    # Decode the final flag buffer into a readable string.
    # We strip any trailing null bytes that were not overwritten.
    try:
        flag = flag_buffer.decode('utf-8', errors='ignore').rstrip('\x00')
        print("\n--- Flag Generation Successful ---")
        print("\nHere is the flag:\n")
        print(flag)
    except Exception as e:
        print(f"\nCould not decode the flag buffer: {e}")


if __name__ == "__main__":
    generate_flag()

