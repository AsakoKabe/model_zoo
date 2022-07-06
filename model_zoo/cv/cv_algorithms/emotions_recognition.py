import math

import cv2
import numpy as np
from cv.cv_algorithms.base import BaseCV
from cv.cv_algorithms.face_detection import FaceDetectionMobileNet
from openvino.runtime import Core


class EmotionsRecognition(BaseCV):
    def __init__(self):
        super(BaseCV, self).__init__()
        self.__ie = Core()
        self.__model = self.__ie.read_model(
            model="cv/weights/intel/emotions-recognition-retail-0003/FP32"
                  "/emotions-recognition-retail-0003.xml")
        self.__compiled_model = self.__ie.compile_model(model=self.__model,
                                                        device_name="CPU")
        self.__prob_layer = self.__compiled_model.output(0)
        self.__face_detection_model = FaceDetectionMobileNet()

        self.__emotions_decode = {
            0: 'Neutral',
            1: 'Happy',
            2: 'Sad',
            3: 'Surprise',
            4: 'Anger'
        }

    def get_predicted_emotions(self, img):
        input_image = cv2.resize(src=img, dsize=(64, 64))
        input_image = np.expand_dims(input_image.transpose(2, 0, 1), 0)

        prob = self.__compiled_model([input_image])[self.__prob_layer]
        emotion = self.__emotions_decode[np.argmax(prob).item()]

        return emotion

    def get_predicted_image(self, img):
        faces = self.__face_detection_model.get_predicted_faces(img)
        height, width, _ = img.shape

        for face in faces:
            conf = float(face[2])
            x_min = int(face[3] * img.shape[1])
            y_min = int(face[4] * img.shape[0])
            x_max = int(face[5] * img.shape[1])
            y_max = int(face[6] * img.shape[0])

            if conf > 0.8:
                emotion = self.get_predicted_emotions(img[y_min:y_max,
                                                      x_min:x_max])

                font_scale = min(width, height) * BaseCV.FONT_SCALE
                thickness = math.ceil(min(width, height) *
                                      BaseCV.THICKNESS_SCALE)

                cv2.rectangle(img, (x_min, y_min), (x_max, y_max),
                              color=(0, 255, 0), thickness=thickness)
                cv2.putText(img, f'{emotion}', (x_min, y_max),
                            cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 255),
                            thickness)

        return img
