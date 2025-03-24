import os
import subprocess
import whisper
import cv2
import time
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from deep_translator import GoogleTranslator
from google.cloud import texttospeech
from gtts import gTTS
import moviepy.editor as mp
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from yt_dlp import YoutubeDL

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
FRAMES_FOLDER = 'frames'
AUDIO_FOLDER = 'audio'
SUBTITLE_FOLDER = 'subtitles'

# Create directories if they do not exist
for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER, FRAMES_FOLDER, AUDIO_FOLDER, SUBTITLE_FOLDER]:
    os.makedirs(folder, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download_url', methods=['POST'])
def download_url():
    video_url = request.form['video_url']
    if not video_url:
        return "❌ Please enter a video URL!"

    ydl_opts = {
        'format': 'best[height<=720]+bestaudio/best',
        'outtmpl': os.path.join(UPLOAD_FOLDER, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4'
    }

    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, Upload=True)
        filename = ydl.prepare_filename(info_dict)
        filename = os.path.basename(filename).replace(".webm", ".mp4").replace(".mkv", ".mp4")

    return redirect(url_for('process_video', filename=filename))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "❌ No file was uploaded!"
    file = request.files['file']
    if file.filename == '':
        return "❌ No file was selected!"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    return redirect(url_for('process_video', filename=file.filename))

@app.route('/process/<filename>')
def process_video(filename):
    video_path = os.path.join(UPLOAD_FOLDER, filename)
    audio_path = os.path.join(AUDIO_FOLDER, f'{filename}_audio.wav')

    video = mp.VideoFileClip(video_path)
    if video.audio is None:
        return "❌ The video does not contain audio!"
    
    video.audio.write_audiofile(audio_path)
    model = whisper.load_model("base", download_root="models/")
    result = model.transcribe(audio_path)
    full_text = result["text"]

    text_file = os.path.join(OUTPUT_FOLDER, f'{filename}_transcript.txt')
    with open(text_file, "w", encoding="utf-8") as f:
        f.write(full_text)

    return render_template('transcript.html', text=full_text, filename=filename)

@app.route('/summarize/<filename>')
def summarize_text(filename):
    text_file = os.path.join(OUTPUT_FOLDER, f'{filename}_transcript.txt')
    summary_file = os.path.join(OUTPUT_FOLDER, f'{filename}_summary.txt')

    if not os.path.exists(text_file):
        return "❌ The text file is not found!"

    with open(text_file, "r", encoding="utf-8") as f:
        text = f.read()

    if len(text.split()) < 50:
        summary = text
    else:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        num_sentences = max(5, int(len(text.split()) * 0.2))
        summary_sentences = summarizer(parser.document, num_sentences)
        summary = " ".join(str(sentence) for sentence in summary_sentences)

    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(summary)

    return render_template('summary.html', summary=summary, filename=filename)

@app.route('/translate/<filename>', methods=['POST'])
def translate_text(filename):
    target_lang = request.form['language']
    summary_file = os.path.join(OUTPUT_FOLDER, f'{filename}_summary.txt')
    translated_file = os.path.join(OUTPUT_FOLDER, f'{filename}_translated.txt')

    if not os.path.exists(summary_file):
        return "❌ Summary file not found!"

    with open(summary_file, "r", encoding="utf-8") as f:
        text = f.read()

    max_chars = 4000
    text_parts = [text[i:i + max_chars] for i in range(0, len(text), max_chars)]
    translated_text = ""

    for part in text_parts:
        try:
            translated_part = GoogleTranslator(source="auto", target=target_lang).translate(part)
            translated_text += translated_part + "\n\n"
            time.sleep(1.5)
        except Exception as e:
            return f"❌ Translation error: {str(e)}"

    with open(translated_file, "w", encoding="utf-8") as f:
        f.write(translated_text.strip())

    return render_template('translate.html', translated_text=translated_text.strip(), filename=filename)

@app.route('/generate_audio/<filename>')
def generate_audio(filename):
    translated_file = os.path.join(OUTPUT_FOLDER, f'{filename}_translated.txt')
    audio_folder = AUDIO_FOLDER
    os.makedirs(audio_folder, exist_ok=True)

    if not os.path.exists(translated_file):
        return "❌ Translation file not found!"

    with open(translated_file, "r", encoding="utf-8") as f:
        text = f.read()

    client = texttospeech.TextToSpeechClient()
    max_bytes = 4000
    text_parts = []
    current_part = ""

    for sentence in text.split(". "):
        if len(current_part.encode("utf-8")) + len(sentence.encode("utf-8")) + 2 <= max_bytes:
            current_part += sentence + ". "
        else:
            text_parts.append(current_part.strip())
            current_part = sentence + ". "

    if current_part:
        text_parts.append(current_part.strip())

    audio_files = []

    for index, part in enumerate(text_parts):
        try:
            synthesis_input = texttospeech.SynthesisInput(text=part)
            voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
            audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

            response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

            output_file = os.path.join(audio_folder, f"{filename}_part{index}.mp3")
            with open(output_file, "wb") as out:
                out.write(response.audio_content)
                audio_files.append(output_file)
        except Exception as e:
            return f"❌ Error generating audio for part {index + 1}: {str(e)}"

    final_audio = os.path.join(audio_folder, f"{filename}_translated_audio.mp3")
    concat_list_path = os.path.join(audio_folder, "concat_list.txt")

    with open(concat_list_path, "w", encoding="utf-8") as f:
        for audio_file in audio_files:
            fixed_path = os.path.abspath(audio_file).replace("\\", "/")  # 🔥 FIXED
            f.write(f"file '{fixed_path}'\n")

    try:
        ffmpeg_cmd = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", concat_list_path, "-c", "copy", final_audio
        ]
        subprocess.run(ffmpeg_cmd, check=True)
    except subprocess.CalledProcessError as e:
        return f"❌ Failed to merge audio files: {str(e)}"

    return redirect(url_for('output_files', filename=os.path.basename(final_audio)))

@app.route('/output/<path:filename>')
def output_files(filename):
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    if os.path.exists(file_path):
        return send_from_directory(OUTPUT_FOLDER, filename)
    else:
        return "❌ The requested file could not be found!"

if __name__ == '__main__':
    app.run(debug=True)
