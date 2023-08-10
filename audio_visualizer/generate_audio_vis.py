import argparse
import subprocess
import os
import threading

def main_generate_visualization(input_audio_filename : str, output_folder : str):

    output_video_file_basename = os.path.join(output_folder, input_audio_filename + "_output_")

    # https://stackoverflow.com/a/2883627/1576548
    
    gen_video_tasks = [ generate_vectorscope, generate_spectrum, generate_waves_diagram, generate_bitscope, generate_audio_histogram, generate_constant_q_transform, generate_power_spectrum ]

    for task in gen_video_tasks:
        thr = threading.Thread(target=task, args=(input_audio_filename, output_video_file_basename))
        thr.start()


def generate_vectorscope(audio_filename, output_video_filename):
    """
    https://en.wikipedia.org/wiki/Vectorscope
    """
    
    cmd = f"ffmpeg -i {audio_filename} -filter_complex \"[0:a]avectorscope=draw=line\" -map 0:a -c:v libx265 -x265-params lossless=1 {output_video_filename}_vectorscope.mp4"

def generate_spectrum(audio_filename, output_video_filename):
    
    cmd = f"ffmpeg -i {audio_filename} -filter_complex \"[0:a]showspectrum=mode=separate\" -map 0:a -c:v libx265 -x265-params lossless=1 {output_video_filename}_spectrum.mp4"

def generate_waves_diagram(audio_filename, output_video_filename):
    
    cmd = f"ffmpeg -i {audio_filename} -filter_complex \"[0:a]showwaves=split_channels=1:draw=full\" -map 0:a -c:v libx265 -x265-params lossless=1 {output_video_filename}_waves.mp4"

def generate_graph(audio_filename):
    pass # only supported by ffmpeg v6.0+

def generate_bitscope(audio_filename, output_video_filename):

    cmd = f"ffmpeg -i {audio_filename} -filter_complex \"[0:a]abitscope=rate=60\" -map 0:a -c:v libx265 -x265-params lossless=1 {output_video_filename}_bitscope.mp4"

def generate_audio_histogram(audio_filename, output_video_filename):

    cmd = f"ffmpeg -i {audio_filename} -filter_complex \"[0:a]ahistogram=dmode=separate\" -map 0:a -c:v libx265 -x265-params lossless=1 {output_video_filename}_histogram.mp4"

def generate_constant_q_transform(audio_filename, output_video_filename):
    
    """
    https://en.wikipedia.org/wiki/Constant-Q_transform
    """
    
    cmd = f"ffmpeg -i {audio_filename} -filter_complex \"[0:a]showcqt=csp=bt709\" -map 0:a -c:v libx265 -x265-params lossless=1 {output_video_filename}_frequency-spectrum.mp4"

def generate_power_spectrum(audio_filename, output_video_filename):

    cmd = f"ffmpeg -i {audio_filename} -filter_complex \"[0:a]showfreqs=cmode=separate\" -map 0:a -c:v libx265 -x265-params lossless=1 {output_video_filename}_power-spectrum.mp4"


## ------------------------------------------------------ ##

if __name__ == "__main__":
    argparse_parser = argparse.ArgumentParser()

    argparse_parser.add_argument("-i", "--input-audio-filename", type=str, required=True,
                                 help="The audio file to be visualized")
    argparse_parser.add_argument("-o", "--output-folder", type=str, required=True,
                                 help="The folder where the created videos will be stored")

    argparse_args = argparse_parser.parse_args()