import pandas as pd
import os
import shutil


def get_colum(path):
    cols = pd.read_excel(path, usecols=[0, 11])  # 지문 코드, 지문 주제
    return cols



def listdir_without_hide(dir_path):
    file_names = [f for f in os.listdir(dir_path) if not f.startswith('.')]

    return file_names


file_name = input("읽을 엑셀 시트 절대 경로를 입력하세요 : ")

wb = pd.read_excel(file_name, usecols=[0, 1, 11])

code_list = [str(int(a)) for a in wb["지문코드"].tolist()]
print(code_list)

folder_list = ['1.평가원', '2.교육청', '3.LEET', '4.MDEET', '5.PEET','해설 데이터 베이스']

root_dir = "Z:\윤국연\\2024_DB"

type_input = input("1. 지문  2. 문단해설  3. 선지해설  4. 체크리스트 5. 문학해설\n필요한 부분을 입력하세요. 만약 지문과 문단해설이 동시에 필요한 경우 1,2로 입력하세요.")

selected_type = type_input.split(',')


type_name = []

for t in selected_type:
    if t == '1':
        type_name.append('지문')
    elif t == '2':
        type_name.append('문단해설')
    elif t == '3':
        type_name.append('선지해설')
    elif t == '4':
        type_name.append('체크리스트')
    elif t == '5':
        type_name.append('문학해설')


if len(type_name) == 0:
    print("필요한 부분 입력 제대로 안 됨. 다시 하세요.")
    exit(0)

saved_dir_path = input("파일 저장할 폴더 절대 경로를 입력하세요 : ")

for (root, directories, files) in os.walk(root_dir):
    for file in files:
        if file[:5] in code_list:
            file_path = os.path.join(root, file)
            # print(file_path)

            for needed_type in type_name:
                # print(file[-1 * len(needed_type) - 4:-4])
                if file[-1 * len(needed_type) - 4:-4] == needed_type:
                    shutil.copy(file_path, os.path.join(saved_dir_path, file))


"""
import os

def rename_file(original_path):
    # 여기에 파일 이름 변경 조건을 구현하세요.
    # 예: new_name = "new_" + os.path.basename(original_path)
    # 이 예제에서는 원래 이름 앞에 "new_"를 붙여 변경합니다.
    new_name = "new_" + os.path.basename(original_path)
    return new_name

def rename_files_in_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            original_path = os.path.join(root, file)
            new_name = rename_file(original_path)
            new_path = os.path.join(root, new_name)
            os.rename(original_path, new_path)
            print(f"Renamed '{original_path}' to '{new_path}'")

# 현재 디렉토리에서 실행
rename_files_in_directory('.')

"""