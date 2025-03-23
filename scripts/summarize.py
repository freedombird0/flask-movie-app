import os
import torch
from transformers import pipeline

# Verify the correct processing unit is being used
device = "cuda" if torch.cuda.is_available() else "cpu"
device_id = 0 if device == "cuda" else -1
print(f"✅ Using device: {device.upper()} (device_id={device_id})")

# Load the summarization model
try:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=device_id)
except Exception as e:
    print(f"❌ Error loading summarization model: {e}")
    exit()

# 🔹 Define paths
base_folder = "C:\\Users\\Mahdi1\\Desktop\\mov"
input_file = os.path.join(base_folder, "output", "cleaned_text.txt")  # Clean text file
output_file = os.path.join(base_folder, "output", "summary.txt")

# 🔹 Verify that the correct file exists
if not os.path.exists(input_file):
    print("❌ File cleaned_text.txt is missing! Make sure to run clean_text.py first.")
    exit()

# 🔹 Read the text from the file
with open(input_file, "r", encoding="utf-8") as f:
    text = f.read().strip()

# 🔹 Check if the text is empty
if not text or len(text.split()) < 50:  
    print("❌ The file is empty or the text is too short! Nothing to summarize.")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("⚠️ Insufficient content to summarize.\n")
    exit()

print("🔄 Summarizing text...")

# 🔹 Function to split text into smaller chunks for the model
def chunk_text(text, max_tokens=400):
    words = text.split()
    chunks = [" ".join(words[i:i+max_tokens]) for i in range(0, len(words), max_tokens)]
    return [chunk for chunk in chunks if len(chunk.split()) > 40]  # Avoid empty or too-small chunks

# 🔹 Split the text into chunks suitable for summarization
chunks = chunk_text(text)

# 🔹 Ensure there is content after splitting
if not chunks:
    print("❌ Error: No sufficient text chunks found after splitting.")
    exit()

print(f"🔹 Text split into {len(chunks)} chunk(s)")

# 🔹 Use batched processing
batch_size = min(2, len(chunks))  # Process in batches
summarized_text = ""

for i in range(0, len(chunks), batch_size):
    batch = chunks[i:i+batch_size]

    # Verify that each batch has enough data
    if not all(batch) or any(len(chunk.strip()) < 40 for chunk in batch):
        print(f"⚠️ Skipping empty or too-short batch {i//batch_size + 1}")
        continue

    print(f"🔹 Processing batch {i//batch_size + 1} of {len(chunks)//batch_size + 1}...")

    try:
        summaries = summarizer(
            batch, 
            max_length=120,  # Maximum words in each summary
            min_length=50,   # Minimum words
            do_sample=False
        )
        summarized_text += "\n".join([s["summary_text"] for s in summaries]) + "\n"

    except Exception as e:
        print(f"⚠️ Error summarizing batch {i//batch_size + 1}: {e}")
        summarized_text += "[⚠️ Summarization error]\n"

# 🔹 Save the summary
with open(output_file, "w", encoding="utf-8") as f:
    f.write(summarized_text.strip())

print(f"✅ Summary saved to: {output_file}")
print(f"📄 Word count in summary: {len(summarized_text.split())}")

# 🔹 Display the first 100 words of the summary for verification
preview_text = " ".join(summarized_text.split()[:100])
print(f"\n📌 First 100 words of summary:\n{preview_text if preview_text else '🔴 Summarization failed!'}")
