import argparse
import os
import subprocess
import sys
import json
import pdb
import re

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
        print(f"Error running ffmpeg command to create blank video: {generate_empty_video_cmd}")
        sys.exit(3)

    return blank_video_filename


def draw_info_onto_video(input_video_filename, additional_info) -> str:

    output_video_filename = "metadata_video.mp4"

    draw_info_on_video_cmd = f"ffmpeg -i {input_video_filename} -vf \"drawtext=fontfile=Arial.ttf: text='%{{pts \:flt}} | %{{frame_num}} \n {additional_info}': start_number=1: x=(w-tw)/2: y=h-(2*lh): fontcolor=white: fontsize=20: box=1: boxcolor=black: boxborderw=5\" {output_video_filename}"

    if subprocess.run(draw_info_on_video_cmd, shell=True).returncode != 0:
        print(f"Error drawing info onto video. Command ran was: {draw_info_on_video_cmd}")
        sys.exit(4)

    return output_video_filename

def stitch_video_bar(original_filename, video_bar_filename):

    # This command performs a re-encoding, because "filtering and streamcopy cannot be used together"
    combine_vids_vertically_cmd = f"ffmpeg -i {original_filename} -i {video_bar_filename} -filter_complex vstack=inputs=2 output.mp4"

    if subprocess.run(combine_vids_vertically_cmd.split(), stdout=subprocess.PIPE).returncode != 0:
        print(f"Error running ffmpeg command to stitch videos: {combine_vids_vertically_cmd}")
        sys.exit(5)

def get_input_video_params(input_video_filename) -> tuple:
    """
    Get the input video's:
    (1) width
    (2) height
    (3) duration
    (4) frame rate
    """

    ffprobe_get_video_props_cmd = f"ffprobe -v error -select_streams v -show_entries stream=width,height,duration,r_frame_rate -of json {input_video_filename}"

    # Outputs something like:
    """
    {
    "programs": [

    ],
    "streams": [
        {
            "width": 640,
            "height": 480,
            "r_frame_rate": "25/1",
            "duration": "16.600000"
        }
    ]
    }
    """

    video_props_json = subprocess.run(ffprobe_get_video_props_cmd.split(), stdout=subprocess.PIPE).stdout.decode().strip()

    # '0' to indicate the first (and only!) video stream,
    # while multi-video-stream files are technically supported by FFMPEG, we don't allow them
    # here since they're nonsensical
    video_props = json.loads(video_props_json)["streams"][0]


    video_width = int(video_props["width"])
    video_height = int(video_props["height"])
    video_frame_rate = eval(video_props["r_frame_rate"])
    video_duration = float(video_props["duration"])

    return tuple([video_width, video_height, video_duration, video_frame_rate])

# ----- End helper functions

def create_video_metadata_bar_from_file(input_txt_filename, input_video_filename):

    width, height, duration, frame_rate = get_input_video_params(input_video_filename)

    metadata_video_filename = create_video_metadata_bar(width, height, duration, frame_rate, input_txt_filename)
    
    stitch_video_bar(input_video_filename, metadata_video_filename)


def create_video_metadata_bar(width, height, duration, framerate, input_txt_filename) -> str:

    img_filename = create_empty_image(width, height)

    # The metadata bar is 1/5 of the height of the original video
    video_filename = create_video_of_duration_from_image(img_filename, width, height / 5, duration, framerate, "video.mp4")

    extra_onscreen_txt = ""
    
    with open(input_txt_filename, 'r') as input_txt_file:
        extra_onscreen_txt = input_txt_file.readlines()

    metadata_video_filename = draw_info_onto_video(video_filename, " ".join(x.replace("\r", " ").replace("\n", " ") for x in extra_onscreen_txt))

    return metadata_video_filename


if __name__ == "__main__":
    
    argparse_parser = argparse.ArgumentParser()

    argparse_parser.add_argument("-w", "--width", type=int, help="Width of video (in pixels)")
    argparse_parser.add_argument("-v", "--height", type=int, help="Height/vertical measurement of video")
    argparse_parser.add_argument("-d", "--duration", type=int, help="Video duration")
    argparse_parser.add_argument("-f", "--frame-rate", type=str, help="The frame rate of the input video, for the output video to match")
    argparse_parser.add_argument("-t", "--text_filename", type=str, help="A text file containing text to be added to the video")
    argparse_parser.add_argument("-i", "--input-video-filename", type=str, help="The video to attach the metadata data to")

    argparse_args = argparse_parser.parse_args()

    if argparse_args.input_video_filename:
        create_video_metadata_bar_from_file(argparse_args.text_filename, argparse_args.input_video_filename)

    else:
        # Manual mode
        create_video_metadata_bar(argparse_args.width, argparse_args.height, argparse_args.duration, argparse_args.frame_rate, argparse_args.text_filename)

