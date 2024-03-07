from Crypto.Random import get_random_bytes

# Generate a 24-byte key for Triple DES
key_24_bytes = get_random_bytes(24)

# Print the key in hexadecimal format
key_hex = key_24_bytes.hex()
print(f"Generated 24-byte key (hexadecimal): {key_hex}")

# Alternatively, you can print the key as bytes
print(f"Generated 24-byte key (bytes): {key_24_bytes}")
