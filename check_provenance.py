"""Inspect disclosure metadata, re-encode without tags, and check audio integrity."""
import argparse,json,re,subprocess,hashlib,wave,math,struct
from pathlib import Path
import imageio_ffmpeg

def check(root,scratch):
 ff=imageio_ffmpeg.get_ffmpeg_exe();scratch.mkdir(parents=True,exist_ok=True);results={}
 for p in sorted((root/'artifacts').glob('*.mp3')):
  metadata=subprocess.check_output([ff,'-v','error','-i',str(p),'-f','ffmetadata','-'],text=True)
  wav=scratch/(p.stem+'.wav')
  subprocess.run([ff,'-v','error','-y','-i',str(p),'-ar','22050','-ac','1','-c:a','pcm_s16le',str(wav)],check=True)
  with wave.open(str(wav),'rb') as w:
   frames=w.readframes(w.getnframes());samples=struct.unpack('<'+'h'*(len(frames)//2),frames);duration=len(samples)/w.getframerate()
   peak=max(abs(x) for x in samples);rms=math.sqrt(sum(x*x for x in samples)/len(samples));clip=sum(abs(x)>=32767 for x in samples)
  results[p.name]={'duration_seconds':duration,'peak_fraction':peak/32768,'rms_fraction':rms/32768,'clipped_samples':clip,'decoded_samples':len(samples),'metadata':metadata,'c2pa_literal_marker_found':b'c2pa' in p.read_bytes().lower(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 original=root/'artifacts'/'AI_generated_synthetic_B_interview.mp3';stripped=scratch/'AI_generated_synthetic_B_metadata_stripped.mp3'
 cmd=[ff,'-v','error','-y','-i',str(original),'-map_metadata','-1','-codec:a','libmp3lame','-q:a','5',str(stripped)]
 subprocess.run(cmd,check=True)
 metadata=subprocess.check_output([ff,'-v','error','-i',str(stripped),'-f','ffmetadata','-'],text=True)
 results['transformation']={'command':cmd,'stripped_metadata':metadata,'disclosure_title_retained':'AI-generated synthetic research audio' in metadata,'sha256_changed':hashlib.sha256(original.read_bytes()).digest()!=hashlib.sha256(stripped.read_bytes()).digest(),'limitation':'Generic metadata inspection and literal marker scan, not a C2PA signature validator or an AI detector. Absence of a marker does not prove absence of every possible watermark. No signed C2PA claim was created by this pipeline.'}
 (root/'provenance_results.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--scratch',type=Path,default=Path('private_work'));a=p.parse_args();check(Path(__file__).resolve().parent,a.scratch)
