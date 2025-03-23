import re

# Path to the subtitle file
subtitle_file = "C:/Users/Mahdi1/Desktop/mov/subtitle.srt"

# List to store extracted timestamps
timestamps = []

# Read the file
with open(subtitle_file, "r", encoding="utf-8") as file:
    lines = file.readlines()
    for line in lines:
        match = re.match(r"(\d{2}):(\d{2}):(\d{2}),(\d{3})", line)
        if match:
            h, m, s, ms = map(int, match.groups())
            total_seconds = h * 3600 + m * 60 + s + ms / 1000
            timestamps.append(total_seconds)

# Print the extracted timestamps
print("📌 Extracted timestamps from the subtitle:")
for time in timestamps:
    print(time)
