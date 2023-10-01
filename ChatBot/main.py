import argparse
import re

# GPT Library
import g4f

# Server
from flask import Flask, jsonify, request
from g4f.Provider import (
    Bard,
    Bing,
    HuggingChat,
    OpenaiChat,
    OpenAssistant,
)

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
async def index() -> str:
    """
    Main function
    """
    # Starts the bot and gets the input
    print("Initializing...")
    question = None

    
    if request.method == "GET":
        question = request.args.get("text")
        print("get")
    else:
        file = request.files["file"]
        text = file.read().decode("utf-8")
        question = text
        print("Post reading the file", question)

    if question is None:
        return "<p id='response'>Please enter a question</p>"
    print("\nInput: " + question)
    
    # Set with provider
    response = (
        await g4f.Provider.ChatgptAi.create_async(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question,}],
            
        )
    )
    print("response: ",response)

    return jsonify({"content":response})

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--remove-sources",
        action='store_true',
        required=False,
        help="needed if you want to remove the sources from the response",
    )
    args = parser.parse_args()

    #Starts the server, change the port if needed
    app.run("0.0.0.0", port=5500, debug=False)
