"""
PDF to Audiobook Converter (no ffmpeg required)
-------------------------------------------------
Extracts text from a PDF and converts it to speech, saved as a WAV
audio file. Speed is controlled directly by the speech engine, so
there's no need for ffmpeg or any audio post-processing.

SETUP (run these once in your terminal):
    pip install pyttsx3 PyPDF2

USAGE:
    1. Put your PDF in the same folder as this script.
    2. Change PDF_FILENAME below to match your file's exact name.
    3. Run: python pdf_to_audiobook.py

The output WAV file plays in any media player (Windows Media Player,
VLC, etc.) just like an mp3 would.
"""

import os
import sys
import pyttsx3
from PyPDF2 import PdfReader

# ---------------------------------------------------------------
# SETTINGS — change these to fit your file
# ---------------------------------------------------------------
PDF_FILENAME = "comptia_core_2.pdf"      # <-- change to your PDF's name
OUTPUT_WAV = "comptia_audiobook.wav"     # final output file
SPEECH_RATE = 250                        # words per minute; ~200 is normal speaking speed,
                                          # so 340 is roughly 1.7x that
PREFERRED_VOICE_KEYWORDS = [             # script searches for these, in order, and uses
    "zira",                              # the first match it finds installed on your PC
    "hazel",
    "susan",
    "samantha",
    "victoria",
    "female",
    "woman",
]


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


def find_female_voice(voices, keywords):
    """
    Search installed voices for a name matching one of the preferred
    keywords. Returns the matching voice object, or None if nothing
    matched.
    """
    for keyword in keywords:
        for voice in voices:
            name = (voice.name or "").lower()
            voice_id = (voice.id or "").lower()
            if keyword in name or keyword in voice_id:
                return voice
    return None


def text_to_speech_file(text, wav_path, rate, keywords):
    """Convert text to speech at the given rate and save as WAV."""
    engine = pyttsx3.init()

    engine.setProperty("rate", rate)

    voices = engine.getProperty("voices")

    if voices:
        print("Available voices on this computer:")
        for v in voices:
            print(f"  - {v.name}")

        chosen_voice = find_female_voice(voices, keywords)

        if chosen_voice:
            engine.setProperty("voice", chosen_voice.id)
            print(f"Using voice: {chosen_voice.name}")
        else:
            # Fall back to the first available voice if no match found
            engine.setProperty("voice", voices[0].id)
            print("No female voice found by name — using default voice instead.")
            print("You can check the 'Available voices' list above and add")
            print("the exact name to PREFERRED_VOICE_KEYWORDS if one looks right.")
    else:
        print("Warning: no voices found on this system.")

    print(f"Converting text to speech at {rate} words per minute...")
    print("(this can take a while for long PDFs)")
    engine.save_to_file(text, wav_path)
    engine.runAndWait()
    print(f"Done! Audiobook saved as '{wav_path}'")


def main():
    text = extract_text_from_pdf(PDF_FILENAME)
    text_to_speech_file(text, OUTPUT_WAV, SPEECH_RATE, PREFERRED_VOICE_KEYWORDS)
    print("\nAll set. Open the WAV file in any media player to listen.")


if __name__ == "__main__":
    main()