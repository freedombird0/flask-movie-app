import cv2
import os
import sys

# Get video path from command line argument
video_path = sys.argv[1]

# Ensure video file exists
if not os.path.exists(video_path):
    print(f"❌ Error: Video file '{video_path}' does not exist!")
    sys.exit()

# Create folder to save extracted frames
output_folder = "output/frames"
os.makedirs(output_folder, exist_ok=True)

# Open video with OpenCV
cap = cv2.VideoCapture(video_path)

# Check if the video was successfully loaded
if not cap.isOpened():
    print("❌ Error: Could not open video!")
    sys.exit()

# Get video properties
fps = cap.get(cv2.CAP_PROP_FPS)  # Frames per second
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Total number of frames
frame_interval = int(fps * 5) if fps > 0 else 30  # Capture one frame every 5 seconds (or every 30 frames if FPS is invalid)

print(f"🎥 Frame rate (FPS): {fps}")
print(f"🔢 Total frames: {total_frames}")
print(f"📸 Capturing one frame every {frame_interval} frames")

frame_count = 0
saved_frames = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break  # End of video

    if frame_count % frame_interval == 0:
        frame_filename = os.path.join(output_folder, f"frame_{saved_frames:04d}.jpg")
        cv2.imwrite(frame_filename, frame)
        saved_frames += 1

    frame_count += 1

# Release the video
cap.release()
print(f"✅ Extracted {saved_frames} images and saved them to '{output_folder}'")
