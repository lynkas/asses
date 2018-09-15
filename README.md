# asses
Ass subtitles combine and trim script

处理字幕的时候用的，是即有中文字幕又有英文字幕的情况。这个脚本会自动处理从ffmpeg中提取的ass字幕：

`ffmpeg -i video.mkv sub.ass`

将两个字幕合成一组。

`asses.py 上面的字幕.ass 下面的字幕.ass`

就会变成类似于字幕组的中英文字幕的形式，新的字幕的文件名为

`上面的字幕.ass.COM.ass`
