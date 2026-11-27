import sys,re,glob
for f in sorted(glob.glob(''+__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','words','src','*.txt')+'')):
  for no,ln in enumerate(open(f),1):
    if not ln.startswith('W '): continue
    p=[x.strip() for x in ln[2:].split(' | ')]
    if len(p)<10: continue
    for txt,lang in ((p[8],'uk'),(p[9],'ru')):
        t=re.sub(r'\{[^}]*\}','',txt)
        pat=r'\b[Яя]\s+(?:\w+\s+){0,2}?(\w+(?:в|ла|вся|лася|лась))\b' if lang=='uk' else r'\b[Яя]\s+(?:\w+\s+){0,2}?(\w+(?:л|ла|лся|лась))\b'
        for m in re.finditer(r'\b(должен|готов|рад|уверен|занят|свободен|недоступен|болен|счастлив|виноват|согласен|повинен|готовий|радий|впевнений|зайнятий|вільний|недоступний|хворий|щасливий|винен|згоден|сам|сама|один|одна|самий)\b',t):
            print(f"{f.split('/')[-1]}:{no} {lang}: ADJ {m.group(1)} :: {txt[:80]}")
        for m in re.finditer(pat,t):
            w=m.group(1)
            if w.lower() in ('пробіл','пробел','стіл','стол','футбол','вокзал','хотів','хотел') and False: pass
            if w.lower() in ('мала','тепла','була','ціла','дуже','сила','мила','весела','біла','стала','кола','школа','села','справа','зла','земля','ла'): pass
            print(f"{f.split('/')[-1]}:{no} {lang}: {w} :: {txt[:80]}")
