import os
import logging
from io import BytesIO
from warnings import filterwarnings, simplefilter
import ssl
from pathlib import Path
from ultralytics import YOLO
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
from src.service.object_detector import ObjectDetector

filterwarnings("ignore")
simplefilter(action='ignore', category=FutureWarning)

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
if not os.path.exists('logs'):
    os.mkdir('logs')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.StreamHandler()
file_handler = logging.FileHandler('logs/api.log')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

app = FastAPI()
model = YOLO('./ml_models/yolov8n.onnx', task="detect")

# Define API endpoint for object detection
@app.post("/detect/")
async def image_detect(request: Request, label: str = None,
                    input_file: UploadFile = File(...)):
    """
    API endpoint for performing object detection on an uploaded image.

    Args:
        request (Request): HTTP request object.
        label (str): Optional label for filtering detection results.
        input_file (UploadFile): Uploaded image file.

    Returns:
        JSONResponse: JSON response containing detection results.
    """
    if request.method == "POST":
        try:
            image = Image.open(BytesIO(await input_file.read()))
            ob = ObjectDetector(image, model)

            # Perform object detection
            object_detect_result = ob.object_detect()
            json_result = object_detect_result[0]
            encoded_image = object_detect_result[1]

            # Filter detection results by label if provided
            if label:
                filtered_json_result = [item for item in json_result if item.get("name") == label]
            else: 
                filtered_json_result = json_result
            logger.info("Detection results: %s", filtered_json_result)

            return JSONResponse({"image": encoded_image,
                                "objects": filtered_json_result,
                                "count": len(filtered_json_result),
                                "message": "object detected successfully",
                                "errors": None},
                                status_code=200)
        except Exception as error:
            logger.error(["process failed", error])
            return JSONResponse({"message": "object detection failed",
                                "errors": "error"},
                                status_code=400)        