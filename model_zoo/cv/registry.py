from cv.cv_algorithms.face_detection import FaceDetectionMobileNet
from cv.cv_algorithms.face_recognition import FaceRecognitionAgeGender
from cv.cv_algorithms.text_detection import TextDetection
from zoo.models import ModelCV


class CVRegistry:
    def __init__(self):
        self.__algorithms = {}
        self.__matching_models = self.__get_matching_models()
        self.__create_algorithm_from_bd()

    def add_algorithm(self, id_algorithm, algorithm_object):
        self.__algorithms[id_algorithm] = algorithm_object

    def get_algorithm_by_id(self, id_algorithm):
        return self.__algorithms[id_algorithm]

    def __create_algorithm_from_bd(self):
        models = ModelCV.objects.all()
        for model in models:
            model_object = self.__matching_models[model.name]()
            self.add_algorithm(model.id, model_object)

    @staticmethod
    def __get_matching_models():
        return {
            'Face Detection': FaceDetectionMobileNet,
            'Face Recognition': FaceRecognitionAgeGender,
            'Text Detection': TextDetection
        }
