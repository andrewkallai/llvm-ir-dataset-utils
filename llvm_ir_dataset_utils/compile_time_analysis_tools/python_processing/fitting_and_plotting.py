"""
Utilies for plotting instruction counts & text segment size scatter plots, as well as instruction counts histograms.

plot_instruction_counts_v_textseg
  Returns: None
  Example Usage: plot_instruction_counts_v_textseg("c", "/tmp", show=True)

 plot_instruction_counts_histograms
  Returns: None
  Example Usage: plot_instruction_counts_histograms("c", "/tmp", show=True)
"""
import matplotlib.pyplot as plt
from read_column import pandas_df_with_outlier_scores

def plot_instruction_counts_v_textseg(lang: str, storage: str, show: bool = False) -> None:
    import numpy as np
    df = pandas_df_with_outlier_scores(lang, storage)
    textseg_data = df["text_segment"]
    inst_data = df["instruction"]
    c, b, a = np.polyfit(textseg_data, inst_data, 2)

    x_axis = range(min(textseg_data), max(textseg_data), 10)
    z = np.polyval([c, b, a], x_axis)

    plt.scatter(textseg_data, inst_data)
    plt.xscale("log")
    plt.yscale("log")
    plt.gca().set_ylim([10**8, 10**13])
    plt.gca().set_xlim([10**(-1), 10**9])
    plt.xlabel("Text Segment Size (bytes)")
    plt.ylabel("Compiler CPU Instructions Count")
    if (lang == "cpp"):
        plt.title("Clang++ Compiler Instructions vs. Text Segment Size ("+lang+")")
    else:
        plt.title("Clang Compiler Instructions vs. Text Segment Size ("+lang+")")
    plt.plot(x_axis, z, 'r')
    equation = f"${c:.1e}x^2 + {b:.1e}x + {a:.1e}$"
    plt.legend([f"fit: {equation}", "original"])
    if (show):
        print(len(textseg_data))
        plt.show()
    else:
        plt.savefig(fname=lang+"_instvtext.pdf", format="pdf")
    plt.close()


def plot_instruction_counts_histograms(lang: str, storage: str, show: bool = False) -> None:
    df = pandas_df_with_outlier_scores(lang, storage)
    inst_data = df["instruction"]
    plt.hist(inst_data, bins='auto', alpha=1, color='b')
    plt.title("Histogram of Compiler Instructions ("+lang+")")
    plt.xscale("log")
    plt.yscale("log")
    plt.gca().set_ylim([10**(-1), 10**5])
    plt.gca().set_xlim([10**8, 10**13])
    plt.xlabel('Compiler CPU Instructions Count')
    plt.ylabel('No. of IR Files')

    plt.text(max(inst_data), 1.1, format(max(inst_data), '.2e'), ha='center')

    if (show):
        print(len(inst_data))
        plt.show()
    else:
        plt.savefig(fname=lang+"_hist.pdf", format="pdf")
    plt.close()

def print_outlier_rows(lang: str, storage: str, show) -> None:
  df = pandas_df_with_outlier_scores(lang, storage)
  outl = df.nlargest(10, "outlier_scores")
#  print(outl.to_string(index=False))
  outl.style.hide_index()
  print(outl)
#  cols = outl.loc[:, "BasicBlockCount":"CallWithPointerArgumentCount"]

#  for col in cols:
#        non_zero_values = outl[col][outl[col] != 0]
#        if not non_zero_values.empty:
#          print(f"Non-zero values in column {col}:")
#          print(non_zero_values)



