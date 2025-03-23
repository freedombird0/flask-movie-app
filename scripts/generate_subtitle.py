import os

# 📂 Define paths
base_folder = "C:\\Users\\Mahdi1\\Desktop\\mov"
translated_file = os.path.join(base_folder, "output", "translated.txt")  # 🔄 Use the translated text
subtitle_folder = os.path.join(base_folder, "output")  # 🔹 Save subtitles directly in `output`
video_folder = os.path.join(base_folder, "uploads")  # 🔹 Folder for original videos

# ✅ Check that the translated text file exists
if not os.path.exists(translated_file):
    print("❌ Translation file not found! Make sure to run `translate.py` first.")
    exit()

# 📖 Read the translated text
with open(translated_file, "r", encoding="utf-8") as f:
    translated_text = f.read().strip()

if not translated_text:
    print("❌ The translation file is empty!")
    exit()

# 📺 Get the current video name
video_files = [f for f in os.listdir(video_folder) if f.endswith(('.mp4', '.avi', '.mov', '.mkv'))]

if not video_files:
    print("❌ No video found in the `uploads` folder!")
    exit()

# 🔹 Use the latest uploaded video
video_filename = sorted(video_files, key=lambda x: os.path.getctime(os.path.join(video_folder, x)), reverse=True)[0]
base_name = os.path.splitext(video_filename)[0]  # 🔄 Extract video name without extension
subtitle_path = os.path.join(subtitle_folder, f"{base_name}.srt")  # 🔹 Save subtitles with same video name

# ✅ Make sure the subtitle folder exists (directly in `output/`)
os.makedirs(subtitle_folder, exist_ok=True)

# 📝 Write subtitles to an SRT file
with open(subtitle_path, "w", encoding="utf-8") as f:
    lines = translated_text.split('. ')  # 🔹 Split the text into sentences by period
    for idx, line in enumerate(lines, start=1):
        start_time = f"00:00:{(idx-1)*3:02d},000"
        end_time = f"00:00:{idx*3:02d},000"
        f.write(f"{idx}\n{start_time} --> {end_time}\n{line.strip()}\n\n")

print(f"✅ Subtitle file created: {subtitle_path}")
