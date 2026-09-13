from pathlib import Path

from frequency_analysis import display_frequency_analysis
from word_frequency_analysis import display_word_frequency_analysis
from pattern_analysis import display_pattern_analysis


def read_ciphertext(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


base_dir = Path(__file__).resolve().parent.parent

ciphertext_file = base_dir / "outputs" / "ciphertext.txt"

ciphertext = read_ciphertext(ciphertext_file)

display_frequency_analysis(ciphertext)

display_word_frequency_analysis(ciphertext)

display_pattern_analysis(ciphertext)