"""Report basic technical measurements for integer PCM WAV files."""

import argparse
import math
from pathlib import Path
import sys
import wave


def inspect_wav(path):
    with wave.open(str(path), "rb") as audio:
        width = audio.getsampwidth()
        channels = audio.getnchannels()
        rate = audio.getframerate()
        expected_frames = audio.getnframes()
        full_scale = 1 << (width * 8 - 1)
        peak = 0
        rail_count = 0
        frames_read = 0
        while chunk := audio.readframes(8192):
            frame_bytes = width * channels
            if len(chunk) % frame_bytes:
                raise ValueError("incomplete PCM frame")
            frames_read += len(chunk) // frame_bytes
            for offset in range(0, len(chunk), width):
                if width == 1:
                    sample = chunk[offset] - 128
                else:
                    sample = int.from_bytes(
                        chunk[offset : offset + width], "little", signed=True
                    )
                peak = max(peak, abs(sample))
                rail_count += sample in (-full_scale, full_scale - 1)
        if frames_read != expected_frames:
            raise ValueError("WAV data is shorter than declared in the header")
        peak_db = f"{20 * math.log10(peak / full_scale):.2f}" if peak else "-inf"
        return (
            f"{path}: {frames_read / rate:.3f} s | {channels} ch | {rate} Hz | "
            f"{width * 8}-bit PCM | peak {peak_db} dBFS | "
            f"full-scale samples {rail_count}"
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wav_files", nargs="+", type=Path)
    args = parser.parse_args()
    status = 0
    for path in args.wav_files:
        try:
            print(inspect_wav(path))
        except (OSError, EOFError, ValueError, wave.Error) as error:
            print(f"{path}: {error or 'invalid WAV file'}", file=sys.stderr)
            status = 1
    return status


if __name__ == "__main__":
    raise SystemExit(main())
