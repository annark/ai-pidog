import base64
import time
import requests
from pathlib import Path
from pidog import Pidog
from pidog.tts import Piper
from vilib import Vilib

# --- CONFIGURATION ---
MAC_IP = "192.168.1.112"
MODEL = "moondream"
TARGET_OBJECT = "white doll"  # <-- Change this to what you want to find!
# ---------------------

dog = Pidog()
tts = Piper()
tts.set_model("en_US-amy-low")

def search_for_object():
    Vilib.camera_start(vflip=False)
    Vilib.display(local=False, web=True)

    # Starting position: Head centered
    current_yaw = 0
    dog.head_move([[current_yaw, 0, 0]], speed=80)
    dog.wait_all_done()

    found = False

    # Search from -90 degrees (left) to 90 degrees (right) in steps
    for angle in range(-90, 91, 30):
        print(f"Checking angle: {angle}...")
        dog.head_move([[angle, 0, 0]], speed=60)
        dog.wait_all_done()
        time.sleep(1) # Let the camera settle

        # Take and process photo
        directory = '/home/arkarkark/ollama_objects'
        filename = 'search_capture'
        photo_path = Path(directory) / f"{filename}.jpg"
        Vilib.take_photo(photo_name=filename, path=directory)

        with open(photo_path, "rb") as img:
            encoded = base64.b64encode(img.read()).decode('utf-8')

        # Ask Mac
        url = f"http://{MAC_IP}:11434/api/generate"
        prompt = f"Is there a {TARGET_OBJECT} in this image? Answer only 'yes' or 'no'."

        try:
            response = requests.post(url, json={
                "model": MODEL,
                "prompt": prompt,
                "images": [encoded],
                "stream": False
            }, timeout=30)

            result = response.json().get('response', '').lower().strip()
            print(f"Mac says: {result}")

            if "yes" in result:
                found = True
                tts.say(f"I found the {TARGET_OBJECT}!")
                # Happy Wiggle
                dog.tail_move([[30], [-30], [30], [-30], [0]], speed=100)
                dog.wait_all_done()
                break 
            else:
                print("Not here, moving on...")

        except Exception as e:
            print(f"Error: {e}")

    if not found:
        tts.say(f"I could not find the {TARGET_OBJECT}.")
        dog.head_move([[0, 0, 0]], speed=50)

if __name__ == "__main__":
    try:
        search_for_object()
    finally:
        Vilib.camera_close()
