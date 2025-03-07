# routes for LLM full stack
from . import api_blueprint
from flask import request, jsonify
from app.services import openai_service, pinecone_service, scraping_service
from app.utils.helper_functions import chunk_text, build_prompt

# pc index name
PC_INDEX_NAME = "llm-flask"

# embed and store api endpoint
@api_blueprint.route('/embed-and-store', methods=['POST'])
def embed_and_store():
    # handles scraping the URL, embedding the texts,
    # and uploading to the vector database.
    url = request.json['url']
    print("Embed and store:")
    print("url = " + url + "\n")
    url_text = scraping_service.scrape_website(url)
    chunks = chunk_text(url_text)
    print("chunks = " + str(chunks))
    pinecone_service.embed_chunks_and_upload_to_pinecone(chunks, PC_INDEX_NAME)
    response_json = {
        "message": "Chunks embedded and stored successfully"
    }
    return jsonify(response_json) 

@api_blueprint.route('/handle-query', methods=['POST'])
def handle_query():
    # handle's embedding the user's question,
    # finding relevant context from the vector database,
    # building the prompt for the LLM, and sending
    # the prompt to the LLM for a response.
    question = request.json['question']
    context_chunks = pinecone_service.get_most_similar_chunks_for_query(question, PC_INDEX_NAME)
    prompt = build_prompt(question, context_chunks)
    answer = openai_service.get_llm_answer(prompt)
    return jsonify({"question": question, "answer": answer}) 
