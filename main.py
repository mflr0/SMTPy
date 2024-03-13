##
##  main.py
##  Python-SMTP
##
##  Created by 0xGuigui on 13/03/2024.
##  Contributor(s): 0xGuigui
##

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import tkinter as tk
from tkinter import messagebox
import json
import os
import ttkthemes
import tkinter.ttk as ttk


def send_mail(username, password, to_emails, subject, body):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(username, password)

    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = ', '.join(to_emails)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server.sendmail(username, to_emails, msg.as_string())
    server.quit()


def submit_form():
    username = username_entry.get()
    password = password_entry.get()
    to_emails = [email.strip() for email in to_email_entry.get().split(',')]
    subject = subject_entry.get()
    body = body_entry.get("1.0", "end-1c")

    try:
        send_mail(username, password, to_emails, subject, body)
        messagebox.showinfo("Success", "Email sent successfully")
        if save_credentials_var.get():
            save_credentials(username, password)
    except Exception as e:
        messagebox.showerror("Error", str(e))


def load_credentials():
    if os.path.exists('credentials.json'):
        with open('credentials.json', 'r') as f:
            credentials = json.load(f)
            username_entry.insert(0, credentials['username'])
            password_entry.insert(0, credentials['password'])


def save_credentials(username, password):
    credentials = {'username': username, 'password': password}
    with open('credentials.json', 'w') as f:
        json.dump(credentials, f)


# Create root window
root = ttkthemes.ThemedTk(theme="yaru")

# Create widgets
username_label = ttk.Label(root, text="Email:")
username_label.grid(row=0, column=0, padx=10, pady=10)
username_entry = ttk.Entry(root)
username_entry.grid(row=0, column=1, padx=10, pady=10)

password_label = ttk.Label(root, text="Password:")
password_label.grid(row=1, column=0, padx=10, pady=10)
password_entry = ttk.Entry(root, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=10)

show_password_var = tk.IntVar()
show_password_checkbox = ttk.Checkbutton(root, text="Show Password", variable=show_password_var,
                                         command=lambda: password_entry.configure(
                                             show='*' if not show_password_var.get() else ''))
show_password_checkbox.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

to_email_label = ttk.Label(root, text="To Email(s):")
to_email_label.grid(row=3, column=0, padx=10, pady=10)
to_email_entry = ttk.Entry(root)
to_email_entry.grid(row=3, column=1, padx=10, pady=10)

subject_label = ttk.Label(root, text="Subject:")
subject_label.grid(row=4, column=0, padx=10, pady=10)
subject_entry = ttk.Entry(root)
subject_entry.grid(row=4, column=1, padx=10, pady=10)

body_label = ttk.Label(root, text="Body:")
body_label.grid(row=5, column=0, padx=10, pady=10)
body_entry = tk.Text(root)
body_entry.grid(row=5, column=1, padx=10, pady=10)

submit_button = ttk.Button(root, text="Send Email", command=submit_form)
submit_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

save_credentials_var = tk.IntVar()
save_credentials_checkbox = ttk.Checkbutton(root, text="Save Credentials", variable=save_credentials_var)
save_credentials_checkbox.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

load_credentials()

root.mainloop()
