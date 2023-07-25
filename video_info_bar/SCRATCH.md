# Generate empty image

generate_empty_image_cmd = "convert -size {}X{} xc:black {}".format(width, height, empty_image_filename)

# Generate video from image
# t = duration
# r = frame rate
# scale = video dimensions
ffmpeg -loop 1 -i image.png -c:v libx264 -t 15 -pix_fmt yuv420p -vf scale=320:240 -r 30 out.mp4

# Write timestamp to video https://superuser.com/questions/1013753/how-can-i-overlay-the-captured-timestamp-onto-a-video-using-ffmpeg-in-yyyy-mm-dd
ffmpeg -i in.webm -filter_complex "drawtext=fontfile=/usr/share/fonts/truetype/arial.ttf: text='%{pts \:flt}': x=100 : y=50 : box=1" -c:a copy out.webm

# Write frame number to video
https://stackoverflow.com/questions/15364861/frame-number-overlay-with-ffmpeg

ffmpeg -i input -vf "drawtext=fontfile=Arial.ttf: text='%{frame_num}': start_number=1: x=(w-tw)/2: y=h-(2*lh): fontcolor=black: fontsize=20: box=1: boxcolor=white: boxborderw=5" -c:a copy output

# Stitch videos vertically

ffmpeg -i input0 -i input1 -filter_complex vstack=inputs=2 output

https://stackoverflow.com/a/33764934/1576548