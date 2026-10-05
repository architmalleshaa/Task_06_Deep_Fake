"""Two stock-voice pipelines on macOS, no identity cloning or paid service."""
from pathlib import Path
import argparse,hashlib,json,platform,subprocess,time
from datetime import datetime,timezone
import imageio_ffmpeg

def run(cmd):
 start=time.perf_counter();r=subprocess.run(cmd,capture_output=True,text=True)
 return {'command':cmd,'elapsed_seconds':time.perf_counter()-start,'return_code':r.returncode,'stderr':r.stderr[-4000:]}
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('artifacts'));p.add_argument('--work',type=Path,default=Path('private_work'));args=p.parse_args()
 root=Path(__file__).resolve().parent;output=args.output.resolve();scratch=args.work.resolve();output.mkdir(parents=True,exist_ok=True);scratch.mkdir(parents=True,exist_ok=True)
 ff=imageio_ffmpeg.get_ffmpeg_exe();script=root/'source_script.txt';paragraphs=script.read_text().strip().split('\n\n')
 log={'started_utc':datetime.now(timezone.utc).isoformat(),'platform':platform.platform(),'os_version':subprocess.check_output(['sw_vers'],text=True),'speech_tool':'/usr/bin/say; installed stock voices; no voice-model version exposed','ffmpeg_version':subprocess.check_output([ff,'-version'],text=True).splitlines()[0],'cost':'Local installed speech synthesis; no paid API, no external upload, no free-tier quota encountered.','source_script_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'commands':[]}
 def checked(cmd):
  result=run(cmd);log['commands'].append(result)
  (root/'process_log.json').write_text(json.dumps(log,indent=2))
  if result['return_code']:raise RuntimeError(result['stderr'])
 a=scratch/'continuous.aiff';checked(['/usr/bin/say','-v','Samantha','-r','175','-f',str(script),'-o',str(a)])
 # Pipeline B alternates question and analyst roles, each synthesized separately.
 parts=[]
 for i,paragraph in enumerate(paragraphs):
  voice='Daniel' if i==0 or i%2==1 else 'Samantha';rate='165' if voice=='Daniel' else '155'
  text=scratch/f'part_{i:02d}.txt';text.write_text(paragraph);part=scratch/f'part_{i:02d}.aiff'
  checked(['/usr/bin/say','-v',voice,'-r',rate,'-f',str(text),'-o',str(part)]);parts.append(part)
 concat=scratch/'concat.txt';concat.write_text(''.join("file '"+str(x).replace("'","'\\''")+"'\n" for x in parts))
 meta=['-metadata','title=AI-generated synthetic research audio','-metadata','comment=Computer-synthesized stock voices. No real coach or player is speaking.']
 checked([ff,'-y','-i',str(a),*meta,'-codec:a','libmp3lame','-q:a','3',str(output/'AI_generated_synthetic_A_monologue.mp3')])
 checked([ff,'-y','-f','concat','-safe','0','-i',str(concat),*meta,'-codec:a','libmp3lame','-q:a','3',str(output/'AI_generated_synthetic_B_interview.mp3')])
 log['finished_utc']=datetime.now(timezone.utc).isoformat();log['generation_wall_seconds']=sum(x['elapsed_seconds'] for x in log['commands'])
 log['artifacts']={x.name:{'bytes':x.stat().st_size,'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for x in output.glob('*.mp3')}
 (root/'process_log.json').write_text(json.dumps(log,indent=2));print(json.dumps(log['artifacts'],indent=2))
if __name__=='__main__':main()
