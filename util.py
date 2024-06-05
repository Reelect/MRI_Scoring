import pandas as pd


def get_dataframe(path):
    df = pd.read_excel(path)
    df.columns = df.columns.map(str)
    df_col_drop = df.dropna(axis=1, how="all")
    df_register_drop = df_col_drop.drop(columns="수험번호")
    df_final = df_register_drop.dropna(how="any")
    return df_final


def get_colum_name(dataframe: pd.DataFrame):
    cols = dataframe.columns
    return list(map(str, cols))


def get_score_summary(df: pd.DataFrame, cols: list[str], answers: list[str]) -> pd.DataFrame:
    stats = pd.DataFrame()
    min_correct = float('inf')
    min_correct_problem_number = 0
    for col_i, col in enumerate(cols):
        result = [0] * 5
        for ele in df[:][col]:
            if isinstance(ele, int):
                result[ele-1] += 1
            elif isinstance(ele, str) and ele == 'O':
                result[int(answers[col_i])] += 1

        ratio = [100 * element / sum(result) for element in result]

        last = [f"{col}번 정답", answers[col_i], "정답률(%)", ratio[int(answers[col_i])-1]]

        if min_correct > ratio[int(answers[col_i])]:
            min_correct = ratio[int(answers[col_i])]
            min_correct_problem_number = col_i + 1

        # 각각의 리스트를 데이터프레임으로 변환하여 추가
        stats = pd.concat([stats, pd.DataFrame([[f"{col}번 선택 분포(명)"] + result])], ignore_index=True)
        stats = pd.concat([stats, pd.DataFrame([[f"{col}번 선택 비율(%)"] + ratio])], ignore_index=True)
        stats = pd.concat([stats, pd.DataFrame([last])], ignore_index=True)

    stats = pd.concat([stats, pd.DataFrame([["최저 정답률", min_correct, "문제번호", min_correct_problem_number]])],
                      ignore_index=True)

    return stats


def get_rank_list(df: pd.DataFrame) -> pd.DataFrame:
    high_count = 0
    sorted_df = df[["성명", "점수"]].sort_values(by=['점수', '성명'], ascending=[False, True])
    sorted_df = sorted_df.reset_index(drop=True)
    # 점수 기준으로 등수 매기기 (점수가 같은 사람은 같은 등수)
    sorted_df['등수'] = sorted_df['점수'].rank(method='min', ascending=False)

    # 등수를 정수형으로 변환
    sorted_df['등수'] = sorted_df['등수'].astype(int)
    sorted_df = sorted_df[['등수'] + [col for col in sorted_df.columns if col != '등수']]
    score_counts = sorted_df['점수'].value_counts().reset_index()
    score_counts.columns = ['점수 분포', '인원 수']
    score_counts = score_counts.sort_values(by=['점수 분포']).reset_index(drop=True)
    return pd.concat([sorted_df, score_counts], axis=1)
