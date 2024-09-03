import pyperclip
import concurrent.futures
import edge_tts
from datetime import datetime
import os
import subprocess
import keyboard

running = False

def fetch_audio(text):
    audio_buffer = bytearray()
    connection = edge_tts.Communicate(text)
    for chunk in connection.stream_sync():
        if chunk["type"] == "audio":
            audio_buffer.extend(chunk["data"])
    return audio_buffer


def main():
    global running
    running = True
    copied_text = pyperclip.paste()
    split_text = copied_text.split(".")
    print("runs")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_audio, line.strip()) for line in split_text if line.strip()]
        audio_parts = [future.result() for future in futures]

    combined_audio = b''.join(audio_parts)
    current_time = datetime.now().strftime("%H_%M_%S")
    audio_name = f"D:/audioRecordings/{current_time}.mp3"
    if not os.path.exists("D:/audioRecordings"):
        os.mkdir("D:/audioRecordings")
    print("runs3")
    with open(f"D:/audioRecordings/{current_time}.mp3", "wb") as audio_file:
        audio_file.write(combined_audio)
    subprocess.run(["start", audio_name], shell=True, check=True)
    running = False

keyboard.add_hotkey("alt+p", lambda: main() if not running else None)

keyboard.wait("alt+p+esc")
