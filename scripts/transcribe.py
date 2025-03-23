import os
import whisper
from deep_translator import GoogleTranslator

# Load Whisper model
model = whisper.load_model("base")

# Allow user to specify the source audio language
source_language = input("🌍 Enter the source language (e.g., 'ar' for Arabic, 'en' for English, 'fr' for French) or leave it blank for auto-detection: ").strip()
translate_to = input("🔄 Enter the language you want to translate to (e.g., 'ar', 'en', 'fr') or leave it blank for no translation: ").strip()

# Define file paths
audio_folder = "audio"
output_file = "output/full_transcript.txt"
translated_file = "output/translated_text.txt"

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)

print("🔄 Extracting text from audio files...")
full_text = ""

# Ensure there are audio files in the folder
audio_files = [f for f in sorted(os.listdir(audio_folder)) if f.endswith((".mp3", ".wav", ".m4a"))]

for file in audio_files:
    audio_path = os.path.join(audio_folder, file)
    print(f"🎧 Processing file: {file}")
    
    try:
        # Transcribe audio to text, allowing for language specification
        result = model.transcribe(audio_path, language=source_language if source_language else None)
        extracted_text = result["text"]
        
        # Save the text to the file
        with open(output_file, "a", encoding="utf-8") as f:
            f.write(f"\n--- {file} ---\n")
            f.write(extracted_text + "\n")
        
        full_text += extracted_text + " "
        
    except Exception as e:
        print(f"❌ Error processing file {file}: {e}")

print("✅ Text has been extracted and saved in full_transcript.txt!")

# Translate text if requested
if translate_to:
    print("🔄 Translating text...")
    translated_text = GoogleTranslator(source='auto', target=translate_to).translate(full_text)
    
    with open(translated_file, "w", encoding="utf-8") as f:
        f.write(translated_text)
    
    print(f"✅ Translation completed and saved in {translated_file}!")
else:
    print("⚠️ No translation language specified; text extraction only.")
