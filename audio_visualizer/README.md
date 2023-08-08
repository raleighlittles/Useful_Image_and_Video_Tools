Original command:

ffmpeg -i input.mp3 -filter_complex \
"[0:a]avectorscope=s=640x518,pad=1280:720[vs]; \
 [0:a]showspectrum=mode=separate:color=intensity:scale=cbrt:s=640x518[ss]; \
 [0:a]showwaves=s=1280x202:mode=line[sw]; \
 [vs][ss]overlay=w[bg]; \
 [bg][sw]overlay=0:H-h,drawtext=fontfile=/usr/share/fonts/TTF/Vera.ttf:fontcolor=white:x=10:y=10:text='\"Song Title\" by Artist'[out]" \
-map "[out]" -map 0:a -c:v libx264 -preset fast -crf 18 -c:a copy output.mkv

Things to add:

(NOT WORKING)
* adrawgraph: https://ffmpeg.org/ffmpeg-filters.html#toc-adrawgraph

```bash
$ ffmpeg -i input.mp3 -filter_complex \
"[0:a]adrawgraph=s=1500:500; \
 [vs][ss]overlay=w[bg]; \
-map "[out]" -map 0:a -c:v libx264 -preset fast -crf 18 -c:a copy output.mkv
```


```bash
$ ffmpeg -i input.mp3 -filter_complex "[0:a]adrawgraph=s=1500x500;" -map 0:a -c:v libx264 -preset fast -crf 18 -c:a copy output.mp4
```

* a3dscope: https://ffmpeg.org/ffmpeg-filters.html#toc-a3dscope [requires version 6.0]

* abitscope: https://ffmpeg.org/ffmpeg-filters.html#toc-abitscope

Worked with:

```bash
$ ffmpeg -i TomsDiner.mp3 -filter_complex "[0:a]abitscope" -map 0:a -c:v libx264 -preset fast -c:a copy output.mp4
```

* ahistogram: https://ffmpeg.org/ffmpeg-filters.html#toc-ahistogram

Worked with:


```bash
$ ffmpeg -i TomsDiner.mp3 -filter_complex "[0:a]ahistogram=dmode=separate" -map 0:a -c:v libx264 -preset fast -c:a copy output.mp4
```

* showcqt: https://ffmpeg.org/ffmpeg-filters.html#toc-showcqt

Works with: 

```bash
$ ffmpeg -i TomsDiner.mp3 -filter_complex "[0:a]showcqt" -map 0:a -c:v libx264 -preset fast -c:a copy output.mp4
```

* showfreqs: https://ffmpeg.org/ffmpeg-filters.html#toc-showfreqs

Worked, tested with: 

```bash
$ ffmpeg -i TomsDiner.mp3 -filter_complex "[0:a]showfreqs" -map 0:a -c:v libx264 -preset fast -c:a copy output.mp4
```

# Dimensions


7 pieces total, so use a 2-row grid of 3 on the top row and 4 on the bottom.