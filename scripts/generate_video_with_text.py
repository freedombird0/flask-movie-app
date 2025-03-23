import os

# File paths
audio_path = "C:\\Users\\Mahdi1\\Desktop\\mov\\audio.wav"  # or use the new audio file
image_path = "C:\\Users\\Mahdi1\\Desktop\\mov\\background.jpg"
text_file = "C:\\Users\\Mahdi1\\Desktop\\mov\\full_transcript.txt"
output_video = "C:\\Users\\Mahdi1\\Desktop\\mov\\final_video_with_text.mp4"

# Read the text from the file
with open(text_file, "r", encoding="utf-8") as f:
    text_content = f.read().replace("\n", " ")  # Convert the text into a single line

# Construct ffmpeg command to add text overlay to the video
command = f'''
ffmpeg -loop 1 -i "{image_path}" -i "{audio_path}" -vf "drawtext=fontfile=/Windows/Fonts/arial.ttf:text='{text_content}':fontcolor=white:fontsize=30:x=(w-text_w)/2:y=h-100" -c:v libx264 -tune stillimage -c:a aac -b:a 192k -shortest "{output_video}"
'''

# Execute the command
os.system(command)

print("✅ Video with scrolling text successfully created!")
