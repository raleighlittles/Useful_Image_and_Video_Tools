# Generate empty image

generate_empty_image_cmd = "convert -size {}X{} xc:black {}".format(width, height, empty_image_filename)

# Generate video from image
# t = duration
# r = frame rate
# scale = video dimensions
ffmpeg -loop 1 -i image.png -c:v libx264 -t 15 -pix_fmt yuv420p -vf scale=320:240 -r 30 out.mp4

# Write timestamp to video https://superuser.com/questions/1013753/how-can-i-overlay-the-captured-timestamp-onto-a-video-using-ffmpeg-in-yyyy-mm-dd

# Write frame number to video
https://stackoverflow.com/questions/15364861/frame-number-overlay-with-ffmpeg