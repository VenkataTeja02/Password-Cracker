import os
import shutil
import subprocess
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox
import queue

# Global variables
process = None
output_queue = queue.Queue()

# Function to select handshake file
def select_handshake_file():
    handshake_file = filedialog.askopenfilename(
        title="Select Handshake File",
        filetypes=[("Handshake Files", "*.cap *.pcapng *.hccapx"), ("All Files", "*.*")]
    )
    handshake_entry.delete(0, ctk.END)
    handshake_entry.insert(0, handshake_file)

# Function to select wordlist file
def select_wordlist_file():
    wordlist_file = filedialog.askopenfilename(
        title="Select Wordlist File",
        filetypes=[("Wordlist Files", "*.txt"), ("All Files", "*.*")]
    )
    wordlist_entry.delete(0, ctk.END)
    wordlist_entry.insert(0, wordlist_file)

# Function to run aircrack-ng in a separate thread
def run_aircrack():
    global process

    handshake_file = handshake_entry.get()
    wordlist_file = wordlist_entry.get()

    # Check if both files are selected
    if not handshake_file or not wordlist_file:
        messagebox.showwarning("Input Error", "Please select both handshake and wordlist files.")
        return

    # Check if aircrack-ng is installed
    if not shutil.which("aircrack-ng"):
        messagebox.showerror("Error", "aircrack-ng is not installed or not found in PATH.")
        return

    # Clear 
    result_text.delete(1.0, ctk.END)  
    password_label.configure(text="")  # Clear password display

    # Disable buttons
    crack_button.configure(state=ctk.DISABLED)
    cancel_button.configure(state=ctk.NORMAL)

    # Start the aircrack-ng process in a separate thread
    thread = threading.Thread(target=aircrack_process, args=(handshake_file, wordlist_file))
    thread.start()

    # Continuously check the output queue for updates
    check_output_queue()

# Function to handle the aircrack-ng process
def aircrack_process(handshake_file, wordlist_file):
    global process

    try:
        # Run aircrack-ng command
        command = ["aircrack-ng", "-w", wordlist_file, handshake_file]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Read the output line by line
        for line in iter(process.stdout.readline, ''):
            if line:
                output_queue.put(line)  # Add the output to the queue

        process.stdout.close()
        process.wait()

        if process.returncode != 0:
            output_queue.put("ERROR: Failed to crack the password or no password found.")

    except Exception as e:
        output_queue.put(f"ERROR: An error occurred: {e}")

    finally:
        process = None
        output_queue.put("DONE")  

# Function to check the output queue and update the GUI
def check_output_queue():
    try:
        while True:
            line = output_queue.get_nowait()  # Get the next line from the queue

            if line.startswith("ERROR:"):
                error_message = line.split(":", 1)[1]
                messagebox.showerror("Error", error_message)

            elif "KEY FOUND!" in line:
                # Extract and display the password
                import re
                match = re.search(r'KEY FOUND! \[ (.+) \]', line)
                if match:
                    password = match.group(1)
                    display_password(password)
                    return  # Stop checking queue

            elif line == "DONE":
                # Re-enable buttons
                crack_button.configure(state=ctk.NORMAL)
                cancel_button.configure(state=ctk.DISABLED)
                return

            else:
                result_text.insert(ctk.END, line)
                result_text.see(ctk.END)  # Auto-scroll to the end

    except queue.Empty:
        root.after(100, check_output_queue)

# Function to handle password display and message box
def display_password(password):
    password_label.configure(text=f"Password: {password}")
    messagebox.showinfo("Password Found", f"The cracked password is: {password}")

# Function to clear the process
def clear_process():
    global process
    if process is not None:
        try:
            process.terminate()
            process = None
        except Exception as e:
            messagebox.showerror("Error", f"Failed to terminate the process: {e}")
    
    # Clear results and reset UI elements
    result_text.delete(1.0, ctk.END)
    password_label.configure(text="")
    handshake_entry.delete(0, ctk.END)
    wordlist_entry.delete(0, ctk.END)
    crack_button.configure(state=ctk.NORMAL)
    cancel_button.configure(state=ctk.DISABLED)

# Function to cancel the cracking process
def cancel_aircrack():
    global process
    if process is not None:
        try:
            process.terminate()
            process = None
            clear_process()
            messagebox.showinfo("Cancelled", "Cracking process has been cancelled.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to cancel the process: {e}")
    else:
        messagebox.showwarning("Warning", "No running process to cancel.")

# Main window
root = ctk.CTk()
root.title("Wi-Fi Password Cracker")
root.geometry("700x400")
root.resizable(False, False)

# Theme and color
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Handshake file selection
handshake_frame = ctk.CTkFrame(root)
handshake_frame.pack(pady=5)

handshake_label = ctk.CTkLabel(handshake_frame, text="Select Handshake File:")
handshake_label.pack(side=ctk.LEFT, padx=5)

handshake_entry = ctk.CTkEntry(handshake_frame, width=300)
handshake_entry.pack(side=ctk.LEFT, padx=5)

handshake_button = ctk.CTkButton(handshake_frame, text="Browse", command=select_handshake_file)
handshake_button.pack(side=ctk.LEFT, padx=5)

# Wordlist file selection
wordlist_frame = ctk.CTkFrame(root)
wordlist_frame.pack(pady=5)

wordlist_label = ctk.CTkLabel(wordlist_frame, text="Select Wordlist File:")
wordlist_label.pack(side=ctk.LEFT, padx=5)

wordlist_entry = ctk.CTkEntry(wordlist_frame, width=300)
wordlist_entry.pack(side=ctk.LEFT, padx=5)

wordlist_button = ctk.CTkButton(wordlist_frame, text="Browse", command=select_wordlist_file)
wordlist_button.pack(side=ctk.LEFT, padx=5)

# Buttons frame
buttons_frame = ctk.CTkFrame(root)
buttons_frame.pack(pady=10)

# Start cracking button
crack_button = ctk.CTkButton(buttons_frame, text="Start Cracking", command=run_aircrack)
crack_button.pack(side=ctk.LEFT, padx=5)

# Cancel button
cancel_button = ctk.CTkButton(buttons_frame, text="Cancel", command=cancel_aircrack, state=ctk.DISABLED)
cancel_button.pack(side=ctk.LEFT, padx=5)

# Clear button
clear_button = ctk.CTkButton(buttons_frame, text="Clear", command=clear_process)
clear_button.pack(side=ctk.LEFT, padx=5)

# Result
result_text = ctk.CTkTextbox(root, height=150, width=500)
result_text.pack(pady=10)

# Cracked password
password_label = ctk.CTkLabel(root, text="", font=("Arial", 18, "bold"))
password_label.pack(pady=20)

root.mainloop()
