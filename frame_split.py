import torch
import cv2
import pathlib
import sys

pathlib.PosixPath = pathlib.WindowsPath

video_path = 'no_helmet.mp4'
cap = cv2.VideoCapture(video_path)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)

model_path = 'best.pt'
model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)

if not cap.isOpened():
    print("Error reading video file")
    sys.exit()

w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

line_points = [(1080, 0), (1080, 920)]
video_writer = cv2.VideoWriter("object_counting_output.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

helmet_count = 0
no_helmet_count = 0
crossed_ids = set()

i = 0
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Video frame is empty or video processing has been successfully completed.")
        break

    results = model(frame)

    for *box, conf, cls in results.xyxy[0]:
        label = model.names[int(cls)]
        cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (255, 0, 0), 2)
        cv2.putText(frame, label, (int(box[0]), int(box[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        if label == 'helmet':
            helmet_count += 1
        elif label == 'no_helmet':
            no_helmet_count += 1

    cv2.imwrite(f'image2/object_counting_output_{i}.jpg', frame)
    i += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print(f"Total helmets: {helmet_count}")
print(f"Total no_helmets: {no_helmet_count}")
print(f"total frames: {cap.get(cv2.CAP_PROP_FRAME_COUNT)}")
print(f"Accuracy: {no_helmet_count / cap.get(cv2.CAP_PROP_FRAME_COUNT)}")
cap.release()
video_writer.release()
cv2.destroyAllWindows()