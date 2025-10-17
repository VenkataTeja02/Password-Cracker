from customtkinter import *
import customtkinter
import os
from PIL import Image, ImageTk
import threading
import subprocess

# Window
app = customtkinter.CTk()
app.title("Password Cracker")
app.geometry('945x630')
app.resizable(False, False)
set_appearance_mode('dark')

# Background Image
image_path = os.path.join(os.path.dirname(__file__), 'Background_image.png')
image = customtkinter.CTkImage(light_image=Image.open(image_path), size=(945,630))
image_label = customtkinter.CTkLabel(app, image=image, text="")
image_label.place(relx=0, rely=0)

# Project Info Button
def project_info():
    html_file = "ProjectInfo.html"
    os.startfile(html_file)

button_project_info = customtkinter.CTkButton(master=app, text="PROJECT INFO", bg_color="white", fg_color="#1c93d7", width=200, height=35,  font=("Arial", 17),
                                             hover_color="#00bf63", corner_radius=5, cursor="hand2", command=project_info)
button_project_info.place(x=372, y=290)

# Wordlist attack Button
def wordlist_attack():
    python_file = "wordlist.py"
    # Subprocess
    subprocess.Popen(['python', python_file], creationflags=subprocess.CREATE_NO_WINDOW)

def wordlist_attack_thread():
    threading.Thread(target=wordlist_attack).start()

button_open_python = customtkinter.CTkButton(master=app, text="WORDLIST ATTACK", bg_color="white", fg_color="#1c93d7", width=250, height=35,  font=("Arial", 17),
                                            hover_color="#00bf63", corner_radius=5, cursor="hand2", command=wordlist_attack_thread)
button_open_python.place(x=200, y=350)


# Rainbow table Button
def rainbow_table_attack():
    python_file = "rainbow_table.py"
    # Subprocess
    subprocess.Popen(['python', python_file], creationflags=subprocess.CREATE_NO_WINDOW)

def rainbow_table_attack_thread():
    threading.Thread(target=rainbow_table_attack).start()

button_open_python = customtkinter.CTkButton(master=app, text="RAINBOW TABLE ATTACK", bg_color="white", fg_color="#1c93d7", width=250, height=35,  font=("Arial", 17),
                                            hover_color="#00bf63", corner_radius=5, cursor="hand2", command=rainbow_table_attack_thread)
button_open_python.place(x=495, y=350)


# Router Credentials Button
def router_creds():
    python_file = "router.py"
    # Subprocess
    subprocess.Popen(['python', python_file], creationflags=subprocess.CREATE_NO_WINDOW)

def router_creds_thread():
    threading.Thread(target=router_creds).start()

button_open_python = customtkinter.CTkButton(master=app, text="ROUTER DEFAULT CREDENTIALS", bg_color="white", fg_color="#1c93d7", width=300, height=35,  font=("Arial", 17),
                                            hover_color="#00bf63", corner_radius=5, cursor="hand2", command=router_creds_thread)
button_open_python.place(x=150, y=410)


# WIFI handshakes Button
def wifi_handshakes():
    python_file = "wifi_handshakes.py"
    # Subprocess
    subprocess.Popen(['python', python_file], creationflags=subprocess.CREATE_NO_WINDOW)

def wifi_handshakes_thread():
    threading.Thread(target=wifi_handshakes).start()

button_open_python = customtkinter.CTkButton(master=app, text="WIFI HANDSHAKES DECODER", bg_color="white", fg_color="#1c93d7", width=300, height=35,  font=("Arial", 17),
                                            hover_color="#00bf63", corner_radius=5, cursor="hand2", command=wifi_handshakes_thread)
button_open_python.place(x=495, y=410)


# Website Bruteforce Button
def website_bruteforce():
    python_file = "website-login.py"
    #Subprocess
    subprocess.Popen(['python', python_file], creationflags=subprocess.CREATE_NO_WINDOW)

def website_bruteforce_thread():
    threading.Thread(target=website_bruteforce).start()

button_open_python = customtkinter.CTkButton(master=app, text="WEBSITE LOGIN BRUTEFORCE", bg_color="white", fg_color="#1c93d7", width=350, height=35,  font=("Arial", 17),
                                            hover_color="#00bf63", corner_radius=5, cursor="hand2", command=website_bruteforce_thread)
button_open_python.place(x=298, y=470)

app.mainloop()