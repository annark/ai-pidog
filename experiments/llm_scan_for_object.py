from pathlib import Path
import time
import requests
import base64
from pidog import Pidog
from vilib import Vilib

# --- CONFIG ---
MAC_IP = "192.168.1.112"
script_dir = Path(__file__).parent.resolve()
target_dir = script_dir.parent / "ollama_objects"
target_dir.mkdir(parents=True, exist_ok=True)
filename = "scan_for_object_capture"
photo_path = target_dir / f"{filename}.jpg"

# Zones: Left, Center, Right (Head Yaw angles)
SCAN_ZONES = [-50, 0, 50]

my_dog = Pidog()
Vilib.camera_start()
time.sleep(2)

def check_for_item(item, current_yaw):
    """Takes a photo at the current angle and asks AI for [x, y]"""
    Vilib.take_photo(PHOTO_PATH)
    with open(PHOTO_PATH, "rb") as img:
        img_str = base64.b64encode(img.read()).decode('utf-8')

    # We ask Moondream to find the object and give coordinates
    prompt = f"Point to the {item}. Return ONLY coordinates as [x, y]. If not present, say 'none'."

    try:
        response = requests.post(
            f"http://{MAC_IP}:11434/api/generate",
            json={
                "model": "moondream",
                "prompt": prompt,
                "images": [img_str],
                "stream": False
            },
            timeout=30
        )
        res = response.json().get("response", "").lower()
        print(f"Zone {current_yaw}° AI Result: {res}")

        if "[" in res and "]" in res:
            coords = res.split("[")[1].split("]")[0].split(",")
            return float(coords[0]), float(coords[1])
    except Exception as e:
        print(f"Error calling AI: {e}")
    return None

def run_scanner():
    target = input("What item should I scan for? (e.g., white mug): ")
    found = False

    for yaw in SCAN_ZONES:
        print(f"🚀 Moving to zone: {yaw}°")
        my_dog.head_move([[yaw, 0, 0]], speed=60)
        my_dog.wait_head_done()
        time.sleep(1) # Let the camera settle

        coords = check_for_item(target, yaw)

        if coords:
            x, y = coords
            # Centering Math:
            # Current Yaw + (Offset from center of image)
            # x is 0.0 to 1.0. (x - 0.5) tells us how far from center.
            # 40 is roughly the FOV of the camera in degrees.
            final_yaw = yaw + ((x - 0.5) * -40)
            final_pitch = (y - 0.5) * -30

            print(f"🎯 Found at {x}, {y}! Centering...")
            my_dog.head_move([[final_yaw, 0, final_pitch]], speed=40)
            my_dog.wait_head_done()

            # Success wiggle!
            my_dog.do_action('wag_tail', step_count=3, speed=100)
            found = True
            break # Stop scanning once found

    if not found:
        print("🔍 Finished scan. Item not found.")
        my_dog.head_move([[0, 0, -45]], speed=30) # Look down
        my_dog.wait_head_done()

try:
    run_scanner()
finally:
    Vilib.camera_close()
