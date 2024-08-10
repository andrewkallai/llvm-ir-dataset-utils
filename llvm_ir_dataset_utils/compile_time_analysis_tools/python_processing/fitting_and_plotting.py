# -*- coding: ascii -*-
import numpy as np
import matplotlib.pyplot as plt
from read_column import open_and_load
# Usage:
# from fitting_and_plotting import plot_functionality


def plot_functionality(lang: str, show: bool = False) -> None:
    '''
    Function to graph csv data for text segment size and instructions counts.
    '''
    textseg_data, inst_data = open_and_load(lang)
    c, b, a = np.polyfit(textseg_data, inst_data, 2)

    x_axis = range(min(textseg_data), max(textseg_data), 10)
    z = np.polyval([c, b, a], x_axis)

    plt.scatter(textseg_data, inst_data)
    plt.xscale("log")
    plt.yscale("log")
    plt.gca().set_ylim([10**8, 10**13])
    plt.xlabel("text_segment_size (bytes)")
    plt.ylabel("compiler_cpu_instructions_count")
    if (lang == "cpp"):
        plt.title("Clang++ Compiler Instructions vs. Text Segment Size ("+lang+")")
    else:
        plt.title("Clang Compiler Instructions vs. Text Segment Size ("+lang+")")
    plt.plot(x_axis, z, 'r')
    equation = f"${c:.1e}x^2 + {b:.1e}x + {a:.1e}$"
    plt.legend([f"fit: {equation}", "original"])
    if (show):
        plt.show()
    else:
        plt.savefig(fname=lang+"_instvtext.pdf", format="pdf")
