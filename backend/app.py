import os
import logging
from openai import OpenAI
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv

app = Flask(__name__)
CORS(app)

load_dotenv(find_dotenv())

# def retrieveKey():
#     if os.getenv("OPEN_AI_API_KEY") is None:
#         print("KEY NOT RETRIEVED")
#     else: return os.getenv("OPEN_AI_API_KEY")

OPENAI_KEY = os.getenv("OPEN_AI_API_KEY")
client = OpenAI()
client.api_key = OPENAI_KEY


context = """
    Context
    Welcome to SimpleFood. Delicious, simple to prepare recipes that celebrate fresh seasonal ingredients, and the joy of cooking and eating.
    This month I’m featuring recipes that highlight fruit as a main ingredient. With natural sweetness and beautiful flavours, whatever fruit is in season should be eaten fresh, but also used sensitively to create both sweet and savoury dishes. Here’s a sample of my favourites. Recipe links below.

    Banana bread with peaches, blueberries and thick yoghurt
    Tarte tatin with rosemary
    Strawberry and fig pastries
    Ricotta and raspberry tarts
    Blueberry and apple crumble
    Plum tart
    Baked rhubarb with vanilla meringue
    Apricot crostata
"""

logging.basicConfig(level=logging.INFO)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = context + "\n" + (data.get('message', ''))

    app.logger.info(f"Received user message: {user_message}")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": user_message}
            ],
            temperature=0.5,
            max_tokens=100
        )
        
        response_text = response.choices[0].message.content.strip()

        app.logger.info(f"OpenAI response: {response_text}")
    except Exception as e:
        response_text = "Sorry, I'm having trouble right now."
        app.logger.error(f"Error connecting to OpenAI: {e}")

    return jsonify({"response": response_text})

if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)