# pinecone service for storing embedded text

from pinecone import Pinecone, ServerlessSpec
from app.services.openai_service import get_embedding
import os
from dotenv import load_dotenv

# load the env vars
load_dotenv()

api_key = os.environ["PINE_CONE_API_KEY"]
pc = Pinecone(api_key=api_key)
EMBEDDING_DIM = 1536

# embed text chunks and upload to PC vectorDB
def embed_chunks_and_upload_to_pinecone(chunks, index_name):
    # del index if it exists
    if index_name in pc.list_indexes():
        pc.delete_index(name=index_name)

    # create new index in PineCone for embedded data
    pc.create_index(name=index_name,
        dimension=EMBEDDING_DIM,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-west-2"
        ))
    index = pc.Index(index_name)

    # embed each chunk and aggregate embeddings
    embeddings_with_ids = []
    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        embeddings_with_ids.append((str(i), embedding, chunk))

    # upload the embeddings and texts for each chunk
    upserts = [(id, vec, {"chunk_text": text}) for id, vec, text in embeddings_with_ids]
    index.upsert(vectors=upserts)

# get the top k contexts for the given query
def get_most_similar_chunks_for_query(query, index_name):
    question_embedding = get_embedding(query)
    index = pc.Index(index_name)
    query_results = index.query(vector=question_embedding, top_k=3, include_metadata=True)
    context_chunks = [x['metadata']['chunk_text'] for x in query_results['matches']]
    return context_chunks
