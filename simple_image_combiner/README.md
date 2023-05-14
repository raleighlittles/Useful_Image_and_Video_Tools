# About

This is a simple Python script that uses ImageMagick's [convert](https://imagemagick.org/script/convert.php) script to concatenate images. This is useful for quickly creating mosaic/tiled output from a directory of images.

Here's an example of one output, created from 24 separate images:

![test-output-image](https://i.imgur.com/MYJZs0J.jpg)

# Setup

## Dependencies

* ImageMagick:

```bash
$ sudo apt install imagemagick
```

## Usage

```
usage: image_combiner.py [-h] [-i INPUT_DIR] [-o OUTPUT_DIR] [--force-square | --no-force-square]
                         [-r NUM_ROWS] [-c NUM_COLS]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_DIR, --input-dir INPUT_DIR
                        Directory where input images are stored.
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Directory where output images will be stored
  --force-square, --no-force-square
                        If number of images is an evenly divisible number, then concatenate the images in
                        such a way that a square is produced. 0 for false, 1 for true
  -r NUM_ROWS, --num-rows NUM_ROWS
                        Number of rows in concatenated image
  -c NUM_COLS, --num-cols NUM_COLS
                        Number of columns in concatenated image
```

To generate the test image shown above, I ran:

```bash
$ python3 image_combiner.py -i=input -o=output -r=4 -c=6
```

Make sure your directories are created before you run them.


# Troubleshooting

## Empty output file, error 'width or height exceeds limit'

If you get an error that looks like:

```
convert-im6.q16: width or height exceeds limit
```

This is because ImageMagick has an unreasonably low default setting for the maximum image size it can handle. Thankfully, you can change these defaults by editing the ImageMagick settings file.

See here: https://askubuntu.com/questions/1041349/imagemagick-command-line-convert-limit-values
