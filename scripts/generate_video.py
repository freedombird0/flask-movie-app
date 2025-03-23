import os
import cv2
import subprocess
import moviepy.editor as mp
import shlex  # To handle paths properly

# 📂 Set paths
base_folder = "C:\\Users\\Mahdi1\\Desktop\\mov"
upload_folder = os.path.join(base_folder, "uploads")
frames_folder = os.path.join(base_folder, "output", "frames")
audio_folder = os.path.join(base_folder, "audio")
subtitle_folder = os.path.join(base_folder, "output")
output_folder = os.path.join(base_folder, "output")

# ✅ Find the latest uploaded video
video_files = [f for f in os.listdir(upload_folder) if f.endswith(('.mp4', '.avi', '.mov', '.mkv'))]

if not video_files:
    print("❌ No video found in `uploads/`. Please upload a video first.")
    exit()

# 🔍 Select the most recent video by creation date
video_filename = sorted(video_files, key=lambda x: os.path.getctime(os.path.join(upload_folder, x)), reverse=True)[0]
video_path = os.path.join(upload_folder, video_filename)
base_name = os.path.splitext(video_filename)[0]

# ✅ Locate the correct audio file
audio_filename = f"{base_name}_translated_audio.mp3"
audio_path = os.path.join(audio_folder, audio_filename)

# 🛠️ Find the closest matching file in the folder
if not os.path.exists(audio_path):
    audio_files = [f for f in os.listdir(audio_folder) if f.endswith("_translated_audio.mp3")]
    for audio in audio_files:
        if base_name.lower() in audio.lower():
            audio_path = os.path.join(audio_folder, audio)
            print(f"🔄 Found matching audio file: {audio_path}")
            break
    else:
        print(f"❌ Audio file not found in {audio_folder}! Please run `generate_audio.py` first.")
        exit()

print(f"✅ Audio file found: {audio_path}")

# ✅ Locate the correct subtitle file
subtitle_file = os.path.join(subtitle_folder, f"{base_name}_fixed.srt")


# 🛠️ Find any available SRT file matching the video name
if not os.path.exists(subtitle_file):
    subtitle_files = [f for f in os.listdir(subtitle_folder) if f.endswith(".srt")]
    for sub in subtitle_files:
        if base_name.lower() in sub.lower():
            subtitle_file = os.path.join(subtitle_folder, sub)
            print(f"🔄 Found matching subtitle file: {subtitle_file}")
            break
    else:
        print(f"❌ Subtitle file not found in {subtitle_folder}! Please run `generate_subtitle.py` first.")
        exit()

print(f"✅ Subtitle file found: {subtitle_file}")

# 🎥 Extract frames from the video
print("📸 Extracting frames from the video...")

os.makedirs(frames_folder, exist_ok=True)
video = cv2.VideoCapture(video_path)
fps = video.get(cv2.CAP_PROP_FPS)
frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
frame_interval = max(1, int(fps * 2))

for i in range(0, frame_count, frame_interval):
    video.set(cv2.CAP_PROP_POS_FRAMES, i)
    success, frame = video.read()
    if success:
        frame_filename = os.path.join(frames_folder, f"{base_name}_frame_{i}.jpg")
        cv2.imwrite(frame_filename, frame)

video.release()

# 🔹 Create a new video from extracted frames
print("🎥 Creating a video from frames...")

images = sorted([img for img in os.listdir(frames_folder) if img.endswith(".jpg")])
if not images:
    print("❌ No images found to create the video!")
    exit()

first_image_path = os.path.join(frames_folder, images[0])
first_frame = cv2.imread(first_image_path)
frame_size = (first_frame.shape[1], first_frame.shape[0])

# 🔹 Calculate appropriate frame rate
audio_clip = mp.AudioFileClip(audio_path)
video_duration = audio_clip.duration
fps = max(1, len(images) / video_duration) if video_duration > 0 else 24

# 🔹 Create a temporary video using frames
output_temp_video = os.path.join(output_folder, f"{base_name}_temp.mp4")
video_writer = cv2.VideoWriter(output_temp_video, cv2.VideoWriter_fourcc(*'mp4v'), fps, frame_size)

for image in images:
    img_path = os.path.join(frames_folder, image)
    frame = cv2.imread(img_path)
    frame = cv2.resize(frame, frame_size)
    video_writer.write(frame)

video_writer.release()
print("✅ Test video created successfully!")

# 🔊 Merge audio with the video
final_video_with_audio = os.path.join(output_folder, f"{base_name}_final_with_audio.mp4")
print("🔊 Merging audio with the video...")

subprocess.run([
    "ffmpeg", "-y", "-i", output_temp_video, "-i", audio_path, 
    "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k", "-shortest", final_video_with_audio
])

# 🔠 **Add subtitles to the video (fixing the issue)**
final_video_with_subtitles = os.path.join(output_folder, f"{base_name}_final_with_subtitles.mp4")
print("📝 Adding subtitles...")

# ✅ **Fix the issue by ensuring proper path handling**
subtitle_file_ffmpeg = os.path.abspath(subtitle_file).replace("\\", "/")  # Replace \ with /
subtitle_file_ffmpeg = shlex.quote(subtitle_file_ffmpeg)  # Secure the path to handle spaces

# ✅ **Pass the path to ffmpeg properly**
subprocess.run([
    "ffmpeg", "-y", "-i", final_video_with_audio, "-vf", f"subtitles={subtitle_file_ffmpeg}", 
    "-c:a", "copy", final_video_with_subtitles
])

# 🗑️ Clean up temporary files
if os.path.exists(output_temp_video):
    os.remove(output_temp_video)

print("🎉 ✅ Final video creation completed successfully!")
print(f"📢 Final video saved at: {final_video_with_subtitles}")
