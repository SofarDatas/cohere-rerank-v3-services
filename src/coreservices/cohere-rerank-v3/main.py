import json
import os
from fastapi import FastAPI
import cohere


# extract the environment variables
COHERE_API_KEY = os.environ['COHERE_API_KEY']
COHERE_RERANK_MODEL = os.environ['COHERE_RERANK_MODEL']


app = FastAPI()


@app.get("/")
def hello_world() -> dict:
    """
    A simple function to return a Hello World message.

    Returns:
        dict: A dictionary with a greeting.
    """
    return {"Hello": "World"}


@app.post("/rerank")
def rerank(request: dict) -> dict:
    query = request['query']
    documents = request['documents']
    top_n = request.get('top_n', 5)
    rank_fields = request.get('rank_fields', None)
    return_documents = request.get('return_documents', False)
    """
        A function to rerank documents using the Cohere API.

        Args:
            query (str): The query to rerank documents.
            documents (list): The list of documents to rerank.
            top_n (int): The number of documents to return.
            rank_fields (list): The list of fields to rank the documents.
            return_documents (bool): A flag to return the documents.

        Returns:
            dict: A dictionary with the reranked documents.
    """

    cohere_client = cohere.Client(api_key=COHERE_API_KEY)
    rerank_model_name = COHERE_RERANK_MODEL

    rerank_response = cohere_client.rerank(
        model=rerank_model_name, query=query, documents=documents, top_n=top_n, return_documents=return_documents, rank_fields=rank_fields)
    # Convert the RerankResponse object to a dictionary and return it
    return {
        "id": rerank_response.id,
        "results": [
            {
                "document": result.document.__dict__,
                "index": result.index,
                "relevance_score": result.relevance_score
            } for result in rerank_response.results
        ],
        "meta": {
            "api_version": rerank_response.meta.api_version.version,
            "billed_units": rerank_response.meta.billed_units.search_units
        }
    }
