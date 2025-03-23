import sys
import os
import moviepy.editor as mp

# Get video path from command line arguments
video_path = sys.argv[1]
audio_output = "audio/output_audio.wav"

# Ensure the audio directory exists
os.makedirs(os.path.dirname(audio_output), exist_ok=True)

# Extract audio from the video
clip = mp.VideoFileClip(video_path)
clip.audio.write_audiofile(audio_output)

print(f"✅ Audio successfully extracted to file: {audio_output}")
