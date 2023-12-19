import json

from flask import Flask, render_template, request
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__,
            template_folder='templates',
            static_folder='static',
            static_url_path=''
            )


def get_colours(msg):
    prompt = f"""
        You are a colour palette generating assistant that responds to text prompts for colour palettes. 
        You should generate colour palettes that fits the theme, mood, or instructions in the prompt.
        
        The palettes should contain between 2 and 8 colours.
        
        Q: Convert the following verbal description of a colour palette into a list of colours:
        The Mediterranean Sea
        A: ["#006699", "#66CCCC", "#F0E68C", "#008000", "#F08080"]
        
        Q: Convert the following verbal description of a colour palette into a list of colours:
        sage, nature, earth
        A: ["#EDF1D6", "#9DC08B", "#609966", "#40513B"]
        
        Q: Convert the following verbal description of a colour palette into a list of colours: {msg}
        A:
    """
    response = openai.ChatCompletion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=200
    )
    colours = response["choices"][0]["text"]
    return json.loads(colours)


def get_colours_with_chat_api(msg):
    messages = [
        {"role": "system", "content": "You are a colour palette generating assistant that responds to text prompts for colour palettes."},
        {"role": "user", "content": "Convert the following verbal description of a colour palette into a list of colours"},
        {"role": "assistant", "content": '["#006699", "#66CCCC", "#F0E68C", "#008000", "#F08080"]'},
        {"role": "user", "content": "Convert the following verbal description of a colour palette into a list of colours: sage, nature, earth"},
        {"role": "assistant", "content": '["#EDF1D6", "#9DC08B", "#609966", "#40513B"]'},
        {"role": "user", "content": f"Convert the following verbal description of a colour palette into a list of colours: {msg}"}

    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=200
    )
    colours = response["choices"][0]["message"]["content"]
    return json.loads(colours)

@app.route("/palette", methods=["POST"])
def prompt_to_palette():
    app.logger.info("Hit the post request route")
    query = request.form.get("query")
    app.logger.info(query)
    # colours = get_colours(query)
    colours = get_colours_with_chat_api(query)

    return {"colours": colours}


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
