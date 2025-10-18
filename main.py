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
import time
import requests
import subprocess
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "🎬 Faceless Video Automation Server Running ✅"


# === STEP 1: Generate a 1-Minute Script ===
def generate_script():
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        raise Exception("❌ Missing OPENROUTER_API_KEY")

    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    data = {
        "model": "deepseek/deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a creative motivational writer."},
            {"role": "user", "content": "Write a motivational 1-minute script about consistency, self-belief, and progress."}
        ]
    }
    res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    res.raise_for_status()
    script = res.json()["choices"][0]["message"]["content"].strip()
    print("\n✅ SCRIPT GENERATED:\n", script)
    return script


# === STEP 2: Get Videos from Pixabay ===
def get_videos():
    key = os.getenv("PIXABAY_API_KEY")
    if not key:
        raise Exception("❌ Missing PIXABAY_API_KEY")

    res = requests.get("https://pixabay.com/api/videos/", params={"key": key, "q": "inspiration landscape", "per_page": 3})
    res.raise_for_status()
    hits = res.json()["hits"]
    if not hits:
        raise Exception("No videos found")

    return [hit["videos"]["medium"]["url"] for hit in hits]


# === STEP 3: Get Music ===
def get_music():
    key = os.getenv("PIXABAY_API_KEY")
    res = requests.get("https://pixabay.com/api/music/", params={"key": key, "q": "motivational", "per_page": 1})
    res.raise_for_status()
    hits = res.json()["hits"]
    if not hits:
        raise Exception("No music found")
    return hits[0]["audio"]


# === STEP 4: Download files ===
def download_file(url, filename):
    r = requests.get(url, stream=True)
    r.raise_for_status()
    with open(filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    return filename


# === STEP 5: Merge Videos + Music + Subtitles using FFmpeg ===
def create_final_video(script_text, video_urls, music_url):
    os.makedirs("tmp", exist_ok=True)

    # Download 1 background video (for free tier we use 1 to save CPU)
    video_path = download_file(video_urls[0], "tmp/background.mp4")
    music_path = download_file(music_url, "tmp/music.mp3")

    # Create text overlay file
    with open("tmp/script.txt", "w", encoding="utf-8") as f:
        f.write(script_text)

    # Output path
    output_path = "tmp/final_video.mp4"

    # FFmpeg command: overlay text + add music
    command = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", music_path,
        "-filter_complex",
        "[0:v]drawtext=textfile=tmp/script.txt:fontcolor=white:fontsize=24:x=(w-text_w)/2:y=h-100,format=yuv420p[v];[1:a]volume=0.4[a]",
        "-map", "[v]", "-map", "[a]",
        "-t", "60",  # 1 minute duration
        output_path
    ]

    subprocess.run(command, check=True)
    print("✅ Final video created:", output_path)
    return output_path


# === STEP 6: Main Workflow ===
@app.route('/run', methods=['GET'])
def run_all():
    try:
        script = generate_script()
        videos = get_videos()
        music = get_music()
        final_video = create_final_video(script, videos, music)
        return jsonify({
            "status": "success",
            "script": script,
            "final_video": final_video
        })
    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"status": "error", "error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
