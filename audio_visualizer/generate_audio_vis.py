import argparse


def main_generate_visualization(input_audio_filename : str) -> str:
    pass


def generate_vectorscope(audio_filename):
    pass

def generate_spectrum(audio_filename):
    pass

def generate_waves_diagram(audio_filename):
    pass

def generate_graph(audio_filename):
    pass


def generate_bitscope(audio_filename):
    pass

def generate_audio_histogram(audio_filename):
    pass

def generate_freq_spectrum_cqt(audio_filename):
    pass

def generate_power_spectrum(audio_filename):
    pass

if __name__ == "__main__":
    argparse_parser = argparse.ArgumentParser()

    argparse_parser.add_argument("-i", "--input-audio-filename", type=str, required=True,
                                 help="The audio file to be visualized")

    argparse_args = argparse_parser.parse_args()


