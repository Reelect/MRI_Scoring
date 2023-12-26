import pandas as pd
import os


def get_dataframe(path):
    df = pd.read_excel(path)
    return df


def get_colum_name(dataframe: pd.DataFrame):
    return list(dataframe.columns)


def replace_filename_by_col(df: pd.DataFrame, code_col: int, subject_col: int, path: str):
    for _, item in df.iterrows():
        sub = item[subject_col]
        code = item[code_col]
        for root, directories, files in os.walk(path):
            files = [f for f in files if not f[0] == '.']
            directories[:] = [d for d in directories if not d[0] == '.']
            for idx, file in enumerate(files):
                if sub in file:
                    old_file = os.path.join(root, file)
                    new_file = os.path.join(root, code+file[5:])
                    os.rename(old_file, new_file)
