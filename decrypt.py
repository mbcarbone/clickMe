import hashlib
from Crypto.Cipher import AES

# Define the filename for our reliably extracted payload.
PAYLOAD_FILENAME = "network_payload.bin"
#PAYLOAD_FILENAME = "payload.bin"
#PAYLOAD_FILENAME = "ciphertext.bin"

# 1. Define the key material.
key_string = "hackingisnotacrime" # This was in the strings output of the exe.

# 2. Calculate the SHA256 hash to get the actual 32-byte encryption key.
sha256 = hashlib.sha256()
sha256.update(key_string.encode('utf-8'))
decryption_key = sha256.digest()

# 3. Read the entire network payload (header + ciphertext).
try:
    with open(PAYLOAD_FILENAME, 'rb') as f:
        network_payload = f.read()
except FileNotFoundError:
    print(f"Error: '{PAYLOAD_FILENAME}' not found. Make sure you saved it from Wireshark.")
    exit()

# 4. Separate the 4-byte header from the actual ciphertext.
header = network_payload[:4]
ciphertext = network_payload[4:]

print(f"Read {len(network_payload)} bytes from {PAYLOAD_FILENAME}.")
print(f"Header is {len(header)} bytes, Ciphertext is {len(ciphertext)} bytes.")
if len(ciphertext) % 16 != 0:
    print("\nError: Ciphertext size is still not a multiple of 16. Please double-check the export from Wireshark.")
    exit()

# 5. Decrypt the correctly sized ciphertext.
cipher = AES.new(decryption_key, AES.MODE_ECB) #
decrypted_plaintext = cipher.decrypt(ciphertext)

# Save the decrypted binary data to a new file
with open('decrypted_library.dll', 'wb') as f:
    f.write(decrypted_plaintext)

print("\n--- Decryption Successful ---")
print("The decrypted data appears to be a Windows DLL.")
print("It has been saved as 'decrypted_library.dll'.")

# 6. Print the result.
try:
    # Use unpad to correctly remove PKCS#7 padding before decoding
    from Crypto.Util.Padding import unpad
    unpadded_data = unpad(decrypted_plaintext, AES.block_size)
    flag = unpadded_data.decode('utf-8').rstrip()
    
    print("\n--- Decryption Successful ---")
    print("\nHere is the flag:\n")
    print(flag)
except (ValueError, UnicodeDecodeError) as e:
    print("\n--- Decryption Succeeded but Unpadding/Decoding Failed ---")
    print(f"Error: {e}")
    print("This might happen if the key is wrong. Here is the raw decrypted data:")
    print(decrypted_plaintext)
