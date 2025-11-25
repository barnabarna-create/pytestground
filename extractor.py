import os
import requests
import zipfile
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

DOWNLOAD_DIR = "D:/zipfiles"

# Ensure directory exists
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def download_and_extract():
    url = url_entry.get()

    if not url.endswith(".zip"):
        messagebox.showerror("Invalid URL", "Please enter a valid .zip file URL.")
        return

    try:
        status_label.config(text="Downloading...")
        window.update_idletasks()

        zip_path = os.path.join(DOWNLOAD_DIR, "downloaded_file.zip")

        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total_size = int(r.headers.get("content-length", 0))
            downloaded = 0

            with open(zip_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)

                        # Update progress
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            progress_bar["value"] = percent
                            window.update_idletasks()

        status_label.config(text="Extracting...")
        window.update_idletasks()

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(DOWNLOAD_DIR)

        status_label.config(text="Completed!")
        messagebox.showinfo("Success", "Download and extraction completed successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")
        status_label.config(text="Failed")



# ---------------- GUI ----------------

window = tk.Tk()
window.title("ZIP Downloader & Extractor")
window.geometry("480x240")

title_label = tk.Label(window, text="Download & Extract ZIP File", font=("Arial", 16))
title_label.pack(pady=10)

url_label = tk.Label(window, text="Enter ZIP file URL:")
url_label.pack()

url_entry = tk.Entry(window, width=50)
url_entry.pack(pady=5)

download_button = tk.Button(window, text="Download & Extract", command=download_and_extract)
download_button.pack(pady=10)

progress_bar = ttk.Progressbar(window, orient="horizontal", length=350, mode="determinate")
progress_bar.pack(pady=10)

status_label = tk.Label(window, text="")
status_label.pack()

window.mainloop()
