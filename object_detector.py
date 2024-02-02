from typing import List
import PIL

class ObjectDetector:

    def __init__(self, image: PIL, model):
        self.resized_image = None
        self.image = image
        self.model = model

    def image_preprocess(self):

        col, row = (640, 640)
        self.resized_image = self.image.resize((col, row), PIL.Image.ANTIALIAS)

    def object_detect(self) -> List:
        self.image_preprocess()
        out = self.model(self.resized_image, size=640)

        json_result = results_to_json(out, self.model)
        return json_result


def results_to_json(results, model):
    """ Converts yolo model output to json (list of dicts)
    This code is from: https://github.com/WelkinU/yolov5-fastapi-demo/blob/main/server.py

    """
    return [
        [
            {
                "class": int(pred[5]),
                "class_name": model.model.names[int(pred[5])],
                "bbox": [int(x) for x in pred[:4].tolist()],
                "confidence": float(pred[4]),
            }
            for pred in result
        ]
        for result in results.xyxy
    ]