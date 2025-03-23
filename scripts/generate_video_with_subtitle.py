import os

# Set correct paths
audio_path = "C:\\Users\\Mahdi1\\Desktop\\mov\\audio.wav"
image_path = "C:\\Users\\Mahdi1\\Desktop\\mov\\background.jpg"
subtitle_file = "C:\\Users\\Mahdi1\\Desktop\\mov\\subtitle.srt"
output_video = "C:\\Users\\Mahdi1\\Desktop\\mov\\final_video_with_subtitles.mp4"

# Format the subtitle path correctly
formatted_subtitle_path = f"'C\\:\\Users\\Mahdi1\\Desktop\\mov\\subtitle.srt'"

# ffmpeg command with correct formatting
command = f'''
ffmpeg -loop 1 -i "{image_path}" -i "{audio_path}" -vf subtitles={formatted_subtitle_path} -c:v libx264 -tune stillimage -c:a aac -b:a 192k -shortest "{output_video}"
'''

# Run the command
os.system(command)

print("✅ Video with subtitles successfully created!")
