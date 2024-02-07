# Object Detection Microservice with YOLO and FastAPI
This project provides a simple microservice for object detection, incorporating a pre-trained YOLOV8 Model and a RESTful API created with FastAPI. 

## YOLOV8 ONNX Model
The YOLOV8 model has been exported ONNX format and can be found under the "models" folder. ONNX models can be used to transition between different frameworks (PyTorch to Tensorflow), and can be used with ONNX Runtime for cross-platform acceleration. The following Python Script was used to export the ONNX model:

```
from ultralytics import YOLO

# Export the model to ONNX format
model.export(format='onnx')  # creates 'yolov8n.onnx'
```

## Docker 
The project Dockerfile is based on the "ultralytics/ultralytics:8.1.9-python" image, which is an optimized minimal Python environment for lightweight YOLO applications. The produced Docker image is ~6GB due to NVIDIA base images. See https://github.com/ultralytics/yolov5/issues/5708 for discussion. The docker-compose.yaml file facilitates deploying a web service using Docker Compose. It defines a web service for running the Python web application and specifies the port mapping, volumne mounting for code changes.

## Project Setup
1. Clone the GitHub repository.
2. Make sure Docker is installed on your computer. Easiest way would be to install Docker Desktop: https://www.docker.com/products/docker-desktop/
3. Navigate to the cloned GitHub Repository. After that, you can directly run ```docker compose up --build``` to build your image and run the web service. 
4. After the image is built, the web service will run automatically. You can then interact with the REST API (see more on API Usage). 
5. When you are done, you can close the server with ```CTRL+C```.
6. After these steps, you can directly use the ```docker compose up``` command to run the server for future usage.

## API Usage.
There are three easy ways to test out the microservice. To test manually, you can either use Postman or FastAPI's own web interface. As a third option, to automate the process, you can run the python script to validate the microservice is working as expected.

### Postman
1. Run the server.
2. Open up Postman, and create a new collection.
3. Right click on the "New Collection" and click on the "Add Request". Then, select the POST request.
4. Enter the ```http://localhost:8000/detect/``` URL.
5. Go to Body, and select the form-data. Write "input_file" for the key value, and then select the type as "File". For the Value, you can click on the "New file from local machine", and then navigate to the data/test_dataset/images folder. Select one of the images for testing.
6. Click on the "Send" button, and you should receive the response in JSON format.
7. Additionally, you can edit the URL with the label query parameter. As an example, you can write ```http://localhost:8000/detect/?label=spoon ``` and select the image "1.jpg". After you send the request, you should only see the spoon object being returned from the JSON response.
8. You can validate the outputs by comparing with the outputs inside the data/test_dataset/outputs files. The outputs were created without any "label" value.

### FastAPI Web Interface 
1. Run the server.
2. Open up your choice of Web Browser.
3. Enter the http://localhost:8000/docs in the URL. You should see the Swagger UI for testing out the endpoint.
4. Click on the "/detect/" endpoint, and then click on the "Try it out" button on the top right.
5. Specify the optional label parameter and select one of the images from the data/test_dataset/images folder.
6. Click on execute, and you should see the response.
7. You can validate the outputs by comparing with the outputs inside the data/test_dataset/outputs files. The outputs were created without any "label" value.

### Test Script
1. Run the server.
2. Navigate to the GitHub Repo. You can directly run the script on your local from your IDE, and it will start sending requests to the server. However, if you want to run it inside the Docker Container, you can open a shell inside the container by running ```docker-compose exec web sh``` (Inside the GitHub Repo). Then, you can navigate to the test folder with ```cd test```. Lastly, when you enter the command ```python3 object_detection_api_test.py```, the script will be run inside the container.
