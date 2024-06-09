import os
import json

def convert_to_yolo_format(box, image_width, image_height):
    x_center = (box[0] + box[2] / 2) / image_width
    y_center = (box[1] + box[3] / 2) / image_height
    width = box[2] / image_width
    height = box[3] / image_height
    return f"{x_center} {y_center} {width} {height}"

def parse_annotations(folder_path, image_width, image_height):
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    continue  # 오류 발생 시 아무 동작도 하지 않음

            output_lines = []
            for annotation in data.get('annotations', {}).get('PM', []):
                pm_code = annotation.get('PM_code')
                if pm_code in ['28', '31']:
                    class_id = 0 if pm_code == '28' else 1
                    bbox = annotation.get('points', [])
                    if len(bbox) == 4:  # BBox는 [x, y, width, height] 형식이어야 합니다.
                        yolo_bbox = convert_to_yolo_format(bbox, image_width, image_height)
                        output_lines.append(f"{class_id} {yolo_bbox}")

            if output_lines:
                output_file = os.path.join(folder_path, filename)
                with open(output_file, 'w', encoding='utf-8') as output:
                    output.write('\n'.join(output_lines))

folder_path = r'E:\캡스톤\킥보드데이터\120.개인형 이동장치 안전 데이터\01.데이터\1.Training\라벨링데이터\TL2\CCTV\주간\맑음\실증'
image_width = 1920  # 이미지의 너비를 지정
image_height = 1080  # 이미지의 높이를 지정

parse_annotations(folder_path, image_width, image_height)
