import argparse
import os
import sys
import typing
import math
import random
import subprocess
import string
import pdb

def get_output_files(output_directory : str, image_extensions : typing.List) -> typing.List:
  
    return [os.path.join(output_directory, filename) for filename in os.listdir(output_directory) if any([filename.endswith(".{}".format(ext)) for ext in image_extensions])]

def generate_concat_command(files : typing.List, output_directory, horizontal : bool) -> str:

    convert_cmd = "convert "

    convert_cmd += " ".join(files)

    if horizontal:
        convert_cmd += " +"

    else:
        convert_cmd += " -"

    convert_cmd += "append "

    # The resulting file takes the extension of the last filename in the list
    file_ext = os.path.splitext(files[-1])[1][1:]

    # Output file name consists of a random 10-letter string (it will be deleted later once the final image is created)
    output_filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) + "." + file_ext

    convert_cmd += os.path.join(output_directory, output_filename)

    print("Running command ", convert_cmd)

    return convert_cmd

def concatenate_images_in_row_or_column(files: typing.List, output_directory : str,  is_row: bool):
    
    concat_cmd = generate_concat_command(files, output_directory, is_row)

    p = subprocess.Popen(concat_cmd, shell=True)
    p.communicate()
    
def main_combine_images(input_dir : str, output_dir : str, force_square : bool, num_rows : int, num_cols : int):
  
  # Before doing anything, make sure that the `convert` utility is installed
  imagemagick_test_cmd = subprocess.Popen("convert --version", shell=True)
  imagemagick_test_cmd.wait()

  if (imagemagick_test_cmd.returncode != 0):
      print("[ERROR] imagemagick test command failed, please make sure it's installed and in your PATH")
      return 1

 
  all_files = []

  image_extensions = ['jpg', 'jpeg', 'png', 'tiff', 'tif', 'webp']

  for filename in os.listdir(input_dir):
      rel_filename = os.path.join(input_dir, filename)
      file_extension = os.path.splitext(rel_filename)[1][1:]

      if file_extension.lower() in image_extensions:
          print("[DEBUG] Adding image {} to list".format(filename))
          all_files.append(rel_filename)

  num_files = len(all_files)

  print(num_files, " images ready to be concatenated")

  # Sanity check: if the user asked us to construct a square image, did they provide a square-number of images?
  if (force_square) and (math.isqrt(num_files) ** 2 != num_files):

      print("ERROR: Can't create a square out of {} images".format(len(all_files)))
      return 2


  # Sanity check: did user pass in a valid value for the number of rows and columns (if they didn't already say to create a square)
  if (not force_square) and ((num_rows * num_cols) != num_files):

      print("ERROR: {} images total, so {} and {} are not valid row column numbers".format(num_files, num_rows, num_cols))
      return 1

  num_rows = num_rows if (num_rows is not None) else (math.isqrt(num_files))
  num_cols = num_cols if (num_cols is not None) else (math.isqrt(num_files))

  # The first two cases are simple -- the user wants all images concatenated in a single row or column
  if num_rows == 1:
      concatenate_images_in_row_or_column(all_files, output_dir, True)

  elif num_cols == 1:
      concatenate_images_in_row_or_column(all_files, output_dir, False)

  else:
      for file_num in range(0, num_files, num_cols):

          files_in_row = all_files[file_num : file_num + num_cols]
          convert_cmd = concatenate_images_in_row_or_column(files_in_row, output_dir, True)

      # Now that the rows have been generated, concatenate those rows vertically
      intermediate_files = get_output_files(output_dir, image_extensions)
      concatenate_images_in_row_or_column(intermediate_files, output_dir, False)
      
  print("[DEBUG] Cleaning up {} intermediate files".format(len(intermediate_files)))
  [os.remove(file) for file in intermediate_files]

if __name__ == "__main__":
  argparse_parser = argparse.ArgumentParser()

  argparse_parser.add_argument("-i", "--input-dir", type=str, help="Directory where input images are stored.")
  argparse_parser.add_argument("-o", "--output-dir", type=str, help="Directory where output images will be stored")
  argparse_parser.add_argument("--force-square", action=argparse.BooleanOptionalAction, help="If number of images is an evenly divisible number, then concatenate the images in such a way that a square is produced. 0 for false, 1 for true")
  argparse_parser.add_argument("-r", "--num-rows", type=int, help="Number of rows in concatenated image")
  argparse_parser.add_argument("-c", "--num-cols", type=int, help="Number of columns in concatenated image")

  argparse_args = argparse_parser.parse_args()
  
  main_combine_images(argparse_args.input_dir, argparse_args.output_dir, argparse_args.force_square, argparse_args.num_rows, argparse_args.num_cols)

