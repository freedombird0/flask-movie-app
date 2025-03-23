import os
from gtts import gTTS

# 📂 Set up the paths
base_folder = "C:\\Users\\Mahdi1\\Desktop\\mov"
output_folder = os.path.join(base_folder, "output")
audio_folder = os.path.join(base_folder, "audio")

# ✅ Find the latest translation file
translated_files = [f for f in os.listdir(output_folder) if f.endswith("_translated.txt")]

if not translated_files:
    print("❌ No translation file found in the `output/` folder!")
    exit()

# 🔍 Select the most recent translation based on creation date
translated_filename = sorted(translated_files, key=lambda x: os.path.getctime(os.path.join(output_folder, x)), reverse=True)[0]
translated_path = os.path.join(output_folder, translated_filename)

# Extract the base video name from the translation file name
video_base_name = translated_filename.replace("_translated.txt", "")
audio_output = os.path.join(audio_folder, f"{video_base_name}_translated_audio.mp3")

# ✅ Ensure the translation file contains text
with open(translated_path, "r", encoding="utf-8") as f:
    text = f.read().strip()

if not text:
    print("❌ Translation file is empty!")
    exit()

print("🔄 Converting text to audio...")

# 🌍 Set the language (default: Arabic)
language = "ar"

# 🗣️ Convert text to audio using Google Text-to-Speech
tts = gTTS(text, lang=language)
os.makedirs(os.path.dirname(audio_output), exist_ok=True)
tts.save(audio_output)

print(f"✅ Audio file saved: {audio_output}")
