"""
MP3 File Partitioner
----------------------
Splits a large MP3 file into smaller numbered parts, so it's easier
to upload/download (e.g. to Google Drive) without one huge transfer.

This does NOT re-encode the audio — it just cuts the raw file into
pieces. The parts are not individually playable as mp3s on their
own; they're meant to be reassembled back into the original file
later (see the note at the bottom of this script for how).

No extra installs needed — this only uses Python's built-in tools.

USAGE:
    1. Put your MP3 file in the same folder as this script.
    2. Change INPUT_FILE below to match your file's exact name.
    3. Change OUTPUT_NAME_BASE to whatever you want the parts called
       (e.g. "core 2" will produce "core 2_1.mp3", "core 2_2.mp3", etc.)
    4. Adjust MAX_PART_SIZE_MB if needed.
    5. Run: python mp3_partition.py
"""

import os
import sys

# ---------------------------------------------------------------
# SETTINGS — change these to fit your file
# ---------------------------------------------------------------
INPUT_FILE = "comptia_audiobook.mp3"   # <-- change to your mp3's exact name
OUTPUT_NAME_BASE = "core 2"            # <-- parts will be named "core 2_1.mp3", "core 2_2.mp3", etc.
MAX_PART_SIZE_MB = 25                  # maximum size of each part, in MEGABYTES
READ_BUFFER_BYTES = 1024 * 1024        # 1 MB read chunks while copying (keeps memory usage low)


def split_file(input_path, output_base, max_part_size_mb, read_buffer):
    if not os.path.exists(input_path):
        print(f"Error: couldn't find '{input_path}' in this folder.")
        print("Make sure the file is in the same directory as this script")
        print("and that INPUT_FILE matches the exact file name.")
        sys.exit(1)

    max_part_bytes = max_part_size_mb * 1024 * 1024
    total_size = os.path.getsize(input_path)
    estimated_parts = -(-total_size // max_part_bytes)  # ceiling division

    print(f"Input file: {input_path}")
    print(f"Total size: {total_size / (1024 * 1024):.2f} MB")
    print(f"Max part size: {max_part_size_mb} MB")
    print(f"Expected number of parts: {estimated_parts}")
    print()

    part_num = 1
    bytes_written_total = 0

    with open(input_path, "rb") as infile:
        while True:
            part_filename = f"{output_base}_{part_num}.mp3"
            bytes_written_this_part = 0

            with open(part_filename, "wb") as outfile:
                while bytes_written_this_part < max_part_bytes:
                    remaining_in_part = max_part_bytes - bytes_written_this_part
                    to_read = min(read_buffer, remaining_in_part)
                    chunk = infile.read(to_read)

                    if not chunk:
                        break

                    outfile.write(chunk)
                    bytes_written_this_part += len(chunk)
                    bytes_written_total += len(chunk)

            if bytes_written_this_part == 0:
                # Nothing was written this round, so remove the empty file
                os.remove(part_filename)
                break

            part_size_mb = bytes_written_this_part / (1024 * 1024)
            print(f"  Created '{part_filename}' ({part_size_mb:.2f} MB)")

            if bytes_written_total >= total_size:
                break

            part_num += 1

    total_parts = part_num
    print()
    print(f"Done! Split into {total_parts} parts.")
    print()
    print("To reassemble the original file later, the parts need to be")
    print("combined in order (part 1, then 2, then 3, etc.) with a")
    print("straight binary concatenation. Let me know if you'd like a")
    print("matching 'rejoin' script for when you're ready to put it")
    print("back together.")


def main():
    split_file(INPUT_FILE, OUTPUT_NAME_BASE, MAX_PART_SIZE_MB, READ_BUFFER_BYTES)


if __name__ == "__main__":
    main()