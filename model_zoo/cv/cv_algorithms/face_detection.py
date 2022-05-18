from pathlib import Path

import cv2


class FaceDetection:
    def __init__(self):
        self.__face_cascade = cv2.CascadeClassifier(
            'cv/weights/haarcascade_frontalface_default.xml'
        )

    def predict(self, path_img):
        path_img = Path(path_img[1::])
        img = cv2.imread(path_img.as_posix())
        img_pred = self.get_predict_for_image(img)

        # create img path format: old_img_path + _pred + '.{file extension}'
        # example: '/media/img.jpg' -> '/media/img_pred.jpg'
        path_img_pred = f'{path_img.parent.as_posix()}/{path_img.stem}_pred' \
                        f'{path_img.suffix}'

        cv2.imwrite(path_img_pred, img_pred)

        # remove '/media' from img_pred_path to save to the database format
        path_img_pred = path_img_pred[6::]

        return path_img_pred

    def get_predict_for_image(self, img):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.__face_cascade.detectMultiScale(img_gray, 1.1, 4)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), color=(0, 0, 255),
                          thickness=5)

        return img
