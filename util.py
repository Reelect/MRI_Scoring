import unicodedata

import pandas as pd
import os


def get_dataframe(path):
    df = pd.read_excel(path)
    df.columns = df.columns.map(str)
    return df


def get_colum_name(dataframe: pd.DataFrame):
    cols = dataframe.columns
    return list(map(str, cols))


def replace_filename_by_col(df: pd.DataFrame, code_col: str, subject_col: str, path, index: int):
    temp = 0
    for _, item in df.iterrows():
        if temp < index:
            temp += 1
            continue
        sub = str(item[subject_col])
        sub_normalized = unicodedata.normalize('NFC', sub)
        code = str(item[code_col])
        for root, directories, files in os.walk(path):
            files = [f for f in files if not f[0] == '.']
            files_normalized = [unicodedata.normalize('NFC', f) for f in files]
            directories[:] = [d for d in directories if not d[0] == '.']
            for idx, f in enumerate(files_normalized):
                if sub_normalized in f:
                    old_file = os.path.join(root, f)
                    new_file = os.path.join(root, code+f[5:])
                    os.rename(old_file, new_file)
