from deep_translator import GoogleTranslator, MyMemoryTranslator
import os
import textwrap

# 📂 Define file paths
base_folder = "C:\\Users\\Mahdi1\\Desktop\\mov"
input_file = os.path.join(base_folder, "output", "summary.txt")  # Summary file
output_file = os.path.join(base_folder, "output", "translated_text.txt")  # Translation file

# 🔍 Check if the summary file exists
if not os.path.exists(input_file):
    print("❌ summary.txt not found! Please run summarize.py first.")
    exit()

# 🏷️ Choose language and translator
target_lang = input("🌍 Enter the target language (e.g., en for English, ar for Arabic, fr for French): ").strip().lower()
translator_choice = input("🔄 Choose the translator [1] Google Translator (recommended) [2] MyMemory Translator: ").strip()

# 📝 Read text from the summary file
with open(input_file, "r", encoding="utf-8") as f:
    text_to_translate = f.read().strip()

# 🔍 Check if there’s text to translate
if not text_to_translate:
    print("⚠️ No text to translate!")
    exit()

print("🔄 Translating...")

# 🔹 Function to split long text into smaller chunks
def split_text(text, max_chars=500):
    return textwrap.wrap(text, max_chars)

# 📌 Perform the translation
try:
    translated_text = ""

    if translator_choice == "2":
        print("🟢 Using MyMemory Translator...")
        for chunk in split_text(text_to_translate):
            translated_text += MyMemoryTranslator(source="auto", target=target_lang).translate(chunk) + " "
    else:
        print("🟢 Using Google Translator...")
        for chunk in split_text(text_to_translate):
            translated_text += GoogleTranslator(source="auto", target=target_lang).translate(chunk) + " "

    # 📁 Save the translated text to the file
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(translated_text.strip())

    print(f"✅ Translation completed successfully and saved to {output_file}!")

except Exception as e:
    print(f"⚠️ Error during translation: {e}")

print("🎉 Translation process completed!")
