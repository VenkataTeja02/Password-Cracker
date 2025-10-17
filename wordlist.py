import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import hashlib
import base64
from Crypto.Hash import MD4
import threading
import time

#Window
root = ctk.CTk()
root.title("Word List Attack")
root.geometry('800x500')

# Stop Process
stop_event = threading.Event()

# Function to hash text
def hash_text(text, hash_type):
    if hash_type == 'MD5':
        return hashlib.md5(text.encode()).hexdigest()
    elif hash_type == 'MD4':
        return MD4.new(text.encode()).hexdigest()
    elif hash_type == 'SHA1':
        return hashlib.sha1(text.encode()).hexdigest()
    elif hash_type == 'SHA256':
        return hashlib.sha256(text.encode()).hexdigest()
    elif hash_type == 'SHA512':
        return hashlib.sha512(text.encode()).hexdigest()
    elif hash_type == 'Base64':
        return base64.b64encode(text.encode()).decode('utf-8')
    else:
        return None

# Function to browse file
def browse_file(entry):
    file_path = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt")],  # Only .txt files
        title="Select a Text File"
    )
    if file_path:  # Update the entry if a file is selected
        entry.delete(0, tk.END)
        entry.insert(0, file_path)

# Function to start the hash in a separate thread
def start_verify_thread():
    global thread
    stop_event.clear()  # Clear the stop process before starting a new process
    thread = threading.Thread(target=verify_hash, daemon=True)
    thread.start()

# Function to check hash
def verify_hash():
    hash_file_path = entry_hash_file.get()
    wordlist_file_path = entry_wordlist_file.get()
    decoding_output.delete('1.0', tk.END)
    result.set("")

    # Check if both files are .txt
    if not (hash_file_path.endswith('.txt') and wordlist_file_path.endswith('.txt')):
        messagebox.showerror("Invalid File Type", "Please select .txt files for both hash and wordlist.")
        return

    try:
        start_time = time.time()  # Timer Start

        with open(hash_file_path, 'r', encoding='utf-8') as hash_file:
            input_hashes = [line.strip() for line in hash_file]

        matches = []

        with open(wordlist_file_path, 'r', encoding='utf-8', errors='ignore') as wordlist_file:
            for line in wordlist_file:
                if stop_event.is_set():  # Check if the stop event is set
                    result.set("Process was canceled.")
                    decoding_output.insert(tk.END, "Process was canceled by user.\n")
                    return

                word = line.strip()
                for hash_type in ["MD5", "MD4", "SHA1", "SHA256", "SHA512", "Base64"]:
                    if stop_event.is_set():  # If cancel button is Clicked
                        result.set("Process was canceled.")
                        decoding_output.insert(tk.END, "Process was canceled by user.\n")
                        return
                    computed_hash = hash_text(word, hash_type)
                    decoding_output.insert(tk.END, f"Trying {word} with {hash_type}: {computed_hash}\n")  # Decoding Process
                    decoding_output.see(tk.END)
                    if computed_hash in input_hashes:
                        matches.append(f"Match found - Word: {word}, Hash ({hash_type}): {computed_hash}")  # Match Found 
                        input_hashes.remove(computed_hash)

                root.update_idletasks()  # Updates if more matches are found

        not_found_count = len(input_hashes)
        end_time = time.time()   # Timer Ends
        time_taken = end_time - start_time  

        # Result Section
        result_text = f"Time taken: {time_taken:.2f} seconds\n"  
        result_text += f"Matches found: {len(matches)}\n"
        result_text += f"Hashes not found: {not_found_count}\n\n"
        result_text += "\n".join(matches)
        result.set(result_text)

    except Exception as e:   # Exception Handling
        result.set(f"Error: {str(e)}")
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to save output results to a .txt file
def save_results_to_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                                             title="Save results as...")
    if file_path:
        with open(file_path, "w") as file:
            file.write(result.get())
        messagebox.showinfo("Save Results", f"Results saved to {file_path}")

# Function to stop the current process
def stop_process():
    stop_event.set()
    if thread.is_alive():  
        thread.join(1)  
        result.set("Process canceled by user.")  

# Function to clear all inputs and outputs
def clear_all():
    entry_hash_file.delete(0, tk.END)
    entry_wordlist_file.delete(0, tk.END)
    result.set("")
    decoding_output.delete('1.0', tk.END)

# GUI
frame1 = ctk.CTkFrame(root)  # Frame for Hash
frame1.pack(fill='x', padx=10, pady=5)  

entry_hash_file_label = ctk.CTkLabel(frame1, text="Select Hash File:")   # Hash File label
entry_hash_file_label.pack(side='left', padx=5, pady=5)

entry_hash_file = ctk.CTkEntry(frame1, width=300)    # Hash file entry
entry_hash_file.pack(side='left', fill='x', expand=True, padx=5, pady=5)

browse_hash_file_button = ctk.CTkButton(frame1, text="Browse", command=lambda: browse_file(entry_hash_file))   # Hash Browse
browse_hash_file_button.pack(side='left', padx=5, pady=5)

frame2 = ctk.CTkFrame(root)  # Frame for wordlist selection
frame2.pack(fill='x', padx=10, pady=5)

entry_wordlist_file_label = ctk.CTkLabel(frame2, text="Select Wordlist File:")  # Wordlist File label
entry_wordlist_file_label.pack(side='left', padx=5, pady=5)

entry_wordlist_file = ctk.CTkEntry(frame2, width=300)   # Wordlist file entry
entry_wordlist_file.pack(side='left', fill='x', expand=True, padx=5, pady=5)

browse_wordlist_file_button = ctk.CTkButton(frame2, text="Browse", command=lambda: browse_file(entry_wordlist_file))  # Wordlist Browse
browse_wordlist_file_button.pack(side='left', padx=5, pady=5)

frame_buttons = ctk.CTkFrame(root)  # Frame for buttons
frame_buttons.pack(pady=10)

verify_button = ctk.CTkButton(frame_buttons, text="Start Cracking", command=start_verify_thread)  # Start Attack button
verify_button.pack(side='left', padx=5)

stop_button = ctk.CTkButton(frame_buttons, text="Cancel", command=stop_process)   # Cancel Button
stop_button.pack(side='left', padx=5)

clear_button = ctk.CTkButton(frame_buttons, text="Clear", command=clear_all)  # Clear Button
clear_button.pack(side='left', padx=5)

save_button = ctk.CTkButton(frame_buttons, text="Save Results", command=save_results_to_file)   # Save Results BUtton
save_button.pack(side='left', padx=5)

frame3 = ctk.CTkFrame(root)  # Frame for results
frame3.pack(fill='x', padx=10, pady=5)

result_label = ctk.CTkLabel(frame3, text="Result:") # Rsult Label
result_label.pack(anchor='w', padx=5, pady=5)

result = tk.StringVar()   # Result Disply 
result_display = ctk.CTkLabel(frame3, textvariable=result, width=300)
result_display.pack(fill='x', padx=5, pady=5)

frame4 = ctk.CTkFrame(root)  # Frame for decoding process
frame4.pack(fill='both', expand=True, padx=10, pady=5)

decoding_output_label = ctk.CTkLabel(frame4, text="Decoding Process:")  # Deoding Label
decoding_output_label.pack(anchor='nw', padx=5, pady=5)

decoding_output = tk.Text(frame4, height=10, width=50)  
decoding_output.pack(fill='both', expand=True, padx=5, pady=5)

root.mainloop()
