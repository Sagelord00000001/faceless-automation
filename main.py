# import requests, os, time

# from flask import Flask
# app = Flask(__name__)

# @app.route('/')
# def home():
#     return "Server running..."

# # === STEP 1: Generate a short script from OpenRouter (DeepSeek or any model) ===
# def generate_script():
#     url = "https://openrouter.ai/api/v1/chat/completions"
#     headers = {"Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}"}
#     data = {
#         "model": "deepseek-chat",
#         "messages": [
#             {
#                 "role": "user",
#                 "content": "Write a 30-second motivational script for a faceless video."
#             }
#         ]
#     }
#     r = requests.post(url, headers=headers, json=data)
#     r.raise_for_status()
#     msg = r.json()["choices"][0]["message"]["content"]
#     print("\n✅ SCRIPT GENERATED:\n", msg)
#     return msg

# # === STEP 2: Fetch a free background clip from Pexels ===
# def get_video_url_pixabay():
#     url = "https://pixabay.com/api/videos/"
#     params = {
#         "key": os.getenv("PIXABAY_API_KEY"),
#         "q": "nature",          # or other keyword
#         "per_page": 1
#     }
#     r = requests.get(url, params=params)
#     r.raise_for_status()
#     result = r.json()
#     video_files = result["hits"][0]["videos"]
#     # pick one video file (e.g. first)
#     video_url = video_files[0]["url"]
#     return video_url

# # === STEP 3: Simulate caption or upload stage (to be replaced later) ===
# def upload_to_social(script_text, video_url):
#     print("\n🚀 Simulating upload to social media…")
#     print("Script:", script_text[:60], "…")
#     print("Video URL:", video_url)
#     time.sleep(2)
#     print("✅ Upload simulated successfully!")

# # === STEP 4: Combine the process ===
# def run():
#     try:
#         script = generate_script()
#         video_url = get_video_url()
#         upload_to_social(script, video_url)
#         print("\n✅ Workflow completed!")
#     except Exception as e:
#         print("❌ Error:", e)

# if __name__ == "__main__":
#     run()


# import os
# import time
# import requests
# from flask import Flask, jsonify

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return "Faceless video automation server running ✅"

# # === STEP 1: Generate a short script from OpenRouter ===
# def generate_script():
#     url = "https://openrouter.ai/api/v1/chat/completions"
#     headers = {
#         "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
#         "Content-Type": "application/json",
#     }
#     data = {
#         "model": "deepseek/deepseek-chat",
#         "messages": [
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": "Write a 15-second video caption about AI future."}
#         ]
#     }
#     print("🔹 Sending request to OpenRouter...")
#     response = requests.post(url, headers=headers, json=data)
#     print("🔹 Status:", response.status_code)
#     print("🔹 Response:", response.text)

#     response.raise_for_status()
#     res_json = response.json()
#     script = res_json["choices"][0]["message"]["content"]
#     return script

# # === STEP 2: Fetch a free background clip from Pixabay ===
# def get_video_url_pixabay():
#     url = "https://pixabay.com/api/videos/"
#     params = {
#         "key": os.getenv("PIXABAY_API_KEY"),
#         "q": "nature",
#         "per_page": 3
#     }
#     r = requests.get(url, params=params)
#     r.raise_for_status()
#     result = r.json()
#     if not result["hits"]:
#         raise Exception("No videos found!")
#     first_hit = result["hits"][0]
#     video_url = first_hit["videos"]["large"]["url"]
#     return video_url

# # === STEP 3: Simulate upload ===
# def upload_to_social(script_text, video_url):
#     print("\n🚀 Simulating upload...")
#     print("Script:", script_text[:80], "…")
#     print("Video URL:", video_url)
#     time.sleep(2)
#     print("✅ Upload simulated successfully!")

# # === STEP 4: Web-triggered automation ===
# @app.route('/run', methods=['GET'])
# def run_workflow():
#     try:
#         script = generate_script()
#         video_url = get_video_url_pixabay()
#         upload_to_social(script, video_url)
#         return jsonify({
#             "status": "success",
#             "script": script,
#             "video_url": video_url
#         })
#     except Exception as e:
#         print("❌ Error:", e)
#         return jsonify({"status": "error", "error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=10000)

