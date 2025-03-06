# helper functions for chunking LLM text

PROMPT_LIMIT = 3750

# chunk the input text for embedding
def chunk_text(text, chunk_size=200):
    # split the text by sentences to avoid breaking in the middle of a sentence
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        # check if adding the next sentence exceeds the chunk size
        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += sentence + '. '
        else:
            # if the chunk reaches the desired size, add it to chunks list
            chunks.append(current_chunk)
            current_chunk = sentence + '. '

    # add last chunk if it's not empty
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

# build the prompt using the context to the LLM
def build_prompt(query, context_chunks):
    # create start and end of the prompt
    prompt_start = (
        "Answer the question based on the context below. If you don't know the answer based on the context provided below, just respond with 'I don't know' instead of making up an answer. Return just the answer to the question, don't add anything else. Don't start your response with the word 'Answer:'. Make sure your response is in markdown format\n\n"+
        "Context:\n"
    )
    prompt_end = (
        f"\n\nQuestion: {query}\nAnswer:"
    )
   
    # append context chunks until we hit the limit of tokens
    prompt = ""
    for i in range(1, len(context_chunks)):
        if len("\n\n---\n\n".join(context_chunks[:i])) >= PROMPT_LIMIT:
            prompt = (
                prompt_start +
                "\n\n---\n\n".join(context_chunks[:i-1]) +
                prompt_end
            )
            break
        elif i == len(context_chunks)-1:
            prompt = (
                prompt_start +
                "\n\n---\n\n".join(context_chunks) +
                prompt_end
            )
    return prompt
