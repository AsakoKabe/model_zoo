import math

import cv2
import numpy as np
from cv.cv_algorithms.base import BaseCV
from openvino.runtime import Core


class TextDetection(BaseCV):
    def __init__(self):
        super(BaseCV, self).__init__()
        self.__ie = Core()
        self.__model = self.__ie.read_model(
            model="cv/weights/intel/horizontal-text-detection-0001/FP32"
                  "/horizontal-text-detection-0001.xml")
        self.__compiled_model = self.__ie.compile_model(model=self.__model,
                                                        device_name="CPU")
        self.__boxes_layer = self.__compiled_model.output(0)
        self.__labels_layer = self.__compiled_model.output(1)
        self.__img_pred_size = 704

    def get_predicted_boxes_and_labels(self, img):
        input_image = cv2.resize(src=img, dsize=(self.__img_pred_size,
                                                 self.__img_pred_size))
        input_image = np.expand_dims(input_image.transpose(2, 0, 1), 0)

        boxes = self.__compiled_model([input_image])[self.__boxes_layer]
        labels = self.__compiled_model([input_image])[self.__labels_layer]

        return boxes, labels

    def get_predicted_image(self, img):
        boxes, labels = self.get_predicted_boxes_and_labels(img)
        height, width, _ = img.shape

        for i, box in enumerate(boxes):
            # if find box with text, label == 0
            if labels[i]:
                continue

            x_min = int(box[0] / self.__img_pred_size * img.shape[1])
            y_min = int(box[1] / self.__img_pred_size * img.shape[0])
            x_max = int(box[2] / self.__img_pred_size * img.shape[1])
            y_max = int(box[3] / self.__img_pred_size * img.shape[0])

            thickness = math.ceil(min(width, height) *
                                  BaseCV.THICKNESS_SCALE)

            cv2.rectangle(img, (x_min, y_min), (x_max, y_max),
                          color=(0, 255, 0), thickness=thickness)

        return img
