# pinecone service for storing embedded text

import pinecone
from app.services.openai_service import get_embedding
import os
from dotenv import load_dotenv

# load the env vars
load_dotenv()

api_key = os.environ["PINE_CONE_API_KEY"]
pc = Pinecone(api_key=api_key)


