import os

# 작업할 디렉토리 경로
image_directory = r"E:\캡스톤\킥보드데이터\120.개인형 이동장치 안전 데이터\01.데이터\2.Validation\원천데이터\VS1\블랙박스\주간\우천\연출"
json_directory = r"E:\캡스톤\킥보드데이터\120.개인형 이동장치 안전 데이터\01.데이터\2.Validation\라벨링데이터\VL1\블랙박스\주간\우천\연출"

# 이미지 디렉토리 내의 모든 파일 가져오기
image_files = os.listdir(image_directory)

# JSON 디렉토리 내의 모든 파일 가져오기
json_files = os.listdir(json_directory)

# JSON 파일명에서 이미지 파일명 추출
json_images = [json_file.split('.')[0] for json_file in json_files]

# 이미지 파일 중에서 JSON 파일이 존재하지 않는 파일 삭제
for image_file in image_files:
    image_name = image_file.split('.')[0]
    if image_name not in json_images:
        os.remove(os.path.join(image_directory, image_file))
        print(f"Removed image: {image_file}")
