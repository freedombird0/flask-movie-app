import os
import chardet

# Specify the path of the folder containing text files
folder_path = "C:\\Users\\Mahdi1\\Desktop\\mov\\output"

# Check the encoding of each file in the folder and convert it to UTF-8 if needed
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)

    if os.path.isfile(file_path):  # ✅ Ensure it's a file, not a folder
        with open(file_path, "rb") as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding = result["encoding"]

        print(f"🔍 {filename} - Detected encoding: {encoding}")

        # Convert the file to UTF-8 if it’s not already in UTF-8
        if encoding and encoding.lower() not in ["utf-8", "utf-8-sig"]:
            try:
                with open(file_path, "r", encoding=encoding, errors="replace") as f:
                    content = f.read()

                # Save the file in UTF-8
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)

                print(f"✅ {filename} - Successfully converted to UTF-8!")
            except Exception as e:
                print(f"❌ Error converting {filename}: {e}")
