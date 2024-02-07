import requests
import json
import os

url = 'http://localhost:8000/detect/'

script_dir = os.path.dirname(os.path.abspath(__file__))
image_paths = list()
label_paths = list()

for i in range(5):
    image_paths.append(os.path.join(script_dir, f'../data/test_dataset/images/{i + 1}.jpg'))

for i in range(5):
    label_paths.append(os.path.join(script_dir, f'../data/test_dataset/outputs/{i + 1}.txt'))

# Function to send request to the API and get response
def get_response(image_path):
    files = {'input_file': open(image_path, 'rb')}
    response = requests.post(url, files=files)
    return response.json()

# Iterate over the image paths and compare responses
for i in range(5):
    api_response = get_response(image_paths[i])
    
    # Read the expected response from file
    with open(label_paths[i], 'r') as file:
        expected_response = json.load(file)
    
    # Compare responses
    if api_response == expected_response:
        print(f'Response for {i + 1}.jpg is as expected.')
    else:
        print(f'Response for {i + 1}.jpg does not match the expected response.')
