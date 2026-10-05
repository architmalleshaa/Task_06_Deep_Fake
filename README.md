# Task 6 Constructing and Evaluating Synthetic Media

**Synthetic-media disclosure:** Both MP3 files contain AI-written analysis read by stock computer-synthesized voices. No Syracuse coach or player is speaking. No real person's voice was cloned. The spoken opening, filenames and embedded title/comment fields identify the outputs as synthetic.

This experiment turns the validated Task 5 advisory analysis into two audio pipelines: a continuous single-voice reading and a segmented two-voice interview. The tools are macOS's installed speech service and local FFmpeg. The assignment permits accessible tools beyond its examples. This is a limited stock-TTS experiment; it is not a demonstration of a modern voice-cloning model or of vendor-specific deepfake safeguards.

## Artifacts and source

- `artifacts/AI_generated_synthetic_A_monologue.mp3` — Samantha voice, continuous reading, approximately 90.12 seconds.
- `artifacts/AI_generated_synthetic_B_interview.mp3` — Daniel question/disclosure segments and Samantha analyst segments, approximately 89.63 seconds.
- `source_script.txt` — exact 253-word spoken script, adapted from [Task 5's narrative](https://github.com/architmalleshaa/Task_05_Descriptive_Stats/blob/main/NARRATIVE.md).
- `process_log.json` and `PROCESS_LOG.md` — actual commands, settings, versions, generation times, and the failed restricted probe.
- `EVALUATION.md` — measured properties and explicit limits of perceptual assessment.
- [AUDIO_REVIEW.md](AUDIO_REVIEW.md) — two-model automated transcript comparison, recorded mismatches, and reproducible review code.
- `provenance_results.json` and `PROVENANCE.md` — metadata inspection and re-encoding experiment.

## Reproduce on macOS

```bash
python -m pip install -r requirements.txt
python generate_audio.py --output artifacts --work private_work
python check_provenance.py --scratch private_work/checks
```

The installed Samantha and Daniel stock voices are required. Other operating systems need a different speech engine and will not reproduce the same waveform. Voice-model builds are not exposed by the speech command; the observed OS and FFmpeg versions are recorded in the log. The source script is the exact text prompt; rate and voice settings are explicit. No paid service, subscription, student credit or external detector upload was used. Hashes verify the generated files, not a claim that future synthesis will be byte-identical.

## Main result

Both pipelines produced nonempty audio that decoded successfully, stayed within the task's two-minute target, and had zero full-scale clipped samples after decoding. Ordinary re-encoding with metadata removal dropped the embedded synthetic title/comment fields. The files were not cryptographically signed, and no validated AI-detection result is claimed. Perceptual listening review was unavailable; pronunciation, naturalness and the likelihood of fooling an audience remain unverified.

This work was generated and measured on 2026-10-05. Logged machine wall time is not a statement of the student's research hours. GitHub publication, email submission and time reporting are separate actions.
