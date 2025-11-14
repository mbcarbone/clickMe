# Deconstructing "nukoneZ's Ransomware" - A CTF Writeup

## This repository contains the analysis and solution for the "nukoneZ's Ransomware" reverse engineering challenge from crackmes.one.

### Challenge Overview

The challenge provides a Windows executable (Click_Me.exe) and a network capture file (RecordUser.pcapng). The goal is to reverse engineer the ransomware's behavior to recover an encrypted "flag," which is the secret key needed to prove the challenge has been solved.

The investigation revealed a multi-stage challenge involving:Network traffic analysis to extract key payloads.Static and dynamic analysis of the main executable to understand its cryptographic process.

Decryption of a hidden second-stage payload (a DLL).Reverse engineering a custom virtual machine within the DLL.Emulating the VM with the correct bytecode to generate the final flag.


* Phase 1: Initial Triage
** Network Analysis (Wireshark) **
The RecordUser.pcapng file immediately provided two critical artifacts:
1. An HTTP Download: The executable downloads a small file named anonymous. This file was extracted and later identified as bytecode for the VM.
2. A TCP C2 Stream: The executable connects to 192.168.134.132 on port 8888 and sends a payload. This payload was extracted and identified as the encrypted second-stage DLL.Static Analysis

Analyzing the strings within Click_Me.exe provided a clear roadmap
Key Material: ``` hackingisnotacrimeC2 Server: 192.168.134.132 ```
Target File: ``` C:\ProgramData\Important\user.html ```
Crypto Functions: Imports for SHA256 and EVP_aes_256_ecb confirmed the cryptographic primitives.

* Phase 2: Deconstructing the RansomwareBy tracing the code from main, we identified the core logic within the sub_001FB3 function.
1. Key Generation: The program calculates the SHA256 hash of the string hackingisnotacrime. This 32-byte hash is used as the AES key.
2. Encryption: The program encrypts the file C:\ProgramData\Important\user.html using AES-256-ECB with the generated key.
3. Exfiltration: It then connects to the C2 server and sends the encrypted file.

* Phase 3: The Twist - A Hidden DLLDecrypting the exfiltrated payload from the C2 stream revealed it was not a flag but a Windows DLL, identified by the "MZ" header. This was the second stage of the challenge.

### Key decryption logic
``` import hashlib
from Crypto.Cipher import AES

key_string = "hackingisnotacrime"
sha256 = hashlib.sha256()
sha256.update(key_string.encode('utf-8'))
decryption_key = sha256.digest()
```
### ... decryption code ...
### Output started with b'MZ...', confirming it's an executable.
* Phase 4: The Final Secret - A Custom VM
The decrypted DLL was analyzed, and its exported functions (gen_from_file, get_result_bytes) pointed to an internal function named gen.

This function was a simple, custom virtual machine that processed bytecode.

## The VM had five opcodes:
1. Store a value in memory buffer
3. Perform addition or subtraction on buffer 1 and store in buffer 
4. Perform an XOR operation between buffers 3 and 3, writing the result to the final flag buffer.
5. Halt execution.The bytecode for this VM was the anonymous file downloaded in Phase 1.

### Flag Recovery
By writing a Python script to emulate the VM and feeding it the anonymous bytecode, the final flag was generated.

## Tools Used
* [Wireshark](https://www.wireshark.org/) (Version 4.6.0) - For network packet analysis.
* [Ghidra](https://ghidra-sre.org/) (Version 11.3.2) - For static analysis and disassembly/decompilation.
* [Python 3](https://www.python.org/) (Version 3.11.2) - For scripting decryption and VM emulation.
    * `pycryptodome` library - For AES decryption.
    * `hashlib` library - For SHA256 hashing.
* [hexdump](https://github.com/util-linux/util-linux) (Version 2.38.1) - For examining binary data.
* [Google Gemini](https://gemini.google.com/) (Model Version 2.5 pro) - For math, reasoning and code.
