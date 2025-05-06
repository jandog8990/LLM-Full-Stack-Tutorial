# LLM-Full-Stack-Tutorial
LLM fullstack tutorial using Flask, OpenAI and PineCone

## Pinecone vector db
llm-flask with 1536 dimensions.

## API Blueprint Endpoints
1. The first embeds and stores scraped websites
    * <url>/embed-and-store
2. The second handles a user's query by embedding the question
    * <url>/handle-query

## Helper classes for querying
1. services/scraping_service.py - uses BeautifulSoup for website scraping
2. utils/helper_functions.py - LLM helper functions
    * chunk_text(text) - chunk text for given sentences
    * build_prompt(query) - build the llm prompt using context chunks

## OpenAI service 
1. services/openai_service.py - issues calls to OpenAI for embeddings/prompts
    * get_embedding(chunk) - queries openai for chunk embeddings
    * get_llm_answer(prompt) - issues prompt to ChatGPT model

## PineCone service
1. services/pinecone_service.py - embeds chunks and uploads to VectorDB
    * embed_chunks_and_upload_to_pinecone(chunks, index) - embed given chunks and upload to the PineCone serverless server
    * get_most_similar_chunks_for_query(query, index) - get embeddings for the given query, and then query the index

## Run the server locally
1. python run.py
2. Example curl query:
```
curl -X POST http://localhost:5000/handle-query \
     -H "Content-Type: application/json" \
     -d '{"question":"Why do we provide ChatGPT with a custom knowledge base?"}'
```
