import os
import json
import requests
from openai import OpenAI
from dotenv import load_dotenv

# load the env vars
load_dotenv()

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
OPENAI_EMBEDDING_MODEL = 'text-embedding-ada-002'
CHATGPT_MODEL = 'gpt-4-1106-preview'

# get the embedded vector for given input chunk
def get_embedding(chunk):
    url = 'https://api.openai.com/v1/embeddings'
    headers = {
        'content-type': 'application/json; charset=utf-8',
        'Authorization': f"Bearer {OPENAI_API_KEY}"
    }
    data = {
        'model': OPENAI_EMBEDDING_MODEL,
        'input': chunk
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_json = response.json()
    embedding = response_json["data"][0]["embedding"]
    return embedding

# prompt the llm
def get_llm_answer(prompt):
    # aggregate messages array to send to llm
    messages = [{"role": "system", "content": "You're a helpful assistant."}]
    messages.append({"role": "user", "content": prompt})

    # send payload to LLM
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'content-type': 'application/json; charset=utf-8',
        'Authorization': f"Bearer {OPENAI_API_KEY}"
    }
    data = {
        'model': CHATGPT_MODEL,
        'messages': messages,
        'temperature': 1,
        'max_tokens': 1000
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # return answer
    response_json = response.json()
    completion = response_json["choices"][0]["message"]["content"]
    return completion
