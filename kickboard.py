import torch
import cv2
from deep_sort_realtime.deepsort_tracker import DeepSort

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
tracker = DeepSort(max_age = 30, nn_budget=70, override_track_class=None)

path = 'cat.webm'

cap = cv2.VideoCapture(path)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)
    detections = []

    for *box, conf, cls in results.xyxy[0]:
        x1, y1, x2, y2 = map(int, box)
        detections.append([[x1, y1, x2, y2],conf, cls])

    tracker_outputs = tracker.update_tracks(detections, frame=frame)

    for track in tracker_outputs:
        bbox = track.to_tlbr()
        id = track.track_id
        cls = model.names[int(track.det_class)]
        # cls = model.names[int(track.get_class())]

        cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (255, 0, 0), 2)
        cv2.putText(frame, f" {cls} {id}", (int(bbox[0]), int(bbox[1]-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)

    cv2.imshow('YOLOv5 DeepSORT Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()