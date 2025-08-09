import requests
import os

API_URL = 'https://fastdl.app/api/convert'
SAVE_DIR = 'reels'
os.makedirs(SAVE_DIR, exist_ok=True)

def get_next_filename(base_dir, base_name="Reels", ext=".mp4"):
    i = 1
    while True:
        file_name = f"{base_name}{i}{ext}"
        full_path = os.path.join(base_dir, file_name)
        if not os.path.exists(full_path):
            return file_name
        i += 1

def download_video(insta_url, tokens):
    payload = tokens.copy()
    payload['url'] = insta_url
    headers = {
        "Content-Type": "application/json",
        "Referer": "https://fastdl.app/en",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    res = requests.post(API_URL, json=payload, headers=headers)
    res.raise_for_status()
    data = res.json()

    video_info_list = data.get('url')
    if not video_info_list or not isinstance(video_info_list, list):
        print(f"Download failed / No links: {insta_url}")
        print("Server response: ", data)
        return

    video_url = video_info_list[0].get('url')
    if not video_url:
        print(f"Download failed / No URL found: {insta_url}")
        print("Server response: ", data)
        return

    file_name = get_next_filename(SAVE_DIR, base_name="Reels", ext=".mp4")

    save_path = os.path.join(SAVE_DIR, file_name)

    print(f"{file_name} Download starting...")
    video_res = requests.get(video_url, stream=True)
    video_res.raise_for_status()

    with open(save_path, 'wb') as f:
        for chunk in video_res.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print(f"{file_name} Download success!")

def read_links_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    links = [link.strip() for link in content.split(',') if link.strip()]
    return links

if __name__ == "__main__":
    # tokens part is hard-coded
    tokens = {
        "ts": 1754757004017,
        "_ts": 1753864701452,
        "_tsc": 0,
        "_s": "6990555ce22283b10e94c3c5c51644cff8c4afb63852225343c3d935381b76c7"
    }
    links = read_links_from_file('links.txt')

    for link in links:
        try:
            download_video(link, tokens)
        except Exception as e:
            print(f"ERROR: {e}")
