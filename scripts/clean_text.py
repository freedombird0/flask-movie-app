import osimport chardet
import ftfy
import unicodedata
import re
import os

# 🔹 Set correct paths
base_folder = "C:\\Users\\Mahdi1\\Desktop\\mov"
input_file = os.path.join(base_folder, "output", "full_transcript.txt")  # Correct file
output_file = os.path.join(base_folder, "output", "cleaned_text.txt")

# 🔹 Ensure the input file exists
if not os.path.exists(input_file):
    print("❌ full_transcript.txt not found! Please run transcribe.py first.")
    exit()

print("🔄 Cleaning text...")

# 🔹 Attempt to automatically detect the file encoding
try:
    with open(input_file, "rb") as f:
        raw_data = f.read()
        detected_encoding = chardet.detect(raw_data)["encoding"]

    # If encoding is unknown, default to utf-8
    if detected_encoding is None:
        detected_encoding = "utf-8"

    print(f"✅ Detected encoding: {detected_encoding}")

    # 🔹 Read the text with the detected encoding
    with open(input_file, "r", encoding=detected_encoding, errors="ignore") as f:
        text = f.read().strip()

    # 🔹 Fix encoding issues using ftfy
    text = ftfy.fix_text(text)

except Exception as e:
    print(f"❌ Error while reading the file: {e}")
    exit()

# 🔹 Clean up the text from unusual characters
def clean_text(text):
    text = unicodedata.normalize("NFKC", text)  # Normalize text

    # 🔹 Remove any characters that are not Arabic, Latin, numbers, or basic punctuation
    text = re.sub(r'[^\w\s\u0600-\u06FF,.!?;:\-]', '', text)

    # 🔹 Remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()

# 🔹 Apply text cleaning
cleaned_text = clean_text(text)

# 🔹 Save the cleaned text to a new file
try:
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(cleaned_text)

    # 🔹 Print results
    print(f"✅ Text cleaned and saved to: {output_file}")
    print(f"📄 Word count after cleaning: {len(cleaned_text.split())}")

    # Display the first 200 words of cleaned text
    preview_text = " ".join(cleaned_text.split()[:200])
    print(f"\n📌 First 200 words after cleaning:\n{preview_text if preview_text else '🔴 Text is empty!'}")

except Exception as e:
    print(f"❌ Error while saving the file: {e}")
