"""Utilities for reading and processing csv data with features for outlier analysis.

pandas_df_with_outlier_scores
  Returns: pandas.core.frame.DataFrame
  Example usage: pandas_df_with_outlier_scores('c', '/tmp', file_name='_other_suffix.csv', write_to_csv=True)
"""


def pandas_df_with_outlier_scores(lang: str, storage: str, file_name_suffix: str = '_combined.csv', write_to_csv: bool = False):
    import pandas as pd

    df = pd.read_csv(storage+lang+file_name_suffix, skipinitialspace=True)
    data = df["instruction"]
    min_value = data.min()
    max_value = data.max()
    df['normalized_instruction'] = (
        data - min_value) / (max_value - min_value) * 100
    df['outlier_scores'] = df["percentage"] + df['normalized_instruction']
    if (write_to_csv):
        df.to_csv('normalized_file.csv', index=False)
    return df
