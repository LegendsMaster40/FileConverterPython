import os
import sys
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from moviepy.video.io.VideoFileClip import VideoFileClip
from pydub import AudioSegment

# Set the path to ffmpeg
os.environ["FFMPEG_BINARY"] = r"C:\ffmpeg\ffmpeg-7.1-essentials_build\bin\ffmpeg.exe"

# Ensure the working directory is the location of the .exe if running as a bundled app
if getattr(sys, 'frozen', False):
    # Running as an executable
    os.chdir(sys._MEIPASS)

# Check if ffmpeg is available
if not shutil.which("ffmpeg"):
    messagebox.showerror("Error", "ffmpeg not found. Please ensure ffmpeg is installed and accessible.")
    sys.exit(1)

class MediaConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Converter")
        self.root.geometry("400x300")

        # Input File
        self.input_label = ttk.Label(root, text="Select Media File:")
        self.input_label.pack(pady=5)
        self.input_file_entry = ttk.Entry(root, width=40)
        self.input_file_entry.pack(pady=5)
        self.browse_button = ttk.Button(root, text="Browse", command=self.browse_file)
        self.browse_button.pack(pady=5)

        # Output Format
        self.format_label = ttk.Label(root, text="Select Output Format:")
        self.format_label.pack(pady=5)
        self.format_combobox = ttk.Combobox(root, values=["mp4", "avi", "mov", "mp3", "wav"], state="readonly")
        self.format_combobox.pack(pady=5)

        # Convert Button
        self.convert_button = ttk.Button(root, text="Convert", command=self.convert_file)
        self.convert_button.pack(pady=20)

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Media Files", "*.*"), ("All Files", "*.*")]
        )
        if file_path:
            self.input_file_entry.delete(0, tk.END)
            self.input_file_entry.insert(0, file_path)

    def convert_file(self):
        input_file = self.input_file_entry.get()
        output_format = self.format_combobox.get()

        if not input_file or not output_format:
            messagebox.showerror("Error", "Please select a file and output format!")
            return

        output_file = os.path.splitext(input_file)[0] + f".{output_format}"

        # Ensure output file doesn't overwrite existing file
        counter = 1
        while os.path.exists(output_file):
            output_file = os.path.splitext(input_file)[0] + f"_{counter}.{output_format}"
            counter += 1

        try:
            if output_format in ["mp4", "avi", "mov"]:
                # Video conversion
                clip = VideoFileClip(input_file)
                clip.write_videofile(output_file, codec="libx264")
            elif output_format in ["mp3", "wav"]:
                # Audio conversion
                audio = AudioSegment.from_file(input_file)
                audio.export(output_file, format=output_format)
            else:
                messagebox.showerror("Error", f"Unsupported format: {output_format}")
                return

            messagebox.showinfo("Success", f"File converted successfully to {output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = MediaConverterApp(root)
    root.mainloop()
