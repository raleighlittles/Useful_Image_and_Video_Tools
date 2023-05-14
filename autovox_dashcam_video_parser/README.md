# About

This simple tool is used for copying over dashcam videos and extracting GPS information from them. I wrote this tool initially for use with my AUTO VOX X2, but it should work with any dashcam.

The process the script uses is described below:

Files matching the given extension are examined and checked for the following criteria:

1. Is the video duration non-zero? If not, the file is removed. (This removes corrupted video files)

2. Does the filename (likely) contain a timestamp? If not, the [file modified](https://en.wikipedia.org/wiki/Inode#POSIX_inode_description) timestamp is added to the filename.

3. Does the video have GPS data embedded in it? If so, the GPS data are extracted via  [EXIFtool](https://exiftool.org/) and stored in a CSV file.

Lastly, the video file is moved to the specified location.

# Usage

```
python3 autovox_dashcam_video_parser.py --help                                                         ─╯
usage: autovox_dashcam_video_parser.py [-h] [-i INPUT_DIR] [-f INPUT_FORMATS [INPUT_FORMATS ...]]
                                       [-o OUTPUT_DIR]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_DIR, --input-dir INPUT_DIR
                        The directory where video files are located
  -f INPUT_FORMATS [INPUT_FORMATS ...], --input-formats INPUT_FORMATS [INPUT_FORMATS ...]
                        The file extension(s) used for videos
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        The directory where videos will be moved to, after processing
```

# Dependencies

* EXIFTool: https://exiftool.org/
* FFProbe (part of FFMPEG): https://ffmpeg.org/
