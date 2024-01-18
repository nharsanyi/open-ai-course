import json
import requests
from pathlib import Path
import base64


def download_image(image_url, local_path):
    image_content = requests.get(image_url).content
    save_image_content(image_content, "url", local_path)


def save_image_content(image_content, image_format, local_path):
    with open(local_path, "wb") as f:
        if image_format == "b64_json":
            decoded_image = base64.b64decode(image_content)
            f.write(decoded_image)
        else:
            f.write(image_content)