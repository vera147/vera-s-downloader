from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import customtkinter
import os
import yt_dlp
import threading

folder_path = os.path.join(os.path.expanduser("~"), "Downloads")

def select_folder_path():
    global folder_path
    folder_path = filedialog.askdirectory()
    
    if folder_path:
        folder_path = folder_path.replace("/", "\\")
        print(f"Selected folder: {folder_path}")
    else:
        print("No folder selected")

def download_format():
    global folder_path
    theformat = download_combobox.get()
    if theformat == "mp3":
        threading.Thread(target=download_audio).start()
    if theformat == "mp4":
        threading.Thread(target=download_video).start()

def download_audio():
    global folder_path
    url = url_entry.get()
    output_directory = folder_path

    if not url:
        print("Error: No URL provided.")
        return
    
    if not output_directory:
            print("Error: No output directory selected.")
            return
    
    if not os.path.exists(output_directory):
            try:
                os.makedirs(output_directory)
            except PermissionError:
                print("Error: Permission denied for creating 'Videos' directory.")
                return

    if url:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_directory, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e: 
            print(f"Error downloading video: {e}")

def download_video():
    global folder_path
    url = url_entry.get()
    output_directory = folder_path

    if not url:
        print("Error: No URL provided.")
        return
    
    if not output_directory:
            print("Error: No output directory selected.")
            return
    
    if not os.path.exists(output_directory):
            try:
                os.makedirs(output_directory)
            except PermissionError:
                print("Error: Permission denied for creating 'Videos' directory.")
                return
            
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(output_directory, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
    except Exception as e:
         print(f"Error downloading video: {e}")
    
root = customtkinter.CTk()
root.geometry("350x267")
root.title("vera's downloader")

tab_holder = customtkinter.CTkTabview(root)
tab_holder.pack(pady=0, padx=10)

downloader_tab = tab_holder.add("Downloader")

url_entry = customtkinter.CTkEntry(downloader_tab, placeholder_text="Enter the url here", width=300)
url_entry.grid(row=0, column=0, columnspan=2, pady=5, padx=5)

yt_format_options = ["mp3", "mp4"]
download_combobox = customtkinter.CTkComboBox(downloader_tab, values=yt_format_options, state="readonly")
download_combobox.grid(row=1, column=0, pady=5, padx=10)

download_button = customtkinter.CTkButton(downloader_tab, text="Download", command=download_format)
download_button.grid(row=1, column=1, pady=5, padx=10)


configurations_tab = tab_holder.add("Configuration")
folder_path_button = customtkinter.CTkButton(configurations_tab, text="File Path", command=select_folder_path).pack()

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

root.mainloop()
