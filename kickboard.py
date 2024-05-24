import torch
import cv2
from deep_sort_realtime.deepsort_tracker import DeepSort

import sys
import pathlib

sys.path.append('models')

temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

model_path = 'weight.pt'
model = torch.hub.load('ultralytics/yolov5', 'custom', path ='weight.pt')
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

pathlib.PosixPath = temp

path = 'kickboard2.mp4'

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

    for track in tracker_outputs:
        bbox = track.to_ltrb()
        tid = track.track_id
        cls = model.names[int(track.det_class)]
        cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (255, 0, 0), 2)
        cv2.putText(frame, f" {cls} {tid}", (int(bbox[0]), int(bbox[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, (255, 0, 0), 2)

    cv2.imshow('YOLOv5 DeepSORT Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()