import openai
import os
import argparse

openai.api_key = os.getenv("OPENAI_API_KEY")

prompt = """
    You will receive a file's contents as text. Generate a code review for the
    file. Indicate what changes should be made to improve its style,
    performance, readability, and maintainability. If there are any reputable
    libraries that could be introduced to improve the code, suggest them.
    Be kind and constructive. For each suggested change, include line numbers to which
    you are referring. 
"""


def make_code_review_request(file_content: str, model:str) -> str:
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"Code review the following file: {file_content}"}
    ]

    res = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    content = res["choices"][0]["message"]["content"]
    return content


def read_file_content(path: str) -> str:
    with open(path, "r") as file:
        file_content = file.read()
    return file_content


def main():
    parser = argparse.ArgumentParser(description="Simple code reviewer for a file")
    parser.add_argument("file")
    parser.add_argument("--model", default="gpt-4")
    args = parser.parse_args()

    file_content = read_file_content(args.file)
    review = make_code_review_request(file_content, args.model)
    print(review)


if __name__ == "__main__":
    main()