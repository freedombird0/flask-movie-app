from PIL import Image

Create a black image with a resolution of 1280x720
image = Image.new("RGB", (1280, 720), (0, 0, 0)) image.save("C:\Users\Mahdi1\Desktop\mov\background.jpg")

print("✅ Image created successfully!")
