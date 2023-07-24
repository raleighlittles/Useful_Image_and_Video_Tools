import argparse
import os
import subprocess
import sys


def create_empty_image(width, height) -> str:
    """
    Creates an empty image of a given dimension, returning the filename to the output image
    """

    empty_image_filename = "empty.jpg"

    generate_black_empty_img_cmd = "convert -size {}X{} xc:black {}".format(width, height, empty_image_filename)

    if subprocess.run(generate_black_empty_img_cmd.split(), stdout=subprocess.PIPE).returncode != 0:
        print(f"Error running convert cmd to generate empty image, make sure you have ImageMagick installed. Command ran: {generate_black_empty_img_cmd}")
        sys.exit(2)

    return empty_image_filename

def create_video_of_duration_from_image(image_filename, width, height, duration, framerate, video_filename) -> str:

    blank_video_filename = "blank_video.mp4"

    generate_empty_video_cmd = f"ffmpeg -loop 1 -i {image_filename} -c:v libx264 -t {duration} -r {float(framerate)} {blank_video_filename}"

    if subprocess.run(generate_empty_video_cmd.split(), stdout=subprocess.PIPE).returncode != 0:
        print(f"Error running ffmpeg command: {generate_empty_video_cmd}")
        sys.exit(3)

    return blank_video_filename


def create_video_metadata_bar(width, height, duration, frame_rate) -> str:

    img_filename = create_empty_image(width, height)

    video_filename = create_video_of_duration_from_image(img_filename, width, height, duration, frame_rate, "video.mp4")



if __name__ == "__main__":
    
    argparse_parser = argparse.ArgumentParser()

    argparse_parser.add_argument("-w", "--width", type=int, required=True, help="Width of video (in pixels)")
    argparse_parser.add_argument("-v", "--height", type=int, required=True, help="Height/vertical measurement of video")
    argparse_parser.add_argument("-d", "--duration", type=int, required=True, help="Video duration")
    argparse_parser.add_argument("-f", "--frame-rate", type=str, required=True, help="The frame rate of the input video, for the output video to match")
    # argparse_parser.add_argument  TEXT FILE LOCATION FOR TITLE/LOCATION/ETC

    argparse_args = argparse_parser.parse_args()

    create_video_metadata_bar(argparse_args.width, argparse_args.height, argparse_args.duration, argparse_args.frame_rate)
