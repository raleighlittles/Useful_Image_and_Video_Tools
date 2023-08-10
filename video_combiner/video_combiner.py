import argparse
import collections
import subprocess
import pdb
import os
import sys
import typing


def combine_videos(input_dir: str, input_formats: typing.List, output_prefix: str):

    # Before doing anything, make sure that ffmpeg is installed
    ffmpeg_test_cmd = subprocess.Popen("ffmpeg -version", shell=True)
    ffmpeg_test_cmd.wait()

    if (ffmpeg_test_cmd.returncode != 0):
        print("[ERROR] ffmpeg test command failed, please make sure it's installed and in your PATH")
        return 1

    video_resolutions_and_filenames = collections.defaultdict(list)

    # Iterate over files in directory, creating a dictionary where the keys are resolutions and the values are lists of filenames for videos having that resolution
    for file in os.listdir(input_dir):

        filename = os.fsdecode(file)
        full_filename = os.path.join(input_dir, filename)

        if any([filename.lower().endswith(ext.lower()) for ext in input_formats]):

            ffmpeg_get_resolution_cmd = "ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 \'{}\'".format(
                full_filename)

            try:
                ffmpeg_resolution_cmd_result = subprocess.check_output(
                    ffmpeg_get_resolution_cmd, shell=True)

            except subprocess.CalledProcessError as ffmpeg_exec:
                print("Encountered FFMPEG error checking file resolution for {} File may not be valid or is somehow corrupt, deleting it now.".format(filename))
                os.remove(full_filename)
                continue

            # In the form: "<width>x<height>", ie. "3840x2160"
            video_resolution = ffmpeg_resolution_cmd_result.decode().strip()

            video_resolutions_and_filenames[video_resolution].append(
                full_filename)

    for video_resolution, video_filenames in video_resolutions_and_filenames.items():

        num_videos_at_resolution = len(video_filenames)

        if num_videos_at_resolution > 1:

            print("{} videos found at resolution {}".format(
                num_videos_at_resolution, video_resolution))

            # Construct intermediate file
            with open("intermediate.txt", 'a') as text_file:
                for filename in video_filenames:
                    text_file.write("file '{}'\n".format(filename))

            # Now that the file is ready, run the command
            ffmpeg_concat_cmd = "ffmpeg -f concat -safe 0 -i intermediate.txt -c copy combined-video-{}-{}.mp4".format(
                output_prefix, video_resolution)

            try:
                ffmpeg_concat_cmd_result = subprocess.check_output(
                    ffmpeg_concat_cmd, shell=True)

            except subprocess.CalledProcessError as ffmpeg_exc:
                print("Encountered error concatenating videos ", ffmpeg_exc)
                return 2

            finally:
                os.remove("intermediate.txt")

        elif (num_videos_at_resolution == 1):
            print("Only one video found at resolution {}, nothing to combine".format(
                video_resolution))
            
        else:
            print("[ERROR] Invalid number of videos found for resolution {}".format(video_resolution))
            return 2

if __name__ == "__main__":
    argparse_parser = argparse.ArgumentParser()
    argparse_parser.add_argument(
        "-i", "--input-dir", type=str, help="The directory where video files are located")
    argparse_parser.add_argument(
        "-f", "--input-formats", nargs='+', help="The file extension(s) used for videos")
    argparse_parser.add_argument("-o", "--output-prefix", type=str,
                                 help="A prefix to attach to each generated output file")

    argparse_args = argparse_parser.parse_args()

    combine_videos(os.fsencode(argparse_args.input_dir).decode(),
                   argparse_args.input_formats, argparse_args.output_prefix)
