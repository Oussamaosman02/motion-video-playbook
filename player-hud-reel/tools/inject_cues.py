# One-off builder used for x-batch/nateherk: injects word times (work/words.json), particle points (work/pts58.json) and the SFX <audio> cues into work/index.tpl.html -> index.html. After the first build, index.html was edited directly, so do not re-run it over a finished project; copy the cue-list pattern instead.
import json
W = json.load(open('work/words.json')); P = json.load(open('work/pts58.json'))
VO = 0.4
t = lambda i: W[i][1] + VO
dur = {'whoosh':1.2,'impact':2.0,'tick':0.5,'type':1.5,'pop':0.5,'glitch':1.2,'key':0.5,'boom':1.5,'click':0.5,'chime':2.0,'shimmer':1.5,'stutter':0.8}
S5=t(26)-0.05; S12=t(83)-0.1; S15=32.95
cues = [('whoosh',0.0,0.4),('stutter',t(14)-0.05,0.6),('impact',t(14),0.55),('pop',t(15),0.45),
  ('type',t(16),0.4),('glitch',t(21)+0.3,0.3),('type',t(22),0.4),('click',t(24)-0.2,0.6),
  ('pop',t(24)-0.08,0.4),('boom',t(25)-0.05,0.6),('shimmer',S5+0.1,0.7),('stutter',S5,0.45),
  ('pop',t(34)-0.08,0.4),('pop',t(36)-0.08,0.4),('pop',t(39)-0.08,0.4),('whoosh',t(43)-0.1,0.4),
  ('pop',t(47)-0.1,0.45),('pop',t(50)-0.05,0.45),('click',t(56)-0.05,0.7),('chime',t(56)-0.05,0.35),
  ('whoosh',t(59)-0.05,0.45),('shimmer',t(62),0.5),('stutter',t(66)-0.05,0.6),('impact',t(68),0.5),
  ('pop',t(73)+0.35,0.4),('click',t(80)+0.15,0.7),('chime',t(80)+0.25,0.3)]
cues += [('tick',S12+i*0.5,0.55) for i in range(4)]
cues += [('stutter',t(87)-0.05,0.45),('whoosh',t(90)-0.15,0.35),('impact',t(90)+0.25,0.45),('pop',t(93)-0.05,0.45),
  ('pop',t(95)-0.05,0.45),('pop',t(97)-0.05,0.4),('impact',t(103)-0.04,0.55),('boom',S15,0.55),('chime',S15+0.9,0.4)]
lines=[]
for n,(f,a,v) in enumerate(cues):
  lines.append(f'      <audio id="a{n}" src="assets/{f}.mp3" data-start="{a:.2f}" data-duration="{dur[f]}" data-track-index="{12+n}" data-volume="{v}"></audio>')
s=open('work/index.tpl.html').read()
s=s.replace('/*W*/',json.dumps(W,ensure_ascii=False,separators=(',',':'))).replace('/*PTS*/',json.dumps(P,separators=(',',':'))).replace('      <!--SFX-->','\n'.join(lines))
open('index.html','w').write(s); print(len(cues),'sfx')
