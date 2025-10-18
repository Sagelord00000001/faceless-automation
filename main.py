import requests, os, time

# === STEP 1: Generate a short script from OpenRouter (DeepSeek or any model) ===
def generate_script():
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}"}
    data = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "user",
                "content": "Write a 30-second motivational script for a faceless video."
            }
        ]
    }
    r = requests.post(url, headers=headers, json=data)
    r.raise_for_status()
    msg = r.json()["choices"][0]["message"]["content"]
    print("\n✅ SCRIPT GENERATED:\n", msg)
    return msg

# === STEP 2: Fetch a free background clip from Pexels ===
def get_video_url_pixabay():
    url = "https://pixabay.com/api/videos/"
    params = {
        "key": os.getenv("PIXABAY_API_KEY"),
        "q": "nature",          # or other keyword
        "per_page": 1
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    result = r.json()
    video_files = result["hits"][0]["videos"]
    # pick one video file (e.g. first)
    video_url = video_files[0]["url"]
    return video_url

# === STEP 3: Simulate caption or upload stage (to be replaced later) ===
def upload_to_social(script_text, video_url):
    print("\n🚀 Simulating upload to social media…")
    print("Script:", script_text[:60], "…")
    print("Video URL:", video_url)
    time.sleep(2)
    print("✅ Upload simulated successfully!")

# === STEP 4: Combine the process ===
def run():
    try:
        script = generate_script()
        video_url = get_video_url()
        upload_to_social(script, video_url)
        print("\n✅ Workflow completed!")
    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    run()
