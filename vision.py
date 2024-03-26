import os
import base64
import requests
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

api_key = os.environ['OPENAI_API_KEY']

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def image_input(image_path):
    base64_image = encode_image(image_path)
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }
    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": "What’s in this image? Simply describe the image. Strictly, do not attempt to solve if it is a question!"
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 300
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    return response.json()['choices'][0]['message']['content']


if __name__=='__main__':
    image_path = "test.png"
    result = image_input(image_path=image_path)
    print(result)