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


import os
import time
import requests
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Faceless video automation server running ✅"

# === STEP 1: Generate a short script from OpenRouter ===
def generate_script():
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "deepseek/deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Write a 15-second video caption about AI future."}
        ]
    }
    print("🔹 Sending request to OpenRouter...")
    response = requests.post(url, headers=headers, json=data)
    print("🔹 Status:", response.status_code)
    print("🔹 Response:", response.text)

    response.raise_for_status()
    res_json = response.json()
    script = res_json["choices"][0]["message"]["content"]
    return script

# === STEP 2: Fetch a free background clip from Pixabay ===
def get_video_url_pixabay():
    url = "https://pixabay.com/api/videos/"
    params = {
        "key": os.getenv("PIXABAY_API_KEY"),
        "q": "nature",
        "per_page": 3
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    result = r.json()
    if not result["hits"]:
        raise Exception("No videos found!")
    first_hit = result["hits"][0]
    video_url = first_hit["videos"]["large"]["url"]
    return video_url

# === STEP 3: Simulate upload ===
def upload_to_social(script_text, video_url):
    print("\n🚀 Simulating upload...")
    print("Script:", script_text[:80], "…")
    print("Video URL:", video_url)
    time.sleep(2)
    print("✅ Upload simulated successfully!")

# === STEP 4: Web-triggered automation ===
@app.route('/run', methods=['GET'])
def run_workflow():
    try:
        script = generate_script()
        video_url = get_video_url_pixabay()
        upload_to_social(script, video_url)
        return jsonify({
            "status": "success",
            "script": script,
            "video_url": video_url
        })
    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"status": "error", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
