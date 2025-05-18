import requests
import base64

API_KEY = "sk-gCtYeW5UyJvrv02yyw3R5KfoLbslS9NBMPLwI9xupwvkpIZx"

url = "https://api.stability.ai/v2beta/generation/stable-diffusion-v1-6/text-to-image"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "text_prompts": [
        {"text": "A hand-drawn pencil sketch of children playing in a garden, simple lines, black and white"}
    ],
    "cfg_scale": 7,
    "height": 512,
    "width": 512,
    "samples": 1,
    "steps": 30
}

response = requests.post(url, headers=headers, json=payload)

if response.status_code == 200:
    img_data = response.json()['artifacts'][0]['base64']
    img_bytes = base64.b64decode(img_data)
    with open("sketch_output.png", "wb") as f:
        f.write(img_bytes)
    print("Sketch image saved as sketch_output.png")
else:
    print(f"Failed: {response.status_code} {response.text}")
