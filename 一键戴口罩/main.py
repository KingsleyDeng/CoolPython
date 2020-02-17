from PIL import Image
import face_recognition
import numpy as np

face_image_np = face_recognition.load_image_file('/path/to/face/picture')
face_landmarks = face_recognition.face_landmarks(face_image_np)

nose_bridge = face_landmarks['nose_bridge']
nose_point = nose_bridge[len(nose_bridge) * 1 // 4]
nose_v = np.array(nose_point)

chin = face_landmarks['chin']
chin_len = len(chin)
chin_bottom_point = chin[chin_len // 2]
chin_bottom_v = np.array(chin_bottom_point)
chin_left_point = chin[chin_len // 8]
chin_right_point = chin[chin_len * 7 // 8]



_face_img = Image.fromarray(face_image_np)
