# Automated audio transcript review

Two local speech-recognition models transcribed each original MP3 without receiving the source script, player names, or expected answers as prompts. The reference script was used only after transcription to measure agreement. These are machine-recognition results, not a human listening or realism assessment.

## Results

| Model | Recording | Reference tokens | Edit distance | Word error rate |
|---|---|---:|---:|---:|
| base.en | A: monologue | 258 | 12 | 4.65% |
| base.en | B: interview | 258 | 11 | 4.26% |
| small.en | A: monologue | 258 | 4 | 1.55% |
| small.en | B: interview | 258 | 2 | 0.78% |

The denominator is 258 tokens after splitting punctuation and hyphenated words; the original 253-word count used whitespace-delimited words. Number formatting, percent signs and apostrophes are normalized transparently in `review_audio.py`; proper names are not silently corrected. Raw transcripts, raw comparison scores, normalized edits, segment times, model revisions and audio hashes are retained in `audio_review/`.

## Supported observations

Both models recovered the opening synthetic-media disclosure, the sixteen-of-twenty-two record, the distinction between adding one and two goals, the four-and-a-half headroom figure, and the final causal limitation. The larger `small.en` model recovered the word “offense” where `base.en` transcribed “a fence.” This model disagreement illustrates why an ASR mismatch is not proof of an audible defect.

Both small-model transcripts spelled Payton as “Peyton” and Tyrrell as “Tiro.” The monologue transcript also spelled a later Rowley mention as “Raleigh” and omitted “if” before the fixed-score scenario. Proper-name spelling differences can be recognition errors or homophones rather than incorrect pronunciation. A listener is still needed to determine what the audio actually sounds like.

The larger model yielded fewer recognition edits on both recordings. This is evidence about recognition under these settings, not a controlled measurement of which audio is more natural, convincing, or preferable to listeners. Both models belong to the Whisper family, and this is one run per model and recording.

## Reproduce

```bash
python -m pip install -r requirements-audio-review.txt
python review_audio.py --cache private_work/models --model base.en
python review_audio.py --cache private_work/models --model small.en --output audio_review/small_en
```

The model weights are downloaded once and inference runs locally. The original MP3 files were not changed. The initial decoder attempt failed because PyAV 19 removed a keyword used by faster-whisper 1.2.1. An attempted PyAV 14 source installation could not build without system libraries; no system library installation was performed. The final script explicitly decodes and resamples using the installed PyAV 19 interface.

Software: [faster-whisper](https://github.com/SYSTRAN/faster-whisper). Exact installed versions, downloaded model revisions and model hashes appear in the result JSON files. These software components are execution tools; no new substantive research dataset was added.

## Listening checks still requiring a person

- Confirm the disclosure is clear at the beginning.
- Listen to the player-name passage and compare it with the written script: approximately 48–55 seconds for Payton Rowley, 63–69 seconds for Emma Tyrrell, and 71–75 seconds for the later Rowley reference.
- Check pacing and transitions between interview segments.
- Confirm “one,” “two,” and “four and a half” are easy to distinguish.
- Listen through the final limitation; note any awkward pauses, cuts, or pronunciation issues.

No listener ratings, naturalness scores, or claims of completed perceptual review are recorded.
