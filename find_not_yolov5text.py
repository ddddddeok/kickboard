import os
import re

def is_valid_yolov5_label_line(line):
    # YOLOv5 라벨 파일의 유효한 라인 형식을 확인하는 정규식
    pattern = re.compile(r'^\d+\s+([0-9]*[.])?[0-9]+\s+([0-9]*[.])?[0-9]+\s+([0-9]*[.])?[0-9]+\s+([0-9]*[.])?[0-9]+$')
    return bool(pattern.match(line))

def find_invalid_yolov5_labels(folder_path):
    # 폴더 내의 모든 파일을 순회
    files = os.listdir(folder_path)
    invalid_files = []

    for file in files:
        if file.endswith('.txt'):
            path = os.path.join(folder_path, file)
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if any(not is_valid_yolov5_label_line(line.strip()) for line in lines):
                    invalid_files.append(file)

    return invalid_files

# 폴더 경로 설정
folder_path = r'E:\캡스톤\selected_data_all\train_labels'
invalid_files = find_invalid_yolov5_labels(folder_path)

# 잘못된 형식의 파일 이름 출력
print("표준화되지 않은 라벨 파일:")
for file in invalid_files:
    print(file)
