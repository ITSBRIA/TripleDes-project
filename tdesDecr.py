from Crypto.Cipher import DES
import tkinter.messagebox as tkMessageBox
def des_decrypt(ciphertext, key):
    cipher = DES.new(key, DES.MODE_ECB)
    decrypted_message = cipher.decrypt(ciphertext)
    return decrypted_message.rstrip(b"\0")
if __name__ == "__main__":
    
    key = b't\x01\x23\x45\x67\x89\xab\xcd'
    encrypted_data = b'251b73c3699b9655b1385e54a9fc451df45cfa2086f60b41'
    for _ in range(3):
        decrypted_data = des_decrypt(encrypted_data, key)
        tkMessageBox.showinfo("Decrypted Message (3DES)", decrypted_data)
       
