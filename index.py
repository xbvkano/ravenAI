import os
import random
import requests
from dotenv import load_dotenv
import re

# Load the .env file
load_dotenv()

# Access the subscription key and endpoint from .env
subscription_key = os.getenv("SUBSCRIPTION_KEY")
endpoint = os.getenv("ENDPOINT")

# characters = [
#             "Kakashi Hatake - Naruto",
#             "Megumi Fushiguro - Jujutsu Kaisen", 
#             "Gale - Baldurs Gate 3",
#             "Leon S. Kennedy - Resident Evil",
#             "Vaxhildan - Vox Machina",
#             "Violet - Arcane",
#             "Touya Kinomoto - Cardcaptor Sakura",
#             "Johnny Silverhand - Cyber punk",
#             "Roronoa Zoro - One Piece"
#             ]

characters = [
    "viktor - arcane",
]


# Define your search query and folder
# query = "Megumi Fushiguro - Jujutsu Kaisen"
folder_path = "./predictions"
# tag_name = "Megumi"

# Create the folder if it doesn't exist
os.makedirs(folder_path, exist_ok=True)

# Set the headers and parameters
headers = {"Ocp-Apim-Subscription-Key": subscription_key}
for character in characters:
    query = character
    tag_name = re.split(r'\s*-\s*', character)[0]
    offset = 50
    params = {"q": query, "count": 5, "offset": offset, "mkt": "en-us"}

    # Make the request
    response = requests.get(endpoint, headers=headers, params=params)

    # Check and parse the response
    if response.status_code == 200:
        results = response.json()
        for i, image in enumerate(results["value"]):
            image_url = image['contentUrl']
            try:
                # Download the image
                print(f"Downloading image {tag_name} {i + 1}: {image_url}")
                image_data = requests.get(image_url).content
                
                # Save the image to the folder
                image_path = os.path.join(folder_path, f"image_{tag_name}_{i + 1}.jpg")
                with open(image_path, 'wb') as f:
                    f.write(image_data)
            except Exception as e:
                print(f"Failed to download image {tag_name} {i + 1}: {e}")
    else:
        print(f"Error: {response.status_code}, {response.text}")
