import os

# 폴더 경로 설정
folder_path = r'E:\캡스톤\selected_data_all\train_labels'

# 해당 폴더의 파일 리스트 가져오기
files = os.listdir(folder_path)

# '1'로 시작하는 파일 수 세기
count = 0
for file in files:
    if file.endswith('.txt'):  # 텍스트 파일인지 확인
        with open(os.path.join(folder_path, file), 'r') as f:
            first_char = f.read(1)  # 파일의 첫 번째 문자 읽기
            if first_char == '1':  # 첫 번째 문자가 '1'인지 확인
                count += 1

# 결과 출력
print(f"'1'로 시작하는 파일의 수: {count}")
