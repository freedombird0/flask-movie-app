import os
import language_tool_python

# Load the grammar checking tool for the Arabic language
tool = language_tool_python.LanguageTool("ar")

# File paths (ensure they are correct according to your project structure)
base_folder = "C:\\Users\\Mahdi1\\Desktop\\mov\\output"  # The directory containing the text files
input_file = os.path.join(base_folder, "full_transcript.txt")
output_file = os.path.join(base_folder, "corrected_transcript.txt")

# Verify that the input file exists
if not os.path.exists(input_file):
    print(f"❌ The file full_transcript.txt was not found at the following path:\n{input_file}")
    print("🔹 Make sure to run transcribe.py first to generate the file.")
    exit()

# Read the extracted text
try:
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read().strip()  # Remove any unnecessary spaces
except Exception as e:
    print(f"⚠️ Error while reading the file: {e}")
    exit()

# Ensure the file is not empty
if not text:
    print("⚠️ The file full_transcript.txt is empty! Make sure that transcribe.py is functioning correctly.")
    exit()

print("🔄 Correcting grammar and language issues...")

# Correct grammatical errors
try:
    corrected_text = tool.correct(text)
except Exception as e:
    print(f"⚠️ Error while correcting the text: {e}")
    exit()

# Save the corrected text
try:
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(corrected_text)
    print(f"✅ Grammar corrections have been applied and saved to: {output_file}")
except Exception as e:
    print(f"⚠️ Error while saving the corrected file: {e}")

