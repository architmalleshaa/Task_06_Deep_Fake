"""Unprompted local ASR check; this is not a human listening assessment."""
import argparse
import hashlib
import importlib.metadata
import json
import re
from datetime import datetime, timezone
from pathlib import Path

def tokens(text, normalize_numbers=False):
    text = text.lower().replace('’', "'")
    if normalize_numbers:
        text = re.sub(r'(\d+)\s*%',r'\1 percent',text)
        forms = {'1':'one','2':'two','3':'three','4':'four','16':'sixteen',
                 '22':'twenty two','23':'twenty three','50':'fifty','55':'fifty five',
                 '70':'seventy','2024':'twenty twenty four'}
        text = re.sub(r'\b\d+\b', lambda m: forms.get(m[0], m[0]), text)
        text = text.replace("'",'')
    return re.findall(r"[a-z0-9]+(?:'[a-z]+)?", text)

def compare(reference, hypothesis):
    # Unit-cost Levenshtein distance, with the actual edits retained for review.
    n,m=len(reference),len(hypothesis)
    d=[[0]*(m+1) for _ in range(n+1)]
    for i in range(n+1): d[i][0]=i
    for j in range(m+1): d[0][j]=j
    for i in range(1,n+1):
        for j in range(1,m+1):
            d[i][j]=min(d[i-1][j]+1,d[i][j-1]+1,d[i-1][j-1]+(reference[i-1]!=hypothesis[j-1]))
    edits=[];i=n;j=m
    while i or j:
        if i and j and d[i][j]==d[i-1][j-1]+(reference[i-1]!=hypothesis[j-1]):
            if reference[i-1]!=hypothesis[j-1]:
                edits.append({'type':'substitution','reference_index':i-1,'reference':reference[i-1],'recognized':hypothesis[j-1]})
            i-=1;j-=1
        elif i and d[i][j]==d[i-1][j]+1:
            edits.append({'type':'deletion','reference_index':i-1,'reference':reference[i-1],'recognized':''});i-=1
        else:
            edits.append({'type':'insertion','reference_index':i,'reference':'','recognized':hypothesis[j-1]});j-=1
    return {'reference_words':n,'recognized_words':m,'edit_distance':d[n][m],
            'word_error_rate':d[n][m]/n,'edits':list(reversed(edits))}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--cache', required=True, type=Path)
    parser.add_argument('--model',default='base.en')
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    from faster_whisper import WhisperModel
    from faster_whisper.utils import download_model
    import av
    import numpy as np
    root=Path(__file__).resolve().parent
    model_path=Path(download_model(args.model,cache_dir=str(args.cache)))
    model=WhisperModel(str(model_path),device='cpu',compute_type='int8',cpu_threads=4)
    out=args.output or root/'audio_review';out.mkdir(parents=True,exist_ok=True)
    report={'review_type':'automated speech recognition; no perceptual listening claim',
            'created_at':datetime.now(timezone.utc).isoformat(),
            'model':args.model,'model_revision':model_path.name,
            'model_sha256':hashlib.sha256((model_path/'model.bin').read_bytes()).hexdigest(),
            'versions':{p:importlib.metadata.version(p) for p in ['faster-whisper','ctranslate2','av']},
            'settings':{'device':'cpu','compute_type':'int8','beam_size':5,'temperature':0,
                        'language':'en','condition_on_previous_text':False,'vad_filter':False,
                        'initial_prompt':None},'files':[]}
    for audio in sorted((root/'artifacts').glob('*.mp3')):
        if audio.name not in {'AI_generated_synthetic_A_monologue.mp3','AI_generated_synthetic_B_interview.mp3'}:continue
        # Decode explicitly: PyAV 19 removed the metadata_errors keyword used
        # by faster-whisper 1.2.1's internal file decoder.
        resampler=av.AudioResampler(format='fltp',layout='mono',rate=16000)
        chunks=[]
        with av.open(str(audio),mode='r') as container:
            for frame in container.decode(audio=0):
                chunks.extend(f.to_ndarray().reshape(-1) for f in resampler.resample(frame))
        chunks.extend(f.to_ndarray().reshape(-1) for f in resampler.resample(None))
        waveform=np.concatenate(chunks).astype(np.float32)
        segments,info=model.transcribe(waveform,language='en',beam_size=5,temperature=0,
                                      condition_on_previous_text=False,vad_filter=False)
        rows=[{'start':s.start,'end':s.end,'text':s.text,'avg_logprob':s.avg_logprob,
               'no_speech_prob':s.no_speech_prob} for s in segments]
        transcript=' '.join(s['text'].strip() for s in rows)
        # Read the reference only after ASR; it is never passed to the model.
        reference=(root/'source_script.txt').read_text()
        record={'file':audio.name,'sha256':hashlib.sha256(audio.read_bytes()).hexdigest(),
                'duration':info.duration,'transcript':transcript,'segments':rows,
                'raw_comparison':compare(tokens(reference),tokens(transcript)),
                'number_normalized_comparison':compare(tokens(reference,True),tokens(transcript,True))}
        report['files'].append(record)
        (out/(audio.stem+'.txt')).write_text(transcript+'\n')
        (out/'results.json').write_text(json.dumps(report,indent=2)+'\n')
        print(audio.name,json.dumps(record['number_normalized_comparison']),flush=True)
    assert len(report['files'])==2,'Expected both generated audio files'

if __name__=='__main__':main()
