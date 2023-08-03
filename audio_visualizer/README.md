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

ffmpeg -i input.mp3 -filter_complex \
"[0:a]adrawgraph=s=1500:500; \
 [vs][ss]overlay=w[bg]; \
-map "[out]" -map 0:a -c:v libx264 -preset fast -crf 18 -c:a copy output.mkv

ffmpeg -i input.mp3 -filter_complex "[0:a]adrawgraph=s=1500x500;" -map 0:a -c:v libx264 -preset fast -crf 18 -c:a copy output.mp4


* a3dscope: https://ffmpeg.org/ffmpeg-filters.html#toc-a3dscope
* abitscope: https://ffmpeg.org/ffmpeg-filters.html#toc-abitscope
* ahistogram: https://ffmpeg.org/ffmpeg-filters.html#toc-ahistogram
* showcqt: https://ffmpeg.org/ffmpeg-filters.html#toc-showcqt
* showfreqs: https://ffmpeg.org/ffmpeg-filters.html#toc-showfreqs

# Dimensions

* Vectorscope: 800x800
* showspectrum: 800x800
* showwaves: 1500x500
--
* adrawgraph: