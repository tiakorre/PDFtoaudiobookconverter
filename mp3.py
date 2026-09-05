"""
WAV to MP3 Converter (no ffmpeg required)
-------------------------------------------
Converts a WAV file to MP3 using lameenc, a pip-installable MP3
encoder. No ffmpeg or other separate program installs needed.

Built to handle very large WAV files safely: it reads and encodes
the audio in small chunks instead of loading the whole file into
memory at once.

SETUP (run this once in your terminal):
    pip install lameenc

USAGE:
    1. Put your WAV file in the same folder as this script.
    2. Change WAV_FILENAME below to match your file's exact name.
    3. Run: python mp3.py
"""

import os
import sys
import wave
import lameenc

# ---------------------------------------------------------------
# SETTINGS — change these to fit your file
# ---------------------------------------------------------------
WAV_FILENAME = "comptia_audiobook.wav"   # <-- change to your WAV file's name
OUTPUT_MP3 = "comptia_audiobook.mp3"     # output file name
MP3_QUALITY = 2                          # 0 = best quality/largest file, 9 = worst/smallest
MP3_BITRATE = 128                        # kbps; 128 is standard, 192/256 is higher quality
CHUNK_FRAMES = 1024 * 8                  # how many audio frames to process at a time


def convert_wav_to_mp3(wav_path, mp3_path, bitrate, quality, chunk_frames):
    if not os.path.exists(wav_path):
        print(f"Error: couldn't find '{wav_path}' in this folder.")
        print("Make sure the WAV file is in the same directory as this")
        print("script and that WAV_FILENAME matches the exact file name.")
        sys.exit(1)

    with wave.open(wav_path, "rb") as wav_file:
        channels = wav_file.getnchannels()
        sample_rate = wav_file.getframerate()
        sample_width = wav_file.getsampwidth()
        total_frames = wav_file.getnframes()

        if sample_width != 2:
            print("Error: this script only supports 16-bit WAV files.")
            print(f"'{wav_path}' uses {sample_width * 8}-bit samples.")
            print("Most text-to-speech and recording tools default to")
            print("16-bit, so re-exporting the WAV at that depth should fix it.")
            sys.exit(1)

        print(f"Input: {wav_path}")
        print(f"  Channels: {channels}")
        print(f"  Sample rate: {sample_rate} Hz")
        print(f"  Total frames: {total_frames}")

        encoder = lameenc.Encoder()
        encoder.set_bit_rate(bitrate)
        encoder.set_in_sample_rate(sample_rate)
        encoder.set_channels(channels)
        encoder.set_quality(quality)

        with open(mp3_path, "wb") as mp3_file:
            frames_done = 0
            last_percent_shown = -1

            while True:
                data = wav_file.readframes(chunk_frames)
                if not data:
                    break

                encoded = encoder.encode(data)
                if encoded:
                    mp3_file.write(encoded)

                frames_done += chunk_frames
                percent = min(100, int((frames_done / total_frames) * 100))
                if percent != last_percent_shown:
                    print(f"  Encoding... {percent}%", end="\r")
                    last_percent_shown = percent

            # Flush any remaining buffered audio
            leftover = encoder.flush()
            if leftover:
                mp3_file.write(leftover)

        print(f"\nDone! Saved as '{mp3_path}'")


def main():
    convert_wav_to_mp3(WAV_FILENAME, OUTPUT_MP3, MP3_BITRATE, MP3_QUALITY, CHUNK_FRAMES)


if __name__ == "__main__":
    main()