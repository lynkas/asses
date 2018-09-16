import re,sys

R=0.7
class an_ass:

    def __init__(self,file,ud):
        self.style = ''
        self.dialogues = []
        with open(file, encoding='utf-8') as f:
            content = f.readlines()

        content=''.join(content)
        content = content.split(r'[Events]')[1]
        content = re.sub(r'(\s*)\[(.*)\](^\S\n)*', '', content)
        content = content.replace('\\N', ' ')

        if ud == 'u':
            self.style='Style: '+ud+',Noto Sans CJK SC Medium,25,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,1,0,2,10,10,15,0\n'
            for p in content.split('\n'):
                if p.split('0,0,0,,')[-1] and p.split('0,0,0,,')[-1].strip()!='-' and p.startswith('Dialogue'):
                    self.dialogues.append(p.replace('Default', ud, 1).replace('0,0,0,,', '0,0,0,,{\pos(193.0,278.0)}').strip())
        else:
            self.style='Style: '+ud+',Noto Sans CJK SC Medium,13,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,1,0,2,10,10,5,0\n'
            for p in content.split('\n'):
                if p.split('0,0,0,,')[-1] and p.split('0,0,0,,')[-1].strip()!='-' and p.startswith('Dialogue'):
                    self.dialogues.append(p.replace('Default', ud, 1).replace('0,0,0,,', '0,0,0,,{\pos(193.0,288.0)}').strip())

class time:
    def __init__(self,t):
        # print(t)
        self.h = int(t.split(':')[0])
        self.m = int(t.split(':')[1])
        self.s = int(t.split(':')[2].split('.')[0])
        self.ms = int(t.split(':')[2].split('.')[1])

        self.rms=((self.h*60+self.m)*60+self.s)*100+self.ms

    def __str__(self):
        return str(self.h)+":"+str(self.m)+":"+str(self.s)+"."+str(self.ms)

    def isLagerThan(self,t):
        return self.rms>t.rms

class dia:
    def __init__(self,dia):
        self.st=time(dia.split(',')[1])
        self.et=time(dia.split(',')[2])
        self.style=dia.split(',')[3]

        self.whole = dia

    def __str__(self):
        return "Dialogue: 0,"+str(self.st)+","+str(self.et)+","+self.style+",,0,0,0,,"+self.whole.split(",,0,0,0,,")[1]


# 0 no re
# 1 1 short
# 2 2 short
# 3 re

def isRe(t1s,t1e,t2s,t2e):
    d=(min(t1e.rms,t2e.rms)-max(t1s.rms,t2s.rms))
    if d/(t1e.rms-t1s.rms)>=R and d/(t2e.rms-t2s.rms)>=R:
        print(3)
        return 3
    elif d/(t1e.rms-t1s.rms)>=R and d/(t2e.rms-t2s.rms)<R:
        print(1)
        return 1
    elif d/(t1e.rms-t1s.rms)<R and d/(t2e.rms-t2s.rms)>=R:
        print(2)
        return 2
    else:
        print(0)
        return 0



# u=sys.argv[1]
# d=sys.argv[2]
u='zh.ass'
d='en.ass'
a = an_ass(u,'u')
b = an_ass(d,'d')
uplist=[]
botlist=[]
finallist=[]

for i in a.dialogues:
    uplist.append(dia(i))
for i in b.dialogues:
    botlist.append(dia(i))

las=time('0:00:00.00')

def comb(lis1,lis2,res):
    global las
    if (len(lis1)==0):
        res.append(lis2)
        return
    if (len(lis2)==0):
        res.append(lis1)
        return

    re=isRe(lis1[0].st,lis1[0].et,lis2[0].st,lis2[0].et)

    if re==0:
        if (lis1[0].st.rms < lis2[0].st.rms):
            print(lis1[0])
            res.append(lis1.pop(0))
        else:
            print(lis2[0])
            if las.isLagerThan(lis2[0].st):
                lis2[0].st=las
            las = lis2[0].et
            print(str(las))
            res.append(lis2.pop(0))

    elif re==1:
        if len(lis1)!=1 and isRe(lis1[0].st, lis1[1].et, lis2[0].st, lis2[0].et)==3:
            lis2[0].st=lis1[0].st
            lis2[0].et=lis1[1].et
            print(lis2[0])
            if las.isLagerThan(lis2[0].st):
                lis2[0].st=las
            las=lis2[0].et
            print(str(las))
            res.append(lis2.pop(0))
            print(lis1[0])
            res.append(lis1.pop(0))
            print(lis1[0])
            res.append(lis1.pop(0))
        else:
            lis2[0].st=lis1[0].st
            lis2[0].et=lis1[0].et

    elif re==2:
        if len(lis2)!=1 and isRe(lis1[0].st, lis1[0].et, lis2[0].st, lis2[1].et)==3:
            lis2[0].st=lis1[0].st
            lis2[1].et=lis1[0].et
            print(lis1[0])
            res.append(lis1.pop(0))
            print(lis2[0])
            res.append(lis2.pop(0))
            if las.isLagerThan(lis2[0].st):
                lis2[0].st=las
            print(lis2[0])
            las = lis2[0].et
            print(str(las))
            res.append(lis2.pop(0))
        else:
            lis2[0].st=lis1[0].st
            lis2[0].et=lis1[0].et
    else:
        lis2[0].st=lis1[0].st
        lis2[0].et=lis1[0].et
        print(lis1[0])
        res.append(lis1.pop(0))
        print(lis2[0])
        if las.isLagerThan(lis2[0].st):
            lis2[0].st = las
        las = lis2[0].et
        print(str(las))
        res.append(lis2.pop(0))

    comb(lis1,lis2,res)

comb(uplist,botlist,finallist)

head='''[Script Info]
; by Moki
ScriptType: v4.00+
PlayResX: 384
PlayResY: 288

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
'''

neck='''[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''


nf = [str(i) for i in finallist]

final=head+a.style+b.style+neck+'\n'.join(nf)

with open(u+".COM.ass", "w",encoding='utf-8') as text_file:
    print(final, file=text_file)

