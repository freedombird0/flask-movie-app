import os
import torch
import whisper
import subprocess
from deep_translator import GoogleTranslator
from transformers import pipeline

# Check GPU or CPU availability
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"✅ Using device: {device.upper()}")

# Ensure FFmpeg is installed
def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ FFmpeg found!")
    except FileNotFoundError:
        print("❌ FFmpeg not found! Make sure it is installed and added to the system PATH.")
        exit()

check_ffmpeg()

# Load Whisper model for audio-to-text conversion
print("🔄 Loading Whisper model...")
try:
    model = whisper.load_model("medium").to(device)
    print("✅ Whisper model loaded!")
except Exception as e:
    print(f"❌ Error loading Whisper model: {e}")
    exit()

# Load summarization model
print("🔄 Loading summarization model...")
try:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=0 if device == "cuda" else -1)
    print("✅ Summarization model loaded!")
except Exception as e:
    print(f"❌ Error loading summarization model: {e}")
    exit()

# Define file paths
audio_folder = "C:\\Users\\Mahdi1\\Desktop\\mov\\"
output_file = os.path.join(audio_folder, "full_transcript.txt")
summary_file = os.path.join(audio_folder, "summary.txt")
subtitle_file = os.path.join(audio_folder, "subtitle.srt")

# Clear previous files
for file in [output_file, summary_file, subtitle_file]:
    try:
        with open(file, "w", encoding="utf-8") as f:
            f.write("")
    except Exception as e:
        print(f"⚠️ Error resetting files: {e}")

# Ask user for source and target languages
source_lang = input("🎤 Enter audio language (e.g., en, ar, de): ").strip()
target_lang = input("🌍 Enter desired translation language (e.g., en, ar, fr): ").strip()

# Validate supported languages
try:
    translator = GoogleTranslator(source=source_lang, target=target_lang)
except Exception as e:
    print(f"❌ Translation error: {e}")
    exit()

# Verify audio file validity before processing
def check_audio_validity(audio_path):
    try:
        result = subprocess.run(
            ["ffmpeg", "-i", audio_path, "-af", "volumedetect", "-f", "null", "-"],
            capture_output=True, text=True
        )
        return "max_volume" in result.stderr
    except Exception as e:
        print(f"⚠️ Error checking audio file: {e}")
        return False

# Extract text from audio files
full_text = ""
subtitle_counter = 1
time_per_segment = 5  # seconds per segment

print("🔄 Extracting text from audio...")
for idx, file in enumerate(sorted(os.listdir(audio_folder))):
    if file.startswith("split_audio_") and file.endswith(".opus"):
        audio_path = os.path.join(audio_folder, file)

        if not check_audio_validity(audio_path):
            print(f"❌ {file} does not contain valid audio data, skipping.")
            continue

        print(f"🎧 Processing {file}...")

        try:
            result = model.transcribe(audio_path)
            extracted_text = result["text"]

            if extracted_text.strip():
                # Save raw transcript
                with open(output_file, "a", encoding="utf-8") as f:
                    f.write(f"\n--- {file} ---\n")
                    f.write(extracted_text + "\n")

                # Translate the text
                translated_text = translator.translate(extracted_text)

                # Determine subtitle timing
                start_time = idx * time_per_segment
                end_time = start_time + time_per_segment
                timestamp = f"00:{start_time // 60:02}:{start_time % 60:02},000 --> 00:{end_time // 60:02}:{end_time % 60:02},000"

                # Save subtitles with timing
                with open(subtitle_file, "a", encoding="utf-8") as f:
                    f.write(f"{subtitle_counter}\n")
                    f.write(f"{timestamp}\n")
                    f.write(translated_text + "\n\n")
                    subtitle_counter += 1

                # Accumulate full text
                full_text += extracted_text + " "

        except Exception as e:
            print(f"⚠️ Error processing file {file}: {e}")

print("✅ Text extraction and translation completed.")

# Summarize the extracted text
if len(full_text.split()) > 50:  # Ensure sufficient text for summarization
    print("🔄 Summarizing text...")
    try:
        summary = summarizer(full_text, max_length=200, min_length=50, do_sample=False)
        summarized_text = summary[0]["summary_text"]

        with open(summary_file, "w", encoding="utf-8") as f:
            f.write(summarized_text)

        print("✅ Summarization saved to summary.txt!")
    except Exception as e:
        print(f"⚠️ Error during summarization: {e}")
else:
    print("⚠️ Extracted text is too short for summarization!")

print("🎉 Text extraction, translation, and summarization complete!")
