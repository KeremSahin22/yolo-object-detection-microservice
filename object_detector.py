from typing import List
import PIL
import json
from PIL import Image
import base64
import cv2
from io import BytesIO
class ObjectDetector:

    def __init__(self, image: PIL, model):
        self.resized_image = None
        self.image = image
        self.model = model

    def image_preprocess(self):

        col, row = (640, 640)
        self.resized_image = self.image.resize((col, row), PIL.Image.LANCZOS)

    #For single image detection
    def object_detect(self):
        self.image_preprocess()
        out = self.model(self.resized_image)
        json_result = out[0].tojson()
        im_array = out[0].plot()  # plot a BGR numpy array of predictions
        im = Image.fromarray(im_array[..., ::-1]) 
        buffered = BytesIO()
        im.save(buffered, format="PNG")
        encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return (json.loads(json_result), encoded_image)