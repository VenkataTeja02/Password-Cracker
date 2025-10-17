import tkinter as tk
import customtkinter as ctk
import subprocess
import re

# Router default credentials - Brand and Gateway
router_credentials = {
    'GPON': ['192.168.0.1', '192.168.1.1'],
    'TP-Link': ['192.168.0.1', '192.168.1.1'],
    'Linksys': ['192.168.0.1', '192.168.1.1'],
    'Netgear': ['192.168.1.1', '192.168.0.1'],
    'Cisco': ['192.168.0.1', '192.168.1.1'],
    'D-Link': ['192.168.0.1', '192.168.1.1'],
    'BenQ': ['192.168.1.1'],
    'ASUS': ['192.168.0.1', '192.168.1.1'],
    'Belkin': ['192.168.2.1', '192.168.1.1'],
    'Sitecom': ['192.168.0.1'],
    'Huawei': ['192.168.1.1'],
    'Tenda': ['192.168.0.1', '192.168.1.1'],
    'Xiaomi Mi': ['192.168.31.1', '192.168.1.1'],
    'Jio':['192.168.29.1']
}

# Default credentials for specific (gateway, brand) pairs
credentials_for_gateways = {
    ('192.168.0.1', 'GPON'): ('admin', 'admin'),
    ('192.168.1.1', 'GPON'): ('admin', 'admin'),
    ('192.168.0.1', 'TP-Link'): ('admin', 'admin'),
    ('192.168.1.1', 'TP-Link'): ('admin', 'admin'),
    ('192.168.0.1', 'Linksys'): ('admin', 'admin'),
    ('192.168.1.1', 'Linksys'): ('admin', 'admin'),
    ('192.168.0.1', 'Netgear'): ('admin', 'password'),
    ('192.168.1.1', 'Netgear'): ('admin', 'password'),
    ('192.168.1.1', 'Cisco'): ('admin', 'password'),
    ('192.168.0.1', 'Cisco'): ('admin', 'password'),
    ('192.168.0.1', 'D-Link'): ('admin', 'admin'),
    ('192.168.1.1', 'D-Link'): ('admin', 'admin'),
    ('192.168.1.1', 'BenQ'): ('admin', 'admin'),
    ('192.168.0.1', 'ASUS'): ('admin', 'admin'),
    ('192.168.1.1', 'ASUS'): ('admin', 'admin'),
    ('192.168.2.1', 'Belkin'): ('admin', 'admin'),
    ('192.168.1.1', 'Belkin'): ('admin', 'admin'),
    ('192.168.0.1', 'Sitecom'): ('sitecom', 'admin'),
    ('192.168.1.1', 'Huawei'): ('admin', 'admin'),
    ('192.168.0.1', 'Tenda'): ('admin', 'admin'),
    ('192.168.1.1', 'Tenda'): ('admin', 'admin'),
    ('192.168.31.1', 'Xiaomi Mi'): ('admin', 'admin'),
    ('192.168.1.1', 'Xiaomi Mi'): ('', 'admin'),
    ('192.168.29.1', 'Jio'):('admin','Jiocentrum')
}

# Function to get the default gateway for the Wireless LAN adapter
def get_default_gateway():
    try:
        result = subprocess.check_output('ipconfig', shell=True).decode()
        wifi_section = re.search(r'Wireless LAN adapter Wi-Fi[^\n]*(\n\s+[^\n]*)*', result)
        if wifi_section:
            lines = wifi_section.group(0).split('\n')
            for i, line in enumerate(lines):
                if 'Default Gateway' in line and i + 1 < len(lines):
                    next_line_match = re.search(r'\s*(\d+\.\d+\.\d+\.\d+)', lines[i + 1])
                    if next_line_match:
                        return next_line_match.group(1)
    except Exception as e:
        print(f"Error: {e}")
    return None

# Function to get router credentials based on the default gateway and selected brand
def get_router_credentials(brand):
    gateway = get_default_gateway()
    print(f"Default Gateway: {gateway}")  # Debug print
    if gateway and brand in router_credentials:
        possible_gateways = router_credentials[brand]
        if gateway in possible_gateways:
            credentials = credentials_for_gateways.get((gateway, brand), ('Unknown', 'Unknown'))
            print(f"Retrieved Credentials for {brand}: {credentials}")  # Debug print
            return credentials
    return ('Unknown', 'Unknown')

# Function to display the credentials
def display_credentials():
    selected_brand = brand_var.get()
    username, password = get_router_credentials(selected_brand)
    username_label_value.configure(text=username)
    password_label_value.configure(text=password)

# Function to clear PRocess
def clear_credentials():
    username_label_value.configure(text="")
    password_label_value.configure(text="")

# Function to copy text
def copy_to_clipboard(text):
    app.clipboard_clear()
    app.clipboard_append(text)

# Main window
app = ctk.CTk()
app.title("Router Default Credentials")
app.geometry("600x400")
app.resizable(False, False)  # Fix the window size


window_width = 600
window_height = 400
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
position_top = int(screen_height/2 - window_height/2)
position_right = int(screen_width/2 - window_width/2)
app.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

# widgets
app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=1)
app.grid_rowconfigure(2, weight=1)
app.grid_rowconfigure(3, weight=1)
app.grid_rowconfigure(4, weight=1)
app.grid_rowconfigure(5, weight=1)
app.grid_rowconfigure(6, weight=1)
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure(2, weight=1)

# labels
title_label = ctk.CTkLabel(app, text="Router Default Credentials", font=("Helvetica", 16))
title_label.grid(row=0, column=0, columnspan=3, pady=20)

brand_label = ctk.CTkLabel(app, text="Router Brand:")
brand_label.grid(row=1, column=0, sticky="e", padx=5, pady=10)

brand_var = tk.StringVar()

# Dropdown menu for brand selection
brand_options = ['GPON','TP-Link', 'Linksys','Jio', 'Netgear', 'Cisco', 'D-Link','BenQ','ASUS','Belkin','Sitecom','Huawei','Tenda','Xiaomi Mi']
brand_menu = ctk.CTkOptionMenu(app, variable=brand_var, values=brand_options)
brand_menu.grid(row=1, column=1, sticky="w", padx=5, pady=10)
brand_var.set(brand_options[0])  # Set default value

username_label = ctk.CTkLabel(app, text="Username:") 
username_label.grid(row=2, column=0, sticky="e", padx=5, pady=10)

username_label_value = ctk.CTkLabel(app, text="")  
username_label_value.grid(row=2, column=1, sticky="w", padx=5, pady=10)

username_copy_button = ctk.CTkButton(app, text="Copy", command=lambda: copy_to_clipboard(username_label_value.cget("text")))
username_copy_button.grid(row=2, column=2, padx=5, pady=10)

password_label = ctk.CTkLabel(app, text="Password:")
password_label.grid(row=3, column=0, sticky="e", padx=5, pady=10)

password_label_value = ctk.CTkLabel(app, text="")
password_label_value.grid(row=3, column=1, sticky="w", padx=5, pady=10)

password_copy_button = ctk.CTkButton(app, text="Copy", command=lambda: copy_to_clipboard(password_label_value.cget("text")))
password_copy_button.grid(row=3, column=2, padx=5, pady=10)

# Buttons
show_button = ctk.CTkButton(app, text="Show Credentials", command=display_credentials)
show_button.grid(row=4, column=0, columnspan=3, pady=10)

clear_button = ctk.CTkButton(app, text="Clear", command=clear_credentials)
clear_button.grid(row=5, column=0, columnspan=3, pady=10)

app.mainloop()
