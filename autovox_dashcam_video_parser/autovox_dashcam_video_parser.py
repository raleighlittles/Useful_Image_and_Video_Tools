import argparse
import datetime
import os
import shutil
import subprocess

argparse_parser = argparse.ArgumentParser()

argparse_parser.add_argument("-i", "--input-dir", type=str, help="The directory where video files are located")
argparse_parser.add_argument("-f", "--input-formats", nargs='+', help="The file extension(s) used for videos")
argparse_parser.add_argument("-o", "--output-dir", type=str, help="The directory where videos will be moved to, after processing")

argparse_args = argparse_parser.parse_args()

dashcam_dir = os.fsencode(argparse_args.input_dir).decode()

for file in os.listdir(dashcam_dir):
    filename = os.fsdecode(file)
    rel_filename = os.path.join(dashcam_dir, filename)

    if any([filename.lower().endswith(ext.lower()) for ext in argparse_args.input_formats]):

        # Test to make sure the video isn't corrupted, by checking the video's duration
        # If it comes back as anything other than at least one second, it's likely invalid/corrupted
        ffmpeg_duration_cmd = "ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {}".format(rel_filename)

        ffmpeg_result = subprocess.run(ffmpeg_duration_cmd.split(), stdout=subprocess.PIPE)

        video_duration = ffmpeg_result.stdout.decode().strip()

        # If the video is corrupt, delete it and move on
        if (video_duration == "") or (float(video_duration) < 1):
            print("Video is corrupted or invalid -- deleting now")
            os.remove(rel_filename)
            continue


        print("Valid video file found [ {} ] ".format(filename))
            
        # Next step: look for the existence of the current or previous year anywhere in the filename.
        # If found, the file (probably) already has the date in the filename -- no need to do anything.
        # If not found, append the file inode's last-modified date to the filename, since this is the closest thing to a timestamp
        # that we have

        current_year = int(datetime.datetime.today().strftime("%Y"))

        # Dashcams don't use the DCIM interface, and the filenames usually start with the timestamp, but the timestamp
        # can have different formats. This is my best guess at assuming whether the filename contains a timestamp
        if not filename.startswith("20"):
            file_modified_time_cmd = "stat -c '%y' {}".format(rel_filename)
            
            # The full timestamp returned by stat looks like (with single quote and all): '2022-06-03 00:21:09.044891968 -0700'
            file_modified_time_cmd_result = subprocess.run(file_modified_time_cmd.split(), stdout=subprocess.PIPE)

            # Remove timezone and microseconds from timestamp, as well as leading single-quote
            file_modified_date, file_modified_time, _ = file_modified_time_cmd_result.stdout.decode().split()

            # Some file systems don't allow colons
            new_filename = "{}_{}".format(file_modified_date[1:] + "_" + file_modified_time.split(".")[0].replace(":", "") + "_", filename)
            
            shutil.move(os.path.join(dashcam_dir, filename), os.path.join(dashcam_dir, new_filename))

            # Update the filenames variable after the rename, because it's going to be used later
            filename, rel_filename = new_filename, os.path.join(dashcam_dir, new_filename)
            print("Appended timestamp to video file")


        # Use ExifTool to check if the video file contains GPS information embedded in it

        exiftool_gps_tag_cmd = "exiftool -ee -G3 {}".format(rel_filename)
        gps_tag_names = ["GPS Date/Time", "GPS Latitude", "GPS Longitude"]
        exiftool_check_gps_result = subprocess.run(exiftool_gps_tag_cmd.split(), stdout=subprocess.PIPE)

        if all([tag_name in exiftool_check_gps_result.stdout.decode() for tag_name in gps_tag_names]):

            print("Video file contains GPS data, extracting..")

            # If it does, extract the GPS data to a CSV file in the output folder
            csv_filename = filename + ".csv"

            # 2 'q' for quiet option, to suppress warnings about certain frames in the video missing GPS data
            exiftool_extract_gps_cmd = """exiftool -ee -q -q -p ' SampleTime $SampleTime GPS-DateTime $GPSDateTime Coordinates $GPSLatitude $GPSLongitude ' {}""".format(rel_filename)

            # Usually you would redirect the result of this command out to a CSV file (via '>'), but redirection doesn't work in Python's shell mode
            with open(os.path.join(argparse_args.output_dir, csv_filename), 'wb') as csv_file_handle:
                # Using shell mode is a 'security risk', but I couldn't get it to work without
                p = subprocess.Popen(exiftool_extract_gps_cmd, stdout=csv_file_handle, shell=True)
                p.communicate()

        # Lastly, move the file to the destination location
        shutil.move(rel_filename, os.path.join(argparse_args.output_dir, filename))

    else:
        print("Non-video file found [[ {} ]] - removing now".format(filename))
        os.remove(os.path.join(dashcam_dir, filename))
