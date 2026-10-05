# Provenance and transformation check

The provenance experiment inspected the two generated MP3 files and re-encoded the interview with metadata explicitly removed. It did not upload the files anywhere.

Both originals contained `title=AI-generated synthetic research audio` and a comment stating that the voices were computer-synthesized and no real coach or player was speaking. After re-encoding with `-map_metadata -1`, the extracted metadata retained only the encoder field. The title and disclosure comment were absent, and the output SHA-256 differed. The exact command and extracted metadata appear in `provenance_results.json`.

This demonstrates a specific weakness of ordinary metadata in this pipeline: it can disappear during transformation. It does not demonstrate that every social platform strips metadata, that a cryptographic provenance system was defeated, or that a detector was fooled. The clip was not uploaded to a platform and no cryptographic signature was created.

No literal `c2pa` marker was found in the inspected MP3 bytes. A byte-marker scan is not a C2PA validator and cannot rule out every metadata representation or watermark. The pipeline itself did not add signed content credentials. The SHA-256 manifest identifies a file version; an unsigned hash alone does not authenticate the speaker, producer, consent or truth of its claims.

The spoken disclosure is part of the scripted audio rather than a metadata field. Re-encoding was intended to retain the audio stream's content, but its intelligibility was not independently heard or transcribed. An excerpt that removes the beginning can remove that contextual safeguard even when metadata is intact. Task 7 therefore requires disclosure on each separately distributed excerpt and a retained source/approval record.

No detector accuracy estimate, confidence score or claim about the field's detection race is supported by this experiment. The assignment permits a detection **or** provenance attempt; the metadata/provenance route is the one actually attempted here.
