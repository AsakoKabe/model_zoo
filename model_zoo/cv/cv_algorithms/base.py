from abc import ABC, abstractmethod
from pathlib import Path

import cv2


class BaseCV(ABC):
    FONT_SCALE = 2e-3  # Adjust for larger font size in all images
    THICKNESS_SCALE = 1e-3  # Adjust for larger thickness in all images

    def predict(self, path_img):
        path_img = Path(path_img[1::])
        img = cv2.imread(path_img.as_posix())
        img_pred = self.get_predicted_image(img)

        # create img path format: old_img_path + _pred + '.{file extension}'
        # example: '/media/img.jpg' -> '/media/img_pred.jpg'
        path_img_pred = f'{path_img.parent.as_posix()}/{path_img.stem}_pred' \
                        f'{path_img.suffix}'

        cv2.imwrite(path_img_pred, img_pred)

        # remove '/media' from img_pred_path to save to the database format
        path_img_pred = path_img_pred[6::]

        return path_img_pred

    @abstractmethod
    def get_predicted_image(self, img):
        pass
