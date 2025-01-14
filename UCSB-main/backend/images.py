import requests
import os
import time
import cv2
import numpy as np
import psycopg2
from datetime import datetime


# Define the base folder to save images and data
base_folder = "images"
data_folder = "data"

# PostgreSQL database connection parameters
db_host = "localhost"
db_port = 5432
db_name = "gaucho"
db_user = "postgres"  # Replace with your PostgreSQL username
db_password = "root"  # Replace with your PostgreSQL password

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=db_host,
    port=db_port,
    database=db_name,
    user=db_user,
    password=db_password
)
cursor = conn.cursor()

# Ensure the data and image folders exist
if not os.path.exists(data_folder):
    os.makedirs(data_folder)
if not os.path.exists(base_folder):
    os.makedirs(base_folder)

# Define the API URLs and their corresponding locations
urls = [
    {"url": "https://api.ucsb.edu/dining/cams/v2/still/carrillo?ucsb-api-key=7oIGngArZiu7cS8hiFxpz17eP4XaUQCp&ts=1736639433924", "location": "carrillo"},
    {"url": "https://api.ucsb.edu/dining/cams/v2/still/de-la-guerra?ucsb-api-key=7oIGngArZiu7cS8hiFxpz17eP4XaUQCp&ts=1736639573923", "location": "de-la-guerra"},
    {"url": "https://api.ucsb.edu/dining/cams/v2/still/portola?ucsb-api-key=7oIGngArZiu7cS8hiFxpz17eP4XaUQCp&ts=1736639558924", "location": "portola"}
]

# Load a pre-trained YOLO model for person detection
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Function to count people in an image
def count_people(image_path):
    img = cv2.imread(image_path)
    height, width, _ = img.shape

    # Prepare the image for the YOLO model
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outputs = net.forward(output_layers)

    # Count people
    count = 0
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and class_id == 0:  # Class ID 0 is for 'person'
                count += 1
    return count

# Function to fetch and save images
def fetch_images():
    for entry in urls:
        api_url = entry["url"]
        location = entry["location"]
        location_folder = os.path.join(base_folder, location)

        # Ensure the location folder exists
        if not os.path.exists(location_folder):
            os.makedirs(location_folder)

        # Fetch the image data from the API
        response = requests.get(api_url)

        if response.status_code == 200:
            # Generate a unique file name with a timestamp
            timestamp = int(time.time())
            dt_object = datetime.fromtimestamp(timestamp)
            timestamp_string = dt_object.strftime('%Y-%m-%d %H:%M:%S')  # Format: YYYY-MM-DD HH:MM:SS

            image_name = os.path.join(location_folder, f"{location}_{timestamp}.jpg")

            # Save the image
            with open(image_name, 'wb') as f:
                f.write(response.content)
            print(f"Image saved to {image_name}")

            # Count people in the image
            people_count = count_people(image_name)
            wait_time = people_count * 20  # Calculate wait time based on the number of people

            # Prepare data for PostgreSQL
            data = (timestamp_string, location, wait_time)

            # Insert data into PostgreSQL
            cursor.execute(
                "INSERT INTO wait_time (timestamp, dining_hall, wait_time) VALUES (%s, %s, %s)",
                data
            )
            conn.commit()  # Commit the transaction

        else:
            print(f"Failed to fetch data from {api_url}. Status code: {response.status_code}")

# Main loop to fetch images periodically
try:
    while True:
        fetch_images()
        print("Waiting for 20 seconds before the next fetch...")
        time.sleep(20)
except KeyboardInterrupt:
    print("Script stopped by the user.")
finally:
    cursor.close()
    conn.close()  # Close the database connection