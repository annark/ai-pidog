# 🐶 PiDog AI: Object Recognition & Search
This repository contains experimental scripts for the SunFounder PiDog 2, integrating local AI processing via Ollama on a Mac to give the robot "eyes" and decision-making capabilities.

## 🌟 Overview
The project currently features two main experiments:

Object Recognition: The dog captures an image, sends it to a Mac running moondream, and receives a description of what it sees.

Object Search: A loop where the dog rotates its head, looks for a specific object (like a "white mug"), and stops once the AI confirms it has been found.


## Hardware Requirements
- Raspberry Pi 5 (mounted on PiDog)
- [SunFounder PiDog Robot Kit](https://sunfounder.com)
- Mac or PC (connected to the same Wi-Fi, running Ollama as the AI server)

## 🚀 Setup & Installation
### 1. PiDog Environment
Ensure you have the official SunFounder libraries installed on your Pi by following the official [SunFounder Quick Guide](https://docs.sunfounder.com/projects/pidog/en/latest/python/python_start/quick_guide_on_python.html).

### 2. Local Ollama AI Server
- Download the [Ollama App](https://ollama.com/).
- Pull the vision model: `ollama pull moondream`
- Expose the server to your local network so the Pi can reach it:
`OLLAMA_ORIGINS="*" OLLAMA_HOST=0.0.0.0 ollama serve`

### 3. Repository Setup
Clone this repository to your Pi and install the Python dependencies:
```
git clone https://github.com/annark/ai-pidog.git
cd ai-pidog
pip install -r requirements.txt
```
Configuration Tip: Open your scripts and update the MAC_IP variable to match the local IP address of your Mac (e.g., 192.168.1.XX).

## Usage
### Running Object Recognition
This script captures one frame from the Pi camera and prints the AI's description to the terminal.
```
sudo python3 llm_ollama_object_recognize.py
```

### Running Object Search
The dog will scan its environment by moving its head. Once the AI identifies the target object, the dog will stop scanning.
```
sudo python3 llm_ollama_search_for_object.py
```

## Project Structure & customizations
- `llm_ollama_object_recognize.py`: Basic vision-to-text script.
- `llm_ollama_search_for_object.py`: Search loop and head-movement logic.
- `.gitignore`: Prevents captured .jpg files from cluttering the repo.
- `requirements.txt`: Necessary Python dependencies.

Developed by [annark](https://github.com/annark)