import os
import random
import requests
import subprocess
from flask import Flask, jsonify
import imageio_ffmpeg as ffmpeg
from shlex import quote


ffmpeg_path = ffmpeg.get_ffmpeg_exe()
print("Using FFmpeg:", ffmpeg_path)


app = Flask(__name__)

# ========================
# ROUTES
# ========================
@app.route('/')
def home():
    return "🎬 Faceless Video Automation Server Running ✅ (GPT-5 powered!)"

@app.route('/run', methods=['GET'])
def run_workflow():
    try:
        # 1️⃣ Generate Script (GPT-5 DeepSeek)
        script_text = generate_script()
        print("\n💬 Script generated by GPT-5:\n", script_text)

        # 2️⃣ Get Pixabay Video
        video_urls = get_pixabay_videos()
        video_file = download_file(video_urls[0], "tmp/background.mp4")

        # 3️⃣ Pick local Mixkit Music
        music_file = get_local_music()

        # 4️⃣ Merge video + music + text overlay
        final_video = "tmp/final_video.mp4"
        generate_final_video(video_file, music_file, script_text, final_video)

        return jsonify({
            "status": "success",
            "script": script_text,
            "video_file": final_video
        })
    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"status": "error", "error": str(e)}), 500

# ========================
# FUNCTIONS
# ========================
def generate_script():
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}", "Content-Type": "application/json"}
    data = {
        "model": "deepseek/deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are GPT-5, a super-intelligent video script writer."},
            {"role": "user", "content": "Write a motivational 1-minute script about consistency, self-belief, and progress."}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    msg = response.json()["choices"][0]["message"]["content"].strip()
    return msg

def get_pixabay_videos():
    url = "https://pixabay.com/api/videos/"
    params = {"key": os.getenv("PIXABAY_API_KEY"), "q": "inspiration landscape", "per_page": 3}
    r = requests.get(url, params=params)
    r.raise_for_status()
    hits = r.json()["hits"]
    if not hits:
        raise Exception("No Pixabay videos found")
    return [hit["videos"]["medium"]["url"] for hit in hits]

def download_file(url, filename):
    os.makedirs("tmp", exist_ok=True)
    r = requests.get(url, stream=True)
    r.raise_for_status()
    with open(filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    return filename

def get_local_music():
    music_folder = "music"
    tracks = [f for f in os.listdir(music_folder) if f.endswith(".mp3")]
    if not tracks:
        raise Exception("No local Mixkit music found in /music")
    chosen = random.choice(tracks)
    return os.path.join(music_folder, chosen)

def generate_final_video(video_file, music_file, script_text, output_file):

    from shlex import quote

    # Extract a short, safe overlay (first line or title)
    first_line = script_text.split("\n")[0]
    short_text = first_line[:80]  # keep it short
    safe_text = short_text.replace("'", "’").replace('"', '').replace(':', '-').replace('*', '')
    
    vf_filter = f"scale=720:1280,drawtext=text={quote(safe_text)}:fontcolor=white:fontsize=32:x=(w-text_w)/2:y=h-th-60:box=1:boxcolor=black@0.5:boxborderw=5"

    # Ensure tmp folder exists
    os.makedirs("tmp", exist_ok=True)

    # FFmpeg command: scale to 720x1280, overlay text, add audio
    cmd = [
        ffmpeg_path,
        "-i", video_file,
        "-i", music_file,
        "-vf", vf_filter,
        "-c:a", "aac",
        "-shortest",
        output_file,
        "-y"
    ]
    print("\n🎥 Running FFmpeg to generate final video...")
    subprocess.run(cmd, check=True)
    print("✅ Final video created:", output_file)

# ========================
# MAIN
# ========================
if __name__ == "__main__":
    os.makedirs("tmp", exist_ok=True)
    app.run(host="0.0.0.0", port=10000)
