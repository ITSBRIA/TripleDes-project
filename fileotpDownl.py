import tkinter as tk
from tkinter import messagebox
import random
import smtplib
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import subprocess

# Placeholder values, replace them with your actual configurations
sender_email = "briankipngetichyegon@gmail.com"
sender_password = "silhxjdnnajubwsj"
receiver_email = "briankipkirui393@gmail.com"
smtp_server = "smtp.gmail.com"
smtp_port = 587
database_path = 'master.db'

class OTPForm:
    def __init__(self, master):
        self.master = master
        self.master.title("OTP Verification")
        self.master.geometry("400x200")
        self.master.configure(bg="#F0F0F0")

        self.otp_label = tk.Label(master, text="Enter OTP:", font=("Arial", 14), bg="#F0F0F0")
        self.otp_label.grid(row=0, column=0, pady=10)

        self.otp_entry = tk.Entry(master, show='*', font=("Arial", 14))
        self.otp_entry.grid(row=0, column=1, pady=10)

        self.send_button = tk.Button(master, text="Send OTP", command=self.send_otp, font=("Arial", 12), bg="blue", fg="white")
        self.send_button.grid(row=1, column=0, pady=10, padx=5)

        self.verify_button = tk.Button(master, text="Download", command=self.verify_otp, font=("Arial", 12), bg="green", fg="white")
        self.verify_button.grid(row=1, column=1, pady=10, padx=5)

        # Generate a random OTP for demonstration purposes
        self.generated_otp = str(random.randint(100000, 999999))

    def send_otp(self):
        # Send OTP via email
        send_otp_via_email(sender_email, sender_password, receiver_email, self.generated_otp, smtp_server, smtp_port)

        # Insert OTP into SQLite database
        insert_otp_into_database(receiver_email, self.generated_otp)

        messagebox.showinfo("OTP Sent", "OTP sent to your registered email.")

    def verify_otp(self):
        entered_otp = self.otp_entry.get()

        # Simulate OTP verification logic (replace with actual logic)
        if entered_otp == self.generated_otp:
            messagebox.showinfo("OTP Verified", "OTP verified successfully!")
            subprocess.call(["python3", "donloadafter.py"])
            messagebox.showinfo("File Download", "File Downloaded sucessfully")
            
        else:
            messagebox.showerror("Invalid OTP", "Invalid OTP. Please try again.")

# Insert OTP into SQLite database
def insert_otp_into_database(email, otp):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    # Create a table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS otp_data (
            email TEXT PRIMARY KEY,
            otp TEXT
        )
    ''')

    # Insert or update the OTP for the given email
    cursor.execute('''
        INSERT OR REPLACE INTO otp_data (email, otp) VALUES (?, ?)
    ''', (email, otp))

    connection.commit()
    connection.close()

# Send OTP via email
def send_otp_via_email(sender_email, sender_password, receiver_email, otp, smtp_server, smtp_port):
    subject = "Your OTP Verification Code"
    body = f"Your OTP code is: {otp}"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

if __name__ == "__main__":
    root = tk.Tk()
    app = OTPForm(root)
    root.mainloop()
