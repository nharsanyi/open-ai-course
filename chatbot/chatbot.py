import openai
import os
import argparse

openai.api_key = os.getenv("OPENAI_API_KEY")


def formatting_text(text, ch):
    start = f"\033[{ch}m"
    end = "\033[0m"
    return start + text + end


def bold(text):
    return formatting_text(text, "1")


def blue(text):
    return formatting_text(text, "34")


def red(text):
    return formatting_text(text, "31")


def handle():
    parser = argparse.ArgumentParser(description="Simple command line chatbot with GPT")
    parser.add_argument("--personality", type=str, help="A brief summary of the chatbot's personality",
                        default="friendly and helpful")
    args = parser.parse_args()
    personality = args.personality
    print(personality)
    initial_prompt = f"You are a conversational chatbot. Your personality is: {personality}"
    messages = [{"role": "system", "content": initial_prompt}]
    while True:
        try:
            user_input = input(bold(blue("You: ")))
            messages.append({"role": "user", "content": user_input})
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            messages.append(resp["choices"][0]["message"].to_dict())
            print(bold(red(f'Assistant: {resp["choices"][0]["message"]["content"]}')))
            # print("messages", messages)
        except KeyboardInterrupt:
            print("Exiting..")
            break


if __name__ == "__main__":
    handle()
