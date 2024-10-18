import os
import asyncio
import cv2
import mediapipe as mp
import pandas as pd
from flet import *
import threading

tasks_module = mp.tasks

# 処理するファイルのキューを管理するためのリスト
file_queue = []

# メインスレッドでイベントループを取得し実行
def run_event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    loop.run_forever()

# 別スレッドでイベントループを実行
threading.Thread(target=run_event_loop, daemon=True).start()

async def process_videos():
    while True:
        if file_queue:
            video_file = file_queue.pop(0)
            await process_video(video_file)
        await asyncio.sleep(1)

async def process_video(video_file):
    cap = cv2.VideoCapture(video_file)
    with tasks_module.vision.HandLandmarker.create_from_model_path("hand_landmarker.task") as hand_landmarker:
        frames_data = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # フレームの前処理
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

            # ハンドランドマークのデータを取得
            result = hand_landmarker.detect(mp_image)
            if result.hand_landmarks:
                for hand_landmarks in result.hand_landmarks:
                    landmarks = []
                    for lm in hand_landmarks:
                        landmarks.extend([lm.x, lm.y, lm.z])
                    frames_data.append(landmarks)

        cap.release()

    # CSVに書き出し
    output_csv = os.path.splitext(video_file)[0] + ".csv"
    df = pd.DataFrame(frames_data)
    df.to_csv(output_csv, index=False)
    print(f"Processed {video_file}, output saved to {output_csv}")

def start_processing(e):
    loop = asyncio.get_running_loop()
    loop.call_soon_threadsafe(asyncio.create_task, process_videos())
    progress_label.value = "Processing videos..."
    page.update()

async def main(page: Page):
    page.title = "Mediapipe CSV Export Tool"
    global progress_label
    progress_label = Text(value="Idle...")
    file_picker = FilePicker(on_result=lambda e: file_queue.extend(e.files))

    # UIの設定
    page.add(
        Column(
            [
                Row([
                    ElevatedButton("Select Videos", on_click=lambda e: file_picker.pick_files(), data={'allowMultiple': True}),
                    ElevatedButton("Start Processing", on_click=start_processing)
                ]),
                progress_label,
                file_picker
            ]
        )
    )

app(target=main)