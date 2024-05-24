import os

# 타겟 텍스트들
target_texts = ["PM_code\": \"28", "PM_code\": \"31"]

# 작업할 디렉토리 경로
directory = r"E:\캡스톤\킥보드데이터\120.개인형 이동장치 안전 데이터\01.데이터\2.Validation\라벨링데이터\VL1\블랙박스\주간\우천\연출"

# 디렉토리 내 파일 확인
for filename in os.listdir(directory):
    filepath = os.path.join(directory, filename)
    if os.path.isfile(filepath):
        # 파일 내용을 읽어와서 모든 타겟 텍스트가 없는지 확인
        with open(filepath, 'r') as file:
            content = file.read()
        if all(target_text not in content for target_text in target_texts):
            # 모든 타겟 텍스트가 없으면 파일 삭제
            os.remove(filepath)
            print(f"Removed file: {filename}")
