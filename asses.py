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
        content = content.replace('--',' ')
        content = content.replace('- -'," ")


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
        # #print(t)
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
        #print(3)
        return 3
    elif d/(t1e.rms-t1s.rms)>=R and d/(t2e.rms-t2s.rms)<R:
        #print(1)
        return 1
    elif d/(t1e.rms-t1s.rms)<R and d/(t2e.rms-t2s.rms)>=R:
        #print(2)
        return 2
    else:
        #print(0)
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
        res+=lis2
        return
    if (len(lis2)==0):
        res+=lis1
        return

    re=isRe(lis1[0].st,lis1[0].et,lis2[0].st,lis2[0].et)

    if re==0:
        if (lis1[0].st.rms < lis2[0].st.rms):
            #print(lis1[0])
            res.append(lis1.pop(0))
        else:
            #print(lis2[0])
            if las.isLagerThan(lis2[0].st):
                lis2[0].st=las
            las = lis2[0].et
            #print(str(las))
            res.append(lis2.pop(0))

    elif re==1:
        if len(lis1)!=1 and isRe(lis1[0].st, lis1[1].et, lis2[0].st, lis2[0].et)==3:
            lis2[0].st=lis1[0].st
            lis2[0].et=lis1[1].et
            #print(lis2[0])
            if las.isLagerThan(lis2[0].st):
                lis2[0].st=las
            las=lis2[0].et
            #print(str(las))
            res.append(lis2.pop(0))
            #print(lis1[0])
            res.append(lis1.pop(0))
            #print(lis1[0])
            res.append(lis1.pop(0))
        else:
            lis2[0].st=lis1[0].st
            lis2[0].et=lis1[0].et

    elif re==2:
        if len(lis2)!=1 and isRe(lis1[0].st, lis1[0].et, lis2[0].st, lis2[1].et)==3:
            lis2[0].st=lis1[0].st
            lis2[1].et=lis1[0].et
            #print(lis1[0])
            res.append(lis1.pop(0))
            #print(lis2[0])
            res.append(lis2.pop(0))
            if las.isLagerThan(lis2[0].st):
                lis2[0].st=las
            #print(lis2[0])
            las = lis2[0].et
            #print(str(las))
            res.append(lis2.pop(0))
        else:
            lis2[0].st=lis1[0].st
            lis2[0].et=lis1[0].et
    else:
        lis2[0].st=lis1[0].st
        lis2[0].et=lis1[0].et
        #print(lis1[0])
        res.append(lis1.pop(0))
        #print(lis2[0])
        if las.isLagerThan(lis2[0].st):
            lis2[0].st = las
        las = lis2[0].et
        #print(str(las))
        res.append(lis2.pop(0))

    comb(lis1,lis2,res)

comb(uplist,botlist,finallist)

head='''[Script Info]
; by Moki
ScriptType: v4.00+
PlayResX: 384
PlayResY: 288
ScaledBorderAndShadow: no

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
'''

