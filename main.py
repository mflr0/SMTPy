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
import argparse
import json
import os
import markdown
import re

try:
    import tkinter as tk
    from tkinter import messagebox
    import ttkthemes
    import tkinter.ttk as ttk
    GUI_MODE = True
except ImportError:
    GUI_MODE = False

def send_mail(username, password, sender_name, to_emails, cc_emails, subject, body):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(username, password)

        msg = MIMEMultipart()
        msg['From'] = f"{sender_name} <{username}>"
        msg['To'] = ', '.join(to_emails)
        msg['Subject'] = subject

        # Convert Markdown to HTML
        html_body = markdown.markdown(body)
        msg.attach(MIMEText(html_body, 'html'))

        all_recipients = to_emails + cc_emails
        server.sendmail(username, all_recipients, msg.as_string())
        server.quit()
    except smtplib.SMTPAuthenticationError:
        raise RuntimeError("Authentication failed. Please check your username and password.")
    except smtplib.SMTPException as e:
        raise RuntimeError(f"Failed to send email: {e}")

def validate_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValueError("Invalid email address")

def submit_form(args=None):
    if args is None:
        parser = argparse.ArgumentParser(description="Send email from CLI or GUI")
        parser.add_argument("-cli", action="store_true", help="Run in CLI mode")
        args = parser.parse_args()

    if args.cli:
        username = input("Email: ")
        password = input("Password: ")
        sender_name = input("Sender Name: ")
        to_emails = input("To Email(s) (comma-separated): ").split(',')
        cc_emails = []
        subject = input("Subject: ")
        body = input("Body: ")
    else:
        username = username_entry.get()
        password = password_entry.get()
        sender_name = sender_name_entry.get()
        to_emails = [email.strip() for email in to_email_entry.get().split(',')]
        cc_emails = []
        subject = subject_entry.get()
        body = body_entry.get("1.0", "end-1c")

    try:
        validate_email(username)
        if not password:
            raise ValueError("Password cannot be empty")
        for email in to_emails:
            validate_email(email)
    except ValueError as e:
        error_message = f"Invalid input: {e}"
        if args.cli:
            print("Error:", error_message)
        else:
            messagebox.showerror("Error", error_message)
        return

    try:
        send_mail(username, password, sender_name, to_emails, cc_emails, subject, body)
        success_message = "Email sent successfully"
        if args.cli:
            print(success_message)
        else:
            messagebox.showinfo("Success", success_message)
            if save_credentials_var.get():
                save_credentials(username, password)
    except Exception as e:
        error_message = f"An error occurred: {e}"
        if args.cli:
            print("Error:", error_message)
        else:
            messagebox.showerror("Error", error_message)

def load_credentials():
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            lines = f.readlines()
            for line in lines:
                key, value = line.strip().split('=')
                if key == 'EMAIL':
                    username_entry.insert(0, value)
                elif key == 'PASSWORD':
                    password_entry.insert(0, value)

def save_credentials(username, password):
    credentials = f"EMAIL={username}\nPASSWORD={password}"
    with open('.env', 'w') as f:
        f.write(credentials)

def toggle_password_visibility():
    if password_entry.cget("show") == "":
        password_entry.config(show="*")
    else:
        password_entry.config(show="")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send email from CLI or GUI")
    parser.add_argument("-cli", action="store_true", help="Run in CLI mode")
    args = parser.parse_args()

    if args.cli:
        try:
            submit_form(args)
        except RuntimeError as e:
            print("Error:", str(e))
    else:
        if GUI_MODE:
            root = ttkthemes.ThemedTk(theme="equilux")
            root.resizable(False, False)

            form_frame = ttk.Frame(root, padding=(20, 10))
            form_frame.grid(row=0, column=0, sticky='ew')

            button_frame = ttk.Frame(root, padding=(0, 10))
            button_frame.grid(row=1, column=0, sticky='ew')

            sender_name_label = ttk.Label(form_frame, text="Sender Name:")
            sender_name_label.grid(row=0, column=0, padx=5, pady=5)
            sender_name_entry = ttk.Entry(form_frame)
            sender_name_entry.grid(row=0, column=1, padx=5, pady=5)

            username_label = ttk.Label(form_frame, text="Email:")
            username_label.grid(row=1, column=0, padx=5, pady=5)
            username_entry = ttk.Entry(form_frame)
            username_entry.grid(row=1, column=1, padx=5, pady=5)

            password_label = ttk.Label(form_frame, text="Password:")
            password_label.grid(row=2, column=0, padx=5, pady=5)
            password_entry = ttk.Entry(form_frame, show="*")
            password_entry.grid(row=2, column=1, padx=5, pady=5)

            show_password_var = tk.BooleanVar()
            show_password_checkbox = ttk.Checkbutton(form_frame, text="Show Password", variable=show_password_var, command=toggle_password_visibility)
            show_password_checkbox.grid(row=2, column=2, padx=5, pady=5)

            to_email_label = ttk.Label(form_frame, text="To Email(s):")
            to_email_label.grid(row=3, column=0, padx=5, pady=5)
            to_email_entry = ttk.Entry(form_frame)
            to_email_entry.grid(row=3, column=1, padx=5, pady=5)

            subject_label = ttk.Label(form_frame, text="Subject:")
            subject_label.grid(row=4, column=0, padx=5, pady=5)
            subject_entry = ttk.Entry(form_frame)
            subject_entry.grid(row=4, column=1, padx=5, pady=5)

            body_label = ttk.Label(form_frame, text="Body:")
            body_label.grid(row=5, column=0, padx=5, pady=5)
            body_entry = tk.Text(form_frame, height=10, width=40)
            body_entry.grid(row=5, column=1, padx=5, pady=5, sticky='ew')

            submit_button = ttk.Button(button_frame, text="Send Email", command=submit_form)
            submit_button.pack(side=tk.LEFT, padx=5, pady=5, expand=True)

            save_credentials_var = tk.IntVar()
            save_credentials_checkbox = ttk.Checkbutton(button_frame, text="Save Credentials", variable=save_credentials_var)
            save_credentials_checkbox.pack(side=tk.RIGHT, padx=5, pady=5, expand=True)

            load_credentials()

            root.mainloop()
        else:
            print("Tkinter module is not available, please run in CLI mode.")
