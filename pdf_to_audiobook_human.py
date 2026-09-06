"""
PDF to Audiobook Converter (natural neural voice, via edge-tts)
------------------------------------------------------------------
Extracts text from a PDF and converts it to speech using Microsoft's
neural text-to-speech voices (the same engine behind Azure TTS).
This sounds far more natural than pyttsx3's robotic default voice,
and it outputs mp3 directly — no ffmpeg, no wav conversion, no
separate encoding step needed.

SETUP (run this once in your terminal):
    pip install edge-tts PyPDF2

USAGE:
    1. Put your PDF in the same folder as this script.
    2. Change PDF_FILENAME below to match your file's exact name.
    3. Run: python pdf_to_audiobook.py

Requires an internet connection — edge-tts streams the audio from
Microsoft's service, it isn't generated fully offline.
"""

import os
import sys
import asyncio
import edge_tts
from PyPDF2 import PdfReader

# ---------------------------------------------------------------
# SETTINGS — change these to fit your file
# ---------------------------------------------------------------
PDF_FILENAME = "comptia_core_2.pdf"      # <-- change to your PDF's name
OUTPUT_MP3 = "comptia_audiobook_human.mp3"     # final output file

# A few natural-sounding female voice options — uncomment the one you want,
# or try others from the full list (see the note printed at the bottom)
VOICE = "en-US-JennyNeural"              # warm, natural, general-purpose
# VOICE = "en-US-AriaNeural"             # clear, confident, slightly more formal
# VOICE = "en-US-MichelleNeural"         # calm, even pacing
# VOICE = "en-US-AnaNeural"              # younger-sounding

SPEECH_RATE = "+60%"                     # edge-tts speed as a percent change from normal
                                          # "+70%" is roughly 1.7x, "+0%" is normal speed,
                                          # "-20%" would be slower than normal


def extract_text_from_pdf(pdf_path):
    """Pull all readable text out of the PDF, page by page."""
    if not os.path.exists(pdf_path):
        print(f"Error: couldn't find '{pdf_path}' in this folder.")
        print("Make sure the PDF is in the same directory as this script")
        print("and that PDF_FILENAME matches the exact file name.")
        sys.exit(1)

    reader = PdfReader(pdf_path)
    full_text = []

    print(f"Reading {len(reader.pages)} pages from '{pdf_path}'...")

    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if text:
            full_text.append(text)
        if i % 10 == 0 or i == len(reader.pages):
            print(f"  ...processed {i}/{len(reader.pages)} pages")

    combined = "\n".join(full_text).strip()

    if not combined:
        print("Warning: no text could be extracted. This PDF may be a")
        print("scanned image rather than real text, which this script")
        print("can't read directly (it would need OCR instead).")
        sys.exit(1)

    return combined


async def text_to_speech_file(text, mp3_path, voice, rate):
    """Convert text to speech using edge-tts and save as mp3."""
    print(f"Using voice: {voice}")
    print(f"Speed adjustment: {rate}")
    print("Converting text to speech...")
    print("(this can take a while for long PDFs, and needs an internet connection)")

    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(mp3_path)

    print(f"Done! Audiobook saved as '{mp3_path}'")


def main():
    text = extract_text_from_pdf(PDF_FILENAME)
    asyncio.run(text_to_speech_file(text, OUTPUT_MP3, VOICE, SPEECH_RATE))
    print("\nAll set. Open the mp3 file in any media player to listen.")
    print("\nWant to hear other voice options first? Run this in your")
    print("terminal to see the full list edge-tts supports:")
    print("    edge-tts --list-voices")


if __name__ == "__main__":
    main()
