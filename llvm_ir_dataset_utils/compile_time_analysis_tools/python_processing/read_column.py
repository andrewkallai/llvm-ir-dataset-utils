"""csv_to_pandas_df is used to read a IR features CSV file and create a Pandas dataframe for it, and outlier_rows is used to filter the Pandas dataframe to the IR files which can be classified as outliers. 

csv_to_pandas_df
  Returns: pandas.core.frame.DataFrame
  Example usage: csv_to_pandas('c', '/tmp', file_name='_other_suffix.csv', write_to_csv=True)
outlier_rows
  Returns: pandas.core.frame.DataFrame
  Example usage: outlier_rows('c', '/tmp')
"""


def csv_to_pandas_df(lang: str,
                     storage: str,
                     file_name_suffix: str = 'combined.csv'):
  import pandas as pd

  df = pd.read_csv(
      storage + lang + '_' + file_name_suffix, skipinitialspace=True)
  return df


def outlier_rows(lang: str,
                 storage: str,
                 outlier_num: int = 10,
                 write_to_csv: bool = False):
  df = csv_to_pandas_df(lang, storage)
  outl = df.nlargest(df.shape[0] // 2, "percentage")
  outl = outl[outl.instruction > outl["instruction"].quantile(
      q=.75, interpolation='lower')]
  outl = outl.nlargest(outlier_num, "percentage")
  if (write_to_csv):
    df.to_csv(lang + '_outliers.csv', index=False)
  return outl
