import os

def find_files_with_text(folder_path, text):
    result = []
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith(".json"):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    if text in content:
                        result.append(file_path)
    return result

folder_path = r"E:\캡스톤\킥보드데이터\120.개인형 이동장치 안전 데이터\01.데이터\1.Training\라벨링데이터\TL1\CCTV\주간\맑음\실증"
text_to_find = "PM_code\": \"15\""
found_files = find_files_with_text(folder_path, text_to_find)
print("찾은 파일:")
for file_path in found_files:
    print(file_path)
