import os
import threading
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from moviepy.editor import VideoFileClip
import subprocess

# 📂 Set up paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "../output")
AUDIO_DIR = os.path.join(BASE_DIR, "../audio")
FRAMES_DIR = os.path.join(BASE_DIR, "../frames")

# ✅ Ensure required directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(FRAMES_DIR, exist_ok=True)

# 🎥 Select video file
def select_video():
    video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mov;*.mkv")])
    if video_path:
        video_entry.delete(0, tk.END)
        video_entry.insert(0, video_path)

# 🔄 Start video processing
def start_processing():
    video_path = video_entry.get()
    language = language_var.get()

    if not video_path:
        messagebox.showerror("Error", "Please select a video file!")
        return

    status_label.config(text="⏳ Processing...")
    progress_bar.start()

    def process():
        try:
            # Extract audio
            audio_output = os.path.join(AUDIO_DIR, "output_audio.wav")
            clip = VideoFileClip(video_path)
            clip.audio.write_audiofile(audio_output)

            # Run transcription
            subprocess.run(["python", os.path.join(BASE_DIR, "transcribe.py")], check=True)

            # Run translation
            subprocess.run(["python", os.path.join(BASE_DIR, "translate.py")], input=f"{language}\n1", text=True, check=True)

            # Generate subtitles
            subprocess.run(["python", os.path.join(BASE_DIR, "generate_subtitle.py")], check=True)

            # Generate final video
            subprocess.run(["python", os.path.join(BASE_DIR, "generate_video.py")], check=True)

            # Update UI after completion
            status_label.config(text="✅ Processing complete!")
            progress_bar.stop()

            # Play the final video after completion
            final_video = os.path.join(OUTPUT_DIR, "final_video_with_subtitles.mp4")
            if os.path.exists(final_video):
                os.system(f'start {final_video}')

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during processing: {str(e)}")
            status_label.config(text="❌ Processing failed")
            progress_bar.stop()

    threading.Thread(target=process).start()

# 🖥️ Set up the GUI
root = tk.Tk()
root.title("Video Processing")
root.geometry("500x350")

# 🎥 Video file path entry
ttk.Label(root, text="📂 Select video file:").pack(pady=5)
video_entry = ttk.Entry(root, width=50)
video_entry.pack(pady=5)
ttk.Button(root, text="📁 Browse", command=select_video).pack(pady=5)

# 🌍 Translation language selection
ttk.Label(root, text="🌍 Select translation language:").pack(pady=5)
language_var = tk.StringVar(value="en")
languages = [("English", "en"), ("Arabic", "ar"), ("French", "fr"), ("German", "de")]
for lang, code in languages:
    ttk.Radiobutton(root, text=lang, variable=language_var, value=code).pack(anchor="w")

# 🔄 Start processing button
ttk.Button(root, text="🚀 Start Processing", command=start_processing).pack(pady=10)

# ⏳ Progress bar
status_label = ttk.Label(root, text="🔹 Ready")
status_label.pack(pady=5)
progress_bar = ttk.Progressbar(root, mode="indeterminate", length=300)
progress_bar.pack(pady=5)

# 🖥️ Run the GUI
root.mainloop()