neck='''[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''


nf = [str(i) for i in finallist]

final=head+a.style+b.style+neck+'\n'.join(nf)

print(nf)

with open(u+".COM.ass", "w",encoding='utf-8') as text_file:
    print(final, file=text_file)


# Dialogue: 0,0:00:51.47,0:00:52.68,Default,,0,0,0,,太阳
# Dialogue: 0,0:00:53.68,0:00:55.02,Default,,0,0,0,,月亮
# Dialogue: 0,0:00:56.85,0:00:58.23,Default,,0,0,0,,星辰
# Dialogue: 0,0:01:01.39,0:01:02.68,Default,,0,0,0,,大地
# Dialogue: 0,0:01:06.44,0:01:07.98,Default,,0,0,0,,天空
# Dialogue: 0,0:01:11.40,0:01:12.78,Default,,0,0,0,,还有海洋
# Dialogue: 0,0:01:15.58,0:01:17.87,Default,,0,0,0,,但一千年前
# Dialogue: 0,0:01:17.95,0:01:21.83,Default,,0,0,0,,一个人类魔法师发现了新魔法
# Dialogue: 0,0:01:22.21,0:01:23.75,Default,,0,0,0,,第七能源
# Dialogue: 0,0:01:25.04,0:01:26.37,Default,,0,0,0,,黑暗魔法
# Dialogue: 0,0:01:36.01,0:01:40.85,Default,,0,0,0,,通过生物内在的本源
# Dialogue: 0,0:01:41.73,0:01:45.15,Default,,0,0,0,,来释放黑暗力量
# Dialogue: 0,0:02:00.25,0:02:02.84,Default,,0,0,0,,由于后果太可怕
# Dialogue: 0,0:02:02.96,0:02:07.30,Default,,0,0,0,,精灵和龙族共同制止了这种行为
# Dialogue: 0,0:02:07.79,0:02:12.00,Default,,0,0,0,,并将人类流放到了西方
# Dialogue: 0,0:02:12.42,0:02:16.47,Default,,0,0,0,,之后 这片大陆就一分为二
# Dialogue: 0,0:02:17.01,0:02:20.26,Default,,0,0,0,,在东方 魔法之地沙迪亚
# Dialogue: 0,0:02:20.60,0:02:23.52,Default,,0,0,0,,西方 则是人类的王国
# Dialogue: 0,0:02:27.40,0:02:33.24,Default,,0,0,0,,几个世纪以来\N龙族国王亲自守卫边界
# Dialogue: 0,0:02:40.91,0:02:42.66,Default,,0,0,0,,冲锋！
# Dialogue: 0,0:02:51.25,0:02:53.42,Default,,0,0,0,,人类将之称为雷电
# Dialogue: 0,0:02:54.67,0:02:55.96,Default,,0,0,0,,因为他说话时
# Dialogue: 0,0:02:56.05,0:03:00.47,Default,,0,0,0,,声音可以摇动大地和苍穹
# Dialogue: 0,0:03:02.97,0:03:07.64,Default,,0,0,0,,但在上个冬天来临前
# Dialogue: 0,0:03:07.73,0:03:12.03,Default,,0,0,0,,人类使用不知名的黑色魔法
# Dialogue: 0,0:03:12.15,0:03:13.86,Default,,0,0,0,,杀死了雷电
# Dialogue: 0,0:03:14.53,0:03:18.83,Default,,0,0,0,,然后残忍地摧毁了唯一的蛋
# Dialogue: 0,0:03:18.95,0:03:22.58,Default,,0,0,0,,他的后代 龙王子
# Dialogue: 0,0:03:24.08,0:03:29.75,Default,,0,0,0,,现在整个世界濒临战争边缘
# Dialogue: 0,0:03:40.09,0:03:41.59,Default,,0,0,0,,（卷1 月亮）
# Dialogue: 0,0:03:42.10,0:03:44.90,Default,,0,0,0,,（第1章 雷霆的回响）
# Dialogue: 0,0:04:18.22,0:04:20.22,Default,,0,0,0,,怪物受死吧！
# Dialogue: 0,0:04:26.06,0:04:29.40,Default,,0,0,0,,-卡勒姆！\N-没事的 艾斯兰 只是打雷
# Dialogue: 0,0:04:29.73,0:04:32.07,Default,,0,0,0,,不要害怕 回去睡觉吧
# Dialogue: 0,0:04:32.98,0:04:34.27,Default,,0,0,0,,我不是害怕
# Dialogue: 0,0:04:35.02,0:04:36.23,Default,,0,0,0,,小饵害怕
# Dialogue: 0,0:04:56.75,0:04:57.79,Default,,0,0,0,,谁在那里？
# Dialogue: 0,0:05:01.84,0:05:03.97,Default,,0,0,0,,表明身份 以哈罗国王的名义
# Dialogue: 0,0:05:43.22,0:05:44.22,Default,,0,0,0,,求你！
# Dialogue: 0,0:05:46.51,0:05:47.60,Default,,0,0,0,,你是谁？
# Dialogue: 0,0:06:32.98,0:06:35.19,Default,,0,0,0,,殿下！有急事禀报
# Dialogue: 0,0:06:41.57,0:06:44.37,Default,,0,0,0,,威伦殿下 我看到些东西
# Dialogue: 0,0:06:52.83,0:06:55.50,Default,,0,0,0,,威伦殿下 哈罗国王还没起床
# Dialogue: 0,0:07:07.68,0:07:11.56,Default,,0,0,0,,威伦 我好像跟你说过\N如果再这么早叫醒我
# Dialogue: 0,0:07:12.14,0:07:13.72,Default,,0,0,0,,我就把你处决
# Dialogue: 0,0:07:15.18,0:07:16.64,Default,,0,0,0,,我给你点时间洗漱
# Dialogue: 0,0:07:28.07,0:07:32.41,Default,,0,0,0,,你不顾生命危险 这么早把我叫醒\N是有什么要紧事
# Dialogue: 0,0:07:33.66,0:07:34.95,Default,,0,0,0,,刺客
# Dialogue: 0,0:07:35.46,0:07:36.38,Default,,0,0,0,,好吧
# Dialogue: 0,0:07:36.83,0:07:40.21,Default,,0,0,0,,黎明前有守卫发现的
# Dialogue: 0,0:07:40.71,0:07:45.26,Default,,0,0,0,,别这么紧张 以前都来过很多刺客
# Dialogue: 0,0:07:45.76,0:07:50.68,Default,,0,0,0,,这次不同 我们相信是月影精灵
# Dialogue: 0,0:07:51.55,0:07:53.14,Default,,0,0,0,,月影精灵？
# Dialogue: 0,0:07:53.60,0:07:55.19,Default,,0,0,0,,那个守卫怎么逃脱的？
# Dialogue: 0,0:07:55.93,0:07:58.68,Default,,0,0,0,,不知道 当时很泥泞 湿滑 天黑
# Dialogue: 0,0:07:59.19,0:08:01.78,Default,,0,0,0,,反正 他就是很走运
# Dialogue: 0,0:08:02.44,0:08:04.82,Default,,0,0,0,,皇家卫队也不能对付他们
# Dialogue: 0,0:08:05.40,0:08:07.94,Default,,0,0,0,,派阿玛雅将军和步兵营过去
# Dialogue: 0,0:08:08.78,0:08:11.91,Default,,0,0,0,,边境距离太远了 回援不及
# Dialogue: 0,0:08:13.08,0:08:15.67,Default,,0,0,0,,-今晚的月亮是什么？\N-满月
# Dialogue: 0,0:08:17.62,0:08:18.79,Default,,0,0,0,,当然
# Dialogue: 0,0:08:19.04,0:08:22.17,Default,,0,0,0,,月影精灵今晚能量达到最高点
# Dialogue: 0,0:08:22.75,0:08:24.67,Default,,0,0,0,,没有人可以抵挡
# Dialogue: 0,0:08:25.55,0:08:28.30,Default,,0,0,0,,我们不能被动防守 要主动出击
# Dialogue: 0,0:08:29.01,0:08:31.01,Default,,0,0,0,,要在今天找到他们
# Dialogue: 0,0:08:31.18,0:08:34.10,Default,,0,0,0,,借助太阳 不然就太迟了
# Dialogue: 0,0:09:26.86,0:09:28.24,Default,,0,0,0,,做得好 瑞拉
# Dialogue: 0,0:09:28.40,0:09:30.78,Default,,0,0,0,,我用了双刀
# Dialogue: 0,0:09:32.11,0:09:33.44,Default,,0,0,0,,我能看见
# Dialogue: 0,0:10:00.39,0:10:01.22,Default,,0,0,0,,小饵
# Dialogue: 0,0:10:11.36,0:10:12.53,Default,,0,0,0,,艾斯兰王子！
# Dialogue: 0,0:10:13.90,0:10:14.94,Default,,0,0,0,,捉到你了
# Dialogue: 0,0:10:15.45,0:10:17.70,Default,,0,0,0,,我觉得很赞
# Dialogue: 0,0:10:18.16,0:10:20.75,Default,,0,0,0,,-所以就伸手了？\N-嗯
# Dialogue: 0,0:10:21.08,0:10:23.58,Default,,0,0,0,,看起来很棒呢
# Dialogue: 0,0:10:23.87,0:10:27.12,Default,,0,0,0,,确实很棒 但不是给你的
# Dialogue: 0,0:10:27.21,0:10:29.80,Default,,0,0,0,,或是你那个小畜生
# Dialogue: 0,0:10:31.01,0:10:32.64,Default,,0,0,0,,你刚才…
# Dialogue: 0,0:10:33.17,0:10:35.21,Default,,0,0,0,,从眼神就能看出他是无辜的
# Dialogue: 0,0:10:37.68,0:10:40.89,Default,,0,0,0,,你开玩笑吗？我就站在这里
# Dialogue: 0,0:10:42.02,0:10:43.06,Default,,0,0,0,,嘿
# Dialogue: 0,0:11:02.08,0:11:05.46,Default,,0,0,0,,卡勒姆王子 今天我们练习防守艺术
# Dialogue: 0,0:11:05.54,0:11:07.54,Default,,0,0,0,,艺术！这个我比较擅长
# Dialogue: 0,0:11:09.38,0:11:11.26,Default,,0,0,0,,抱歉 不会再插嘴了
# Dialogue: 0,0:11:11.88,0:11:13.88,Default,,0,0,0,,请继续 索伦
# Dialogue: 0,0:11:15.30,0:11:19.26,Default,,0,0,0,,防守的艺术 在持剑搏斗时至关重要
# Dialogue: 0,0:11:19.85,0:11:22.85,Default,,0,0,0,,闪避和角度 动作 预判有关
# Dialogue: 0,0:11:23.06,0:11:26.77,Default,,0,0,0,,如果预判错了 就结束了\N准备好了吗？
# Dialogue: 0,0:11:30.44,0:11:33.65,Default,,0,0,0,,-我没准备好\N-很好 来吧
# Dialogue: 0,0:11:38.28,0:11:40.41,Default,,0,0,0,,闪避 闪避 你死了
# Dialogue: 0,0:11:41.99,0:11:44.70,Default,,0,0,0,,闪避 闪避 你死了\N闪避 死了
# Dialogue: 0,0:11:46.25,0:11:48.84,Default,,0,0,0,,即使我穿着盔甲也死了吗？
# Dialogue: 0,0:11:48.92,0:11:51.76,Default,,0,0,0,,即使你穿着由骄阳精灵所制的
# Dialogue: 0,0:11:51.84,0:11:54.55,Default,,0,0,0,,最好的盔甲 也死了
# Dialogue: 0,0:11:55.13,0:11:58.13,Default,,0,0,0,,-我不擅长这些事\N-但你要继续练习
# Dialogue: 0,0:11:58.22,0:12:00.22,Default,,0,0,0,,因为这是王子的责任
# Dialogue: 0,0:12:01.10,0:12:03.44,Default,,0,0,0,,-或是继王子的责任\N-什么？
# Dialogue: 0,0:12:03.76,0:12:04.68,Default,,0,0,0,,什么？
# Dialogue: 0,0:12:16.03,0:12:18.87,Default,,0,0,0,,你妹妹 快要撞树了
# Dialogue: 0,0:12:22.24,0:12:23.37,Default,,0,0,0,,克劳迪娅
# Dialogue: 0,0:12:25.12,0:12:26.91,Default,,0,0,0,,你好 卡勒姆
# Dialogue: 0,0:12:28.50,0:12:29.59,Default,,0,0,0,,你真无趣
# Dialogue: 0,0:12:31.79,0:12:32.88,Default,,0,0,0,,这是新树吗？
# Dialogue: 0,0:12:33.29,0:12:34.58,Default,,0,0,0,,相当新
# Dialogue: 0,0:12:35.30,0:12:37.97,Default,,0,0,0,,不过300年左右
# Dialogue: 0,0:12:41.97,0:12:45.27,Default,,0,0,0,,我们能再试试吗？我准备好了
# Dialogue: 0,0:12:56.57,0:12:57.53,Default,,0,0,0,,那是什么？
# Dialogue: 0,0:12:57.99,0:12:59.12,Default,,0,0,0,,我不知道
# Dialogue: 0,0:12:59.95,0:13:04.04,Default,,0,0,0,,-我想扫击你的脚\N-这不是剑击的动作
# Dialogue: 0,0:13:09.37,0:13:11.37,Default,,0,0,0,,我明白了
# Dialogue: 0,0:13:12.17,0:13:13.76,Default,,0,0,0,,别担心 我会帮你的
# Dialogue: 0,0:13:14.50,0:13:15.88,Default,,0,0,0,,你攻过来
# Dialogue: 0,0:13:19.80,0:13:21.34,Default,,0,0,0,,我被刺中了
# Dialogue: 0,0:13:21.43,0:13:23.56,Default,,0,0,0,,被王子刺中了
# Dialogue: 0,0:13:23.64,0:13:26.31,Default,,0,0,0,,王子殿下威武
# Dialogue: 0,0:13:26.72,0:13:28.85,Default,,0,0,0,,流血了 流血了！
# Dialogue: 0,0:13:29.98,0:13:31.77,Default,,0,0,0,,做得好 卡勒姆
# Dialogue: 0,0:13:32.48,0:13:33.82,Default,,0,0,0,,他活该
# Dialogue: 0,0:13:35.19,0:13:38.24,Default,,0,0,0,,卡勒姆王子 国王现在要见你
# Dialogue: 0,0:13:38.90,0:13:40.53,Default,,0,0,0,,他没有刺中我
# Dialogue: 0,0:13:51.83,0:13:53.83,Default,,0,0,0,,孩子们
# Dialogue: 0,0:13:54.25,0:13:58.17,Default,,0,0,0,,你要去班瑟小屋一趟
# Dialogue: 0,0:13:58.25,0:14:01.09,Default,,0,0,0,,现在是春天 一般冬天才去
# Dialogue: 0,0:14:01.88,0:14:03.84,Default,,0,0,0,,冬天快来了
# Dialogue: 0,0:14:04.09,0:14:05.09,Default,,0,0,0,,迟早的事
# Dialogue: 0,0:14:05.18,0:14:09.35,Default,,0,0,0,,去那边做什么 要有雪和冰才好玩
# Dialogue: 0,0:14:09.43,0:14:13.60,Default,,0,0,0,,或者你们会找到新的乐子
# Dialogue: 0,0:14:13.98,0:14:16.27,Default,,0,0,0,,搞个泥人什么的
# Dialogue: 0,0:14:16.77,0:14:19.86,Default,,0,0,0,,泥式速滑 应该很不错
# Dialogue: 0,0:14:23.86,0:14:26.32,Default,,0,0,0,,你们必须去
# Dialogue: 0,0:14:26.53,0:14:28.37,Default,,0,0,0,,-爸\N-已经决定了
# Dialogue: 0,0:14:28.99,0:14:31.83,Default,,0,0,0,,日落之前离开 去收拾一下
# Dialogue: 0,0:14:32.29,0:14:33.88,Default,,0,0,0,,遵命 来吧 艾斯兰
# Dialogue: 0,0:14:38.17,0:14:41.30,Default,,0,0,0,,他为何送我们走？有点不对头
# Dialogue: 0,0:14:41.38,0:14:44.59,Default,,0,0,0,,没事的 我肯定
# Dialogue: 0,0:14:52.18,0:14:53.43,Default,,0,0,0,,怎么了？父亲
# Dialogue: 0,0:14:54.94,0:14:56.94,Default,,0,0,0,,沙迪亚那边来了人
# Dialogue: 0,0:14:57.81,0:14:59.69,Default,,0,0,0,,不怀好意的访客
# Dialogue: 0,0:15:00.19,0:15:02.65,Default,,0,0,0,,什么人？吟游诗人吗？
# Dialogue: 0,0:15:02.74,0:15:05.95,Default,,0,0,0,,-刺客\N-我知道 我不是傻的
# Dialogue: 0,0:15:08.41,0:15:11.58,Default,,0,0,0,,在这附近他们有个落脚点
# Dialogue: 0,0:15:11.83,0:15:14.79,Default,,0,0,0,,-索伦 你负责带队攻击\N-好的
# Dialogue: 0,0:15:15.29,0:15:16.75,Default,,0,0,0,,那个落脚点
# Dialogue: 0,0:15:17.29,0:15:20.50,Default,,0,0,0,,我要怎么找到位置？
# Dialogue: 0,0:15:21.09,0:15:24.47,Default,,0,0,0,,这些刺客是月影精灵
# Dialogue: 0,0:15:25.13,0:15:27.13,Default,,0,0,0,,他们的力量来自于月亮
# Dialogue: 0,0:15:27.72,0:15:31.47,Default,,0,0,0,,盒子里是阿卡天使
# Dialogue: 0,0:15:31.56,0:15:33.06,Default,,0,0,0,,大只的月形飞蛾
# Dialogue: 0,0:15:33.64,0:15:35.60,Default,,0,0,0,,会追踪他们的能量
# Dialogue: 0,0:15:35.98,0:15:38.57,Default,,0,0,0,,跟着它 你就找到目标了
# Dialogue: 0,0:15:39.48,0:15:42.36,Default,,0,0,0,,如果我找不到会怎样？
# Dialogue: 0,0:15:42.44,0:15:45.65,Default,,0,0,0,,那我们就可能找一个新的领袖了
# Dialogue: 0,0:15:45.74,0:15:47.70,Default,,0,0,0,,你意思是他们会杀死国王？
# Dialogue: 0,0:15:57.67,0:16:00.76,Default,,0,0,0,,小声点 笨蛋 你想全世界都知道？
# Dialogue: 0,0:16:00.83,0:16:03.79,Default,,0,0,0,,-抱歉\N-快点出发 找到他们
# Dialogue: 0,0:16:04.13,0:16:06.01,Default,,0,0,0,,-在日落之前\N-那么
# Dialogue: 0,0:16:06.51,0:16:10.26,Default,,0,0,0,,如果真的是月影精灵\N一旦月亮升起
# Dialogue: 0,0:16:10.76,0:16:12.72,Default,,0,0,0,,他们是不可战胜的
# Dialogue: 0,0:16:13.31,0:16:15.56,Default,,0,0,0,,我去想想办法
# Dialogue: 0,0:16:15.72,0:16:19.35,Default,,0,0,0,,这个世界没有不可战胜的东西
# Dialogue: 0,0:16:19.52,0:16:21.52,Default,,0,0,0,,这话不对
# Dialogue: 0,0:16:21.61,0:16:23.82,Default,,0,0,0,,我是这样想的
# Dialogue: 0,0:16:31.07,0:16:32.28,Default,,0,0,0,,等等
# Dialogue: 0,0:16:33.28,0:16:34.57,Default,,0,0,0,,我跟你去
# Dialogue: 0,0:16:35.66,0:16:37.12,Default,,0,0,0,,你看起来很害怕
# Dialogue: 0,0:16:37.62,0:16:41.17,Default,,0,0,0,,顺便跟你说 你那是仪式用的盔甲
# Dialogue: 0,0:16:41.25,0:16:43.96,Default,,0,0,0,,3倍重量 一半的强度
# Dialogue: 0,0:16:44.29,0:16:45.79,Default,,0,0,0,,但确实华丽
# Dialogue: 0,0:16:46.38,0:16:49.88,Default,,0,0,0,,我不管 我知道发生什么 我要跟你去
# Dialogue: 0,0:16:49.97,0:16:53.81,Default,,0,0,0,,-你只是个孩子\N-还有2个月就满15岁了
# Dialogue: 0,0:16:53.89,0:16:56.64,Default,,0,0,0,,14岁又四分之三 哇
# Dialogue: 0,0:16:57.14,0:16:59.89,Default,,0,0,0,,是六分之五 他是我们的王
# Dialogue: 0,0:17:00.35,0:17:01.48,Default,,0,0,0,,还是我父亲
# Dialogue: 0,0:17:01.94,0:17:03.44,Default,,0,0,0,,我有责任去帮他
# Dialogue: 0,0:17:03.52,0:17:06.31,Default,,0,0,0,,他是你的后父
# Dialogue: 0,0:17:07.86,0:17:10.65,Default,,0,0,0,,当然这没什么区别 接着
# Dialogue: 0,0:17:13.95,0:17:15.74,Default,,0,0,0,,你应该能接住的
# Dialogue: 0,0:17:30.80,0:17:32.47,Default,,0,0,0,,经过了4次满月
# Dialogue: 0,0:17:32.97,0:17:37.10,Default,,0,0,0,,在冬天来临前 人类进入沙迪亚
# Dialogue: 0,0:17:37.18,0:17:39.68,Default,,0,0,0,,杀掉了龙族国王
# Dialogue: 0,0:17:39.77,0:17:42.06,Default,,0,0,0,,还毁掉了唯一的蛋
# Dialogue: 0,0:17:42.44,0:17:43.86,Default,,0,0,0,,龙王子
# Dialogue: 0,0:17:44.48,0:17:48.23,Default,,0,0,0,,今晚 我们要以血还血
# Dialogue: 0,0:17:48.73,0:17:50.07,Default,,0,0,0,,为自由呼吸！
# Dialogue: 0,0:17:50.32,0:17:52.16,Default,,0,0,0,,为真理而视！
# Dialogue: 0,0:17:52.49,0:17:54.03,Default,,0,0,0,,为荣誉而战！
# Dialogue: 0,0:17:54.49,0:17:56.45,Default,,0,0,0,,为正义流血！
# Dialogue: 0,0:17:57.33,0:17:59.21,Default,,0,0,0,,为沙迪亚用心！
# Dialogue: 0,0:18:02.96,0:18:04.46,Default,,0,0,0,,生命可贵
# Dialogue: 0,0:18:05.29,0:18:06.54,Default,,0,0,0,,生命脆弱
# Dialogue: 0,0:18:07.38,0:18:10.43,Default,,0,0,0,,我们可以牺牲 但不要无谓牺牲
# Dialogue: 0,0:18:16.22,0:18:20.60,Default,,0,0,0,,月亮轮转太阳 犹如死亡取代生命
# Dialogue: 0,0:18:34.45,0:18:37.25,Default,,0,0,0,,事成之后 我会派出影鹰
# Dialogue: 0,0:18:37.32,0:18:40.12,Default,,0,0,0,,带着盟誓带 回复龙族王后
# Dialogue: 0,0:18:40.83,0:18:43.33,Default,,0,0,0,,月亮最高时出击
# Dialogue: 0,0:18:46.96,0:18:48.80,Default,,0,0,0,,-路纳安\N-怎么了？瑞拉
# Dialogue: 0,0:18:49.50,0:18:50.67,Default,,0,0,0,,我想问
# Dialogue: 0,0:18:51.51,0:18:53.39,Default,,0,0,0,,他们知道我们要来会怎样？
# Dialogue: 0,0:18:53.47,0:18:55.60,Default,,0,0,0,,我们现在出其不意
# Dialogue: 0,0:18:56.09,0:18:59.72,Default,,0,0,0,,如果速度够快\N可以完成任务全身而退
# Dialogue: 0,0:19:16.07,0:19:18.74,Default,,0,0,0,,小饵 你藏匿和寻找的本事真差
# Dialogue: 0,0:19:21.33,0:19:22.58,Default,,0,0,0,,艾斯 你做什么？
# Dialogue: 0,0:19:23.08,0:19:26.71,Default,,0,0,0,,-你好 卡勒姆 你想要…\N-我不想吃啫喱
# Dialogue: 0,0:19:26.87,0:19:29.96,Default,,0,0,0,,你为何不去打包？我们要出远门
# Dialogue: 0,0:19:30.04,0:19:33.84,Default,,0,0,0,,-但你也没打包\N-我现在在做
# Dialogue: 0,0:19:36.13,0:19:38.13,Default,,0,0,0,,艾斯兰 你不明白吗？
# Dialogue: 0,0:19:38.59,0:19:43.14,Default,,0,0,0,,他们为何送走我们？因为有刺客
# Dialogue: 0,0:20:03.08,0:20:07.84,Default,,0,0,0,,看看这个月形飞蛾有没有效果
# Dialogue: 0,0:20:08.62,0:20:11.92,Default,,0,0,0,,-因为飞蛾吃衣服？\N-是的
# Dialogue: 0,0:20:23.14,0:20:24.06,Default,,0,0,0,,出发
# Dialogue: 0,0:20:46.54,0:20:47.71,Default,,0,0,0,,他们知道我们来了
# Dialogue: 0,0:20:54.25,0:20:55.92,Default,,0,0,0,,树匿术
# Dialogue: 0,0:21:20.82,0:21:21.86,Default,,0,0,0,,没发现
# Dialogue: 0,0:21:22.36,0:21:23.86,Default,,0,0,0,,真让人惊讶
# Dialogue: 0,0:21:23.95,0:21:27.45,Default,,0,0,0,,月形飞蛾就像一般飞蛾那样无用
# Dialogue: 0,0:21:33.17,0:21:35.59,Default,,0,0,0,,只能等月影精灵上门了
# Dialogue: 0,0:22:04.61,0:22:06.78,Default,,0,0,0,,你撒谎了
# Dialogue: 0,0:22:06.87,0:22:09.66,Default,,0,0,0,,-你放走了他\N-我很抱歉
# Dialogue: 0,0:22:10.08,0:22:13.54,Default,,0,0,0,,那个人类 我能从他眼睛看到恐惧
# Dialogue: 0,0:22:14.04,0:22:17.59,Default,,0,0,0,,当然他会恐惧 但你该完成任务
# Dialogue: 0,0:22:17.67,0:22:21.55,Default,,0,0,0,,但他都没有攻击我 我怎么取他性命
# Dialogue: 0,0:22:21.76,0:22:23.89,Default,,0,0,0,,你让他走了
# Dialogue: 0,0:22:23.97,0:22:25.47,Default,,0,0,0,,会害死我们全部人！
# Dialogue: 0,0:23:13.39,0:23:15.31,Default,,0,0,0,,字幕翻译：谢春明

