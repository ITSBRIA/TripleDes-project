from Crypto.Cipher import DES
import tkinter as tk
from tkinter import Entry, Label, Button

def des_encrypt(message, key):
    message = message + b"\0" * (8 - len(message) % 8)
    cipher = DES.new(key, DES.MODE_ECB)
    ciphertext = cipher.encrypt(message)
    return ciphertext
def encrypt_message():
    message = entry_message.get().encode('utf-8')
    key =  b't\x01\x23\x45\x67\x89\xab\xcd'
    for _ in range(3):
        encrypted_data = des_encrypt(message, key)
        message = encrypted_data
    encrypted_data_hex = encrypted_data.hex()
    label_result.config(text=f"Encrypted Data (Tripple DES): {encrypted_data_hex}")
    print(encrypted_data_hex)
root = tk.Tk()
root.title("DES Encryption")
root.geometry("400x250")
root.resizable(False, True)
root.configure(bg="#F0F0F0")
label_message = Label(root, text="Enter Message:", font=("Helvetica", 12), bg="#F0F0F0")
label_message.pack(pady=10)
entry_message = Entry(root, width=30, font=("Helvetica", 12))
entry_message.pack(pady=10)
encrypt_button = Button(root, text="Encrypt", command=encrypt_message, font=("Helvetica", 12), bg="#4CAF50", fg="white", padx=10, pady=5)
encrypt_button.pack(pady=20)
label_result = Label(root, text="", font=("Helvetica", 12), bg="#F0F0F0")
label_result.pack(pady=10)
root.mainloop()
