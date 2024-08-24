"""Utilities for reading and processing csv data with features for outlier analysis.

csv_to_pandas_df
  Returns: pandas.core.frame.DataFrame
  Example usage: csv_to_pandas('c', '/tmp', file_name='_other_suffix.csv', write_to_csv=True)
outlier_rows
  Returns: pandas.core.frame.DataFrame
  Example usage: outlier_rows('c', '/tmp')
"""


def csv_to_pandas_df(lang: str, storage: str, file_name_suffix: str = 'combined.csv', write_to_csv: bool = False):
    import pandas as pd

    df = pd.read_csv(storage+lang+'_'+file_name_suffix, skipinitialspace=True)
    if (write_to_csv):
        df.to_csv(lang+'_normalized_'+file_name_suffix, index=False)
    return df


def outlier_rows(lang: str, storage: str) -> None:
    df = csv_to_pandas_df(lang, storage)
    outl = df.nlargest(df.shape[0]//2, "percentage")
    return outl.nlargest(10, "instruction")
