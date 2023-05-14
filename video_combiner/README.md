# About

This is a simple script that uses [FFMPEG](https://ffmpeg.org/) to concatenate videos.

For FFMPEG to be able to concatenate videos, the videos must have the same dimensions, so this tool first sorts videos by their resolution, and then combines them all, e.g. 3 1080p videos and 5 4K videos will produce 2 videos total, one 1080p video and one 4K video.

# Usage

```bash
$ python3 video_combiner.py --help

```
