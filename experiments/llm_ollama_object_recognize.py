from vilib import Vilib
from pidog.tts import Piper
from pidog import Pidog

from pathlib import Path
import requests
import base64
import time

# --- CONFIGURATION ---
MAC_IP = "192.168.1.112"  # <--- CHANGE THIS TO YOUR MAC'S IP
MODEL = "moondream"
# ---------------------

tts = Piper()
dog = Pidog()
# Set a voice model (Piper)
tts.set_model("en_GB-southern_english_female-low")


def remote_recognize():
    # 1. Start Camera
    Vilib.camera_start(vflip=False)
    Vilib.display(local=False, web=True)
    time.sleep(2)  # Warm-up time

    # 2. Scanning Routine
    print("Scanning for object...")
    # Head move: [[yaw, roll, pitch]]
    dog.head_move([[0, 0, 0]], speed=80) 
    dog.wait_all_done()
    time.sleep(0.5)

    # 3. Take the photo
    directory = '/home/arkarkark/ollama_objects'
    filename = 'object_capture'
    photo_path = Path(directory) / f"{filename}.jpg"  # The / operator joins the strings
    Vilib.take_photo(photo_name=filename, path=directory)
    print(f"Photo captured to {photo_path}!")
    time.sleep(2)

    # 4. Prepare image for Mac
    with open(photo_path, "rb") as img:
        encoded_string = base64.b64encode(img.read()).decode('utf-8')

    # 5. Send to Ollama on Mac
    print(f"Talking to Mac at {MAC_IP}...")
    url = f"http://{MAC_IP}:11434/api/generate"
    payload = {
        "model": MODEL,
        "prompt": "What toy is in this image? Describe it in very simple terms, in four words or less.",
        "images": [encoded_string],
        "stream": False
    }

    try:
        response = requests.post(url, json=payload, timeout=60)
        data = response.json()
        description = data.get('response', 'something mysterious')

        # 6. Dog Speaks and Reacts
        print(f"Result: {description}")
        tts.say(f"I see {description}")

        # Happy wiggle
        dog.tail_move([[30], [-30], [30], [-30], [0]], speed=100)
        dog.wait_all_done()

    except Exception as e:
        print(f"Error: {e}")
        tts.say("I can't talk to my Mac brain right now.")

if __name__ == "__main__":
    try:
        remote_recognize()
    finally:
        # Clean up
        Vilib.camera_close()
        # dog.close() # Optional: keeps servos in place
