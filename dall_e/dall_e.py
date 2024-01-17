import openai
import os
import argparse
import json
import requests
from pathlib import Path
import base64

openai.api_key = os.getenv("OPENAI_API_KEY")
image_directory_name = "images"
Path(image_directory_name).mkdir(parents=True, exist_ok=True)


def main():
    parser = argparse.ArgumentParser(description="Image generator using Dall-E")
    parser.add_argument("--query", type=str, default="Generate an image about an astronaut lounging "
                                                     "in a tropical resort in space in cubist style")
    parser.add_argument("--response_format", type=str, help="The desired format for the api", default="url")
    args = parser.parse_args()

    response_format = args.response_format
    query = args.query

    img = generate_image(query, response_format)
    if response_format == "url":
        download_image(img)
    else:
        save_image_content(img, response_format)

    variation_url = create_img_variation(f"{image_directory_name}/astronaut.png")
    download_image(variation_url, f"{image_directory_name}/astronaut_variation.png")
    edit_url = create_img_edit(img_path=f"{image_directory_name}/great_wave.png",
                               mask_path=f"{image_directory_name}/great_wave_mask.png",
                               prompt="A pink flamingo floaty")
    download_image(edit_url, f"{image_directory_name}/great_wave_edit.png")


def create_img_edit(img_path, mask_path, prompt):
    resp = openai.Image.create_edit(image=open(img_path, "rb"),
                                    mask=open(mask_path, "rb"),
                                    prompt=prompt,
                                    n=1,
                                    size="1024x1024")
    url = resp["data"][0]["url"]
    print(url)
    return url


def create_img_variation(img_path: str):
    resp = openai.Image.create_variation(
        image=open(img_path, "rb"),
        n=1,
        size="1024x1024"
    )
    return resp['data'][0]['url']


def generate_image(prompt: str, response_format="url"):
    res = openai.Image.create(
        prompt=prompt,
        size="1024x1024",
        n=1,
        response_format=response_format  # or b64_json
    )
    return res["data"][0][response_format]


def download_image(image_url, local_path=f"{image_directory_name}/astronaut.png"):
    image_content = requests.get(image_url).content
    save_image_content(image_content, "url", local_path)


def save_image_content(image_content, image_format, local_path):
    with open(local_path, "wb") as f:
        if image_format == "b64_json":
            decoded_image = base64.b64decode(image_content)
            f.write(decoded_image)
        else:
            f.write(image_content)


if __name__ == "__main__":
    main()
