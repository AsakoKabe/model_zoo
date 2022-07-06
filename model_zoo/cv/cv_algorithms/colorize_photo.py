import cv2 as cv
import numpy as np
from cv.cv_algorithms.base import BaseCV
from openvino.runtime import Core


class ColorizePhoto(BaseCV):
    def __init__(self):
        super(BaseCV, self).__init__()
        self.__ie = Core()
        self.__model = self.__ie.read_model(
            model="cv/weights/intel/colorization-v2/FP32/colorization-v2.xml")
        self.__compiled_model = self.__ie.compile_model(model=self.__model,
                                                        device_name="CPU")
        self.__output_tensor = self.__compiled_model.output(0)

    def get_predicted_image(self, img):
        inputs = {}
        for inp in self.__model.inputs:
            inputs[inp.get_any_name()] = np.zeros(inp.shape)

        infer_request = self.__compiled_model.create_infer_request()

        input_tensor_name = 'data_l'
        input_shape = self.__model.input(input_tensor_name).shape

        _, _, h_in, w_in = input_shape

        (h_orig, w_orig) = img.shape[:2]

        if img.shape[2] > 1:
            frame = cv.cvtColor(cv.cvtColor(img, cv.COLOR_BGR2GRAY),
                                cv.COLOR_GRAY2RGB)
        else:
            frame = cv.cvtColor(img, cv.COLOR_GRAY2RGB)

        img_rgb = frame.astype(np.float32) / 255
        img_lab = cv.cvtColor(img_rgb, cv.COLOR_RGB2Lab)
        img_l_rs = cv.resize(img_lab.copy(), (w_in, h_in))[:, :, 0]

        inputs[input_tensor_name] = np.expand_dims(img_l_rs, axis=[0, 1])

        res = infer_request.infer(inputs)[self.__output_tensor]

        update_res = np.squeeze(res)

        out = update_res.transpose((1, 2, 0))
        out = cv.resize(out, (w_orig, h_orig))
        img_lab_out = np.concatenate((img_lab[:, :, 0][:, :, np.newaxis], out),
                                     axis=2)
        img_bgr_out = np.clip(cv.cvtColor(img_lab_out, cv.COLOR_Lab2BGR), 0, 1)

        colorize_image = (
                cv.resize(img_bgr_out, img.shape[:2][::-1]) * 255).astype(
            np.uint8)

        return colorize_image
