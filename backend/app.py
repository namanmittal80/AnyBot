from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_rag import initialize_services, create_rag_chain, process_query

app = Flask(__name__)
CORS(app)

index, embedding_model, llm = initialize_services()
rag_chain = create_rag_chain(index, embedding_model, llm)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = (data.get('message', ''))

    app.logger.info(f"Received user message: {user_message}")

    try:
        response = process_query(rag_chain, user_message)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)