import cv2
import mediapipe as mp
import numpy as np
import csv
import time
from tkinter import ttk
import math
import datetime

def extract_face_landmarks_to_csv(video_path, csv_path, progress_bar,progress_text, progress_image_update_function):
    model_path = "faceTracking.task"

    # FaceLandmarkerのオプションを設定
    options = mp.tasks.vision.FaceLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(model_asset_path=model_path),
        output_face_blendshapes=True,
        running_mode=mp.tasks.vision.RunningMode.VIDEO)

    # FaceLandmarkerインスタンスを生成
    landmarker = mp.tasks.vision.FaceLandmarker.create_from_options(options)



    try:
        # 動画ファイルを開く
        cap = cv2.VideoCapture(video_path)

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        progress_bar["maximum"] = total_frames
        fps = cap.get(cv2.CAP_PROP_FPS)  # フレームレートを取得

        if fps == 0:
            print("fps is 0")

        frame_num = 0
        print(str(total_frames) + "frames video detected.")
        print("videoPath:" + video_path + "csv_path: " + csv_path + "total_frames:" + str(total_frames) + "fps:" + str(fps) )
        # 出力CSVファイルの設定
        with open(csv_path, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            start_time = time.time()
            #ヘッダー出力
            header = ["time"]
            for i in range(0, 478):
                header.append(str(i)+"x")
                header.append(str(i)+"y")
                header.append(str(i)+"z")
            for i in ["_neutral"
                ,"browDownLeft"
                ,"browDownRight"
                ,"browInnerUp"
                ,"browOuterUpLeft"
                ,"browOuterUpRight"
                ,"cheekPuff"
                ,"cheekSquintLeft"
                ,"cheekSquintRight"
                ,"eyeBlinkLeft"
                ,"eyeBlinkRight"
                ,"eyeLookDownLeft"
                ,"eyeLookDownRight"
                ,"eyeLookInLeft"
                ,"eyeLookInRight"
                ,"eyeLookOutLeft"
                ,"eyeLookOutRight"
                ,"eyeLookUpLeft"
                ,"eyeLookUpRight"
                ,"eyeSquintLeft"
                ,"eyeSquintRight"
                ,"eyeWideLeft"
                ,"eyeWideRight"
                ,"jawForward"
                ,"jawLeft"
                ,"jawOpen"
                ,"jawRight"
                ,"mouthClose"
                ,"mouthDimpleLeft"
                ,"mouthDimpleRight"
                ,"mouthFrownLeft"
                ,"mouthFrownRight"
                ,"mouthFunnel"
                ,"mouthLeft"
                ,"mouthLowerDownLeft"
                ,"mouthLowerDownRight"
                ,"mouthPressLeft"
                ,"mouthPressRight"
                ,"mouthPucker"
                ,"mouthRight"
                ,"mouthRollLower"
                ,"mouthRollUpper"
                ,"mouthShrugLower"
                ,"mouthShrugUpper"
                ,"mouthSmileLeft"
                ,"mouthSmileRight"
                ,"mouthStretchLeft"
                ,"mouthStretchRight"
                ,"mouthUpperUpLeft"
                ,"mouthUpperUpRight"
                ,"noseSneerLeft"
                ,"noseSneerRight"]:
                header.append(i)

            csv_writer.writerow(header)

            startProcess = datetime.datetime.now()
            updateTime = datetime.datetime.now()
            process_fps = 0

            if not cap.isOpened():
                raise ValueError("Unable to open video file: " + video_path)
            # ビデオからフレームを読み取る
            while cap.isOpened():

                frame_num += 1
                time_diff = datetime.datetime.now() - updateTime
                if time_diff.total_seconds() > 1:
                    process_fps = math.ceil((frame_num - process_fps)*100 / time_diff.total_seconds())/100
                    progress_text.set(str(math.ceil(frame_num*10000/total_frames)/100) + "% " + str(process_fps) + "fps 残り"+ str(math.floor((total_frames-frame_num)/process_fps/60))+ "分" +str(math.ceil((total_frames-frame_num)/process_fps)%60) +"秒")
                    updateTime = datetime.datetime.now()
                    process_fps = frame_num
                    progress_image_update_function(frame)

                if frame_num % 10 == 0:
                    progress_bar["value"] = frame_num

                ret, frame = cap.read()
                if not ret:
                    break

                # OpenCVからMediaPipeのImageオブジェクトへ変換
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

                # 現在のフレームのタイムスタンプを計算
                frame_timestamp_ms = int((time.time() - start_time) * 1000)

                # 顔のランドマーキングを実行
                face_landmarker_result = landmarker.detect_for_video(mp_image, frame_timestamp_ms)

                if face_landmarker_result.face_landmarks:
                    # ランドマークデータの取得と整形
                    landmarks = []
                    for face_landmark in face_landmarker_result.face_landmarks[0]:
                        landmarks.append(face_landmark.x)
                        landmarks.append(face_landmark.y)
                        landmarks.append(face_landmark.z)

                    for face_blendshapes in face_landmarker_result.face_blendshapes[0]:
                        landmarks.append(face_blendshapes.score)


                    csv_writer.writerow([frame_timestamp_ms / 1000] + landmarks)

                else:
                    csv_writer.writerow([frame_timestamp_ms / 1000])


    except Exception as e:
        raise e
    finally:
        cap.release()


# 使用例
#model_path = 'path_to_your_model'  # モデルのパスを適切に設定
#video_path = 'path_to_your_video.mp4'  # ビデオのパスを設定
#csv_path = 'output_data.csv'  # CSVファイルのパスを設定
#extract_face_landmarks_to_csv(video_path, csv_path, model_path)
