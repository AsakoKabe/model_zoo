import math
from abc import abstractmethod

import cv2
import numpy as np
from cv.cv_algorithms.base import BaseCV
from openvino.runtime import Core


class BaseFaceDetection(BaseCV):
    @abstractmethod
    def get_predicted_faces(self, img):
        pass


class FaceDetectionHaarCascade(BaseFaceDetection):
    def __init__(self):
        super(BaseFaceDetection, self).__init__()
        self.__face_cascade = cv2.CascadeClassifier(
            'cv/weights/haarcascade_frontalface_default.xml'
        )

    def get_predicted_faces(self, img):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.__face_cascade.detectMultiScale(img_gray, 1.1, 4)

        return faces

    def get_predicted_image(self, img):
        faces = self.get_predicted_faces(img)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), color=(0, 0, 255),
                          thickness=5)

        return img


class FaceDetectionMobileNet(BaseFaceDetection):
    def __init__(self):
        super(BaseFaceDetection, self).__init__()
        self.__ie = Core()
        self.__model = self.__ie.read_model(
            model="cv/weights/intel/face-detection-retail-0004/FP32/face"
                  "-detection-retail-0004.xml")
        self.__compiled_model = self.__ie.compile_model(model=self.__model,
                                                        device_name="CPU")
        self.__output_layer = self.__compiled_model.output(0)

    def get_predicted_faces(self, img):
        input_image = cv2.resize(src=img, dsize=(300, 300))
        input_image = np.expand_dims(input_image.transpose(2, 0, 1), 0)

        faces = self.__compiled_model([input_image])[self.__output_layer]
        faces = faces.reshape(-1, 7)

        return faces

    def get_predicted_image(self, img):
        faces = self.get_predicted_faces(img)
        height, width, _ = img.shape

        for face in faces:
            conf = float(face[2])
            x_min = int(face[3] * img.shape[1])
            y_min = int(face[4] * img.shape[0])
            x_max = int(face[5] * img.shape[1])
            y_max = int(face[6] * img.shape[0])

            if conf > 0.8:
                thickness = math.ceil(min(width, height) *
                                      BaseCV.THICKNESS_SCALE)
                cv2.rectangle(img, (x_min, y_min), (x_max, y_max),
                              color=(0, 255, 0),
                              thickness=thickness)

        return img
