# Italian Voice QA

A small evaluation kit for Italian text-to-speech, designed around the listening checks used in dialogue editing and audio post-production.

It includes an Italian prompt set, a listening rubric, a scoring sheet, and a Python utility for basic PCM WAV inspection.

## Run an evaluation

1. Pick four to six lines from [prompts.csv](prompts.csv). Generate the same lines with two voices or two settings, changing one variable at a time. Use the same export format. Keep the original files.
2. Give takes neutral IDs, such as P03-A and P03-B. Match perceived playback levels for listening and hide which voice or setting produced each take.
3. Listen once for the overall delivery, then listen again for specific issues. Score each take using the rubric and log timecodes, actual and expected readings, and the suggested fix in [scores.csv](scores.csv).
4. Inspect the original WAV exports with the command below. Use those results to guide a recheck by ear.

```sh
python3 wav_check.py P03-A.wav P03-B.wav
```

The script uses Python 3.10+ and the standard library. It accepts uncompressed integer PCM WAV files (8, 16, 24 or 32 bit) supported by Python's `wave` module. It reports duration, channels, sample rate, bit depth, sample peak in dBFS, and full-scale sample counts. A full-scale sample is a cue to inspect the audio. Loudness, true peak, and clipping diagnosis require other measurements or listening.

## Listening rubric

| Dimension | Listen for |
| --- | --- |
| Pronunciation | Stress, names, acronyms, numbers, and the chosen variety of Italian |
| Prosody | Pacing, pauses, emphasis, and whether intonation fits the sentence |
| Intelligibility | Words that are clear on first listen, including endings and consonants |
| Technical quality | Clicks, glitches, harsh sibilance, abrupt edits, and changes in timbre |

Score each dimension **1–5**. Use 5 for ready to use, 4 for a small audible issue, 3 for a distracting issue that needs a correction, 2 for repeated or meaning-changing problems, and 1 for an unusable take. Flag any change in meaning separately, even when the voice sounds natural. For a close call, record which take you prefer and the specific reason.

**Example finding (illustrative)** — P03-A, 00:02.1, pronunciation 2/5. The voice says “milleduecento” and drops the cents. Expected “milleduecento euro e cinquanta centesimi.” Spell out the amount, regenerate, and listen to the line in context.

The prompts are original sample material. The example is hypothetical. Add your own evaluation results as you test voices.
