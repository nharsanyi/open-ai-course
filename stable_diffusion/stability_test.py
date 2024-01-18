
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import os
import io
from PIL import Image
from utils import image_utils

key = os.getenv("STABILITY_AI_KEY")


def main():
    print("start")
    stability_api = client.StabilityInference(
        key=key,
        verbose=True
    )
    responses = stability_api.generate(
        prompt="Cute little kittie with princesses, playing in a desert",
        seed=11223344,
        steps=30,
        cfg_scale=8.0,
        width=512,
        height=512,
        samples=1,
        sampler=generation.SAMPLER_K_DPMPP_2M
    )
    for resp in responses:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                print("Your request activated the API's safety filters and could not be processed.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                img.save('images/stability_test.png')


if __name__ == "__main__":
    main()