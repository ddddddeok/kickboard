import torch
import cv2
from deep_sort_realtime.deepsort_tracker import DeepSort
import sys
import pathlib
import pygame

sys.path.append('models')

temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

model_path = 'weight.pt'
model = torch.hub.load('ultralytics/yolov5', 'custom', path='weight.pt')
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

pathlib.PosixPath = temp

path = 'kickboard2.mp4'
audio_path = 'melody.mp3'

cap = cv2.VideoCapture(path)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

object_tracker = DeepSort(
    max_age=5,
    n_init=2,
    nms_max_overlap=1.0,
    max_cosine_distance=0.3,
    nn_budget=None,
    override_track_class=None,
    embedder="mobilenet",
    half=True,
    bgr=True,
    embedder_gpu=True,
    embedder_model_name=None,
    embedder_wts=None,
    polygon=False,
    today=None
)

# 클래스별 추적된 객체의 고유 ID를 저장할 사전
class_tracks = {}

# pygame 초기화
pygame.mixer.init()
audio_playing = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)
    detections = []

    for *box, conf, cls in results.xyxy[0]:
        x1, y1, x2, y2 = map(int, box)
        detections.append([[x1, y1, x2 - x1, y2 - y1], conf, cls])

    tracker_outputs = object_tracker.update_tracks(detections, frame=frame)

    class_1_detected = False

    for track in tracker_outputs:
        bbox = track.to_ltrb()
        tid = track.track_id
        cls = model.names[int(track.det_class)]
       
        # 클래스별 추적된 객체의 고유 ID 업데이트
        if cls in class_tracks:
            class_tracks[cls].add(tid)
        else:
            class_tracks[cls] = {tid}
       
        if int(track.det_class) == 1:
            class_1_detected = True

        cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (255, 0, 0), 2)
        cv2.putText(frame, f" {cls} {tid}", (int(bbox[0]), int(bbox[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, (255, 0, 0), 2)

    # 클래스 번호 1번이 인식되는 경우 오디오 재생
    if class_1_detected:
        if not audio_playing:
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play(-1)  # 무한 반복 재생
            audio_playing = True
    else:
        if audio_playing:
            pygame.mixer.music.stop()
            audio_playing = False

    cv2.imshow('YOLOv5 DeepSORT Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# pygame 종료
pygame.mixer.quit()

# 클래스별 추적한 객체 수 출력
print("Class tracks:")
for cls, tracks in class_tracks.items():
    print(f"{cls}: {len(tracks)}")
