import pyperclip
import concurrent.futures
import edge_tts
from datetime import datetime
import os
import subprocess
import keyboard

def fetch_audio(text):
    try:
        audio_buffer = bytearray()
        connection = edge_tts.Communicate(text)
        for chunk in connection.stream_sync():
            if chunk["type"] == "audio":
                audio_buffer.extend(chunk["data"])
        return audio_buffer
    except Exception as e:
        print(f"Error in fetch_audio: {e}")
        return None

def main():
    print("runs1")
    try:
        copied_text = pyperclip.paste()
        print(f"Copied text: {copied_text}")  # Debug: print the copied text
        split_text = copied_text.split(".")
        print(f"Split text: {split_text}")  # Debug: print the split text

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(fetch_audio, line.strip()) for line in split_text if line.strip()]
            audio_parts = [future.result() for future in futures if future.result() is not None]
        print("runs2")

        combined_audio = b''.join(audio_parts)
        current_time = datetime.now().strftime("%H_%M_%S")
        audio_name = f"D:/audioRecordings/{current_time}.mp3"
        if not os.path.exists("D:/audioRecordings"):
            os.mkdir("D:/audioRecordings")
        print("runs3")

        with open(audio_name, "wb") as audio_file:
            audio_file.write(combined_audio)
        subprocess.run(["start", audio_name], shell=True, check=True)
    except Exception as e:
        print(f"Error in main: {e}")

keyboard.add_hotkey("alt+p", lambda: main())
keyboard.wait("alt+p+esc")
