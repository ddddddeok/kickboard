import json
import os
import shutil

def json_to_txt(input_dir):
    # 입력 디렉토리의 모든 파일 목록 가져오기
    files = os.listdir(input_dir)
    
    # 모든 파일에 대해 반복
    for file_name in files:
        # 파일 경로
        input_path = os.path.join(input_dir, file_name)
        
        # 디렉토리인 경우 재귀적으로 탐색
        if os.path.isdir(input_path):
            json_to_txt(input_path)
        # JSON 파일인 경우 변환
        elif os.path.isfile(input_path) and file_name.endswith('.json'):
            # TXT 파일 경로
            output_path = os.path.splitext(input_path)[0] + ".txt"
            
            # JSON 파일 읽기
            with open(input_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
            
            # TXT 파일로 쓰기
            with open(output_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(json.dumps(data, indent=4))
                
            # JSON 파일 삭제
            os.remove(input_path)

# 변환할 JSON 파일이 들어 있는 최상위 디렉토리를 지정합니다.
input_directory = r'E:\캡스톤\킥보드데이터\120.개인형 이동장치 안전 데이터\01.데이터\2.Validation\라벨링데이터\VL1\블랙박스\주간\우천\연출'

# 함수 호출
json_to_txt(input_directory)

# 변환 작업이 끝났음을 알리는 메시지 출력
print("작업이 완료되었습니다.")

