import re,sys

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
                if p.split('0,0,0,,')[-1] and p.split('0,0,0,,')[-1].strip()!='-':
                    self.dialogues.append(p.replace('Default', ud, 1).replace('0,0,0,,', '0,0,0,,{\pos(193.0,278.0)}').strip())
        else:
            self.style='Style: '+ud+',Noto Sans CJK SC Medium,13,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,1,0,2,10,10,5,0\n'
            for p in content.split('\n'):
                if p.split('0,0,0,,')[-1] and p.split('0,0,0,,')[-1].strip()!='-':
                    self.dialogues.append(p.replace('Default', ud, 1).replace('0,0,0,,', '0,0,0,,{\pos(193.0,288.0)}').strip())



u=sys.argv[1]
d=sys.argv[2]

a = an_ass(u,'u')
b = an_ass(d,'d')

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

final=head+a.style+b.style+neck+'\n'.join(a.dialogues)+'\n'.join(b.dialogues)

with open(u+".COM.ass", "w",encoding='utf-8') as text_file:
    print(final, file=text_file)

