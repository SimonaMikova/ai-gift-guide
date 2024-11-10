import streamlit as st
from pymilvus import connections, Collection
from langchain_openai import OpenAIEmbeddings
from config import (
    OPENAI_API_KEY,
    EMBEDDING_MODEL,
    EMBEDDING_DIM,
    MILVUS_HOST,
    MILVUS_PORT,
    DEPARTMENT_MAPPING
)
from typing import List, Optional
import pandas as pd


@st.cache_resource
def initialize_embeddings() -> OpenAIEmbeddings:
    """Initialize the OpenAI embeddings model."""
    embed_model = OpenAIEmbeddings(
        openai_api_key=OPENAI_API_KEY,
        model=EMBEDDING_MODEL,
        dimensions=EMBEDDING_DIM
    )
    return embed_model


@st.cache_resource
def initialize_milvus():
    """Initialize Milvus connection."""
    connections.connect("default", host=MILVUS_HOST, port=MILVUS_PORT)


def get_embedding(text: str, embed_model: OpenAIEmbeddings) -> Optional[List[float]]:
    """Generate embedding for the given text."""
    try:
        return embed_model.embed_query(text)
    except Exception as e:
        st.error(f"Error getting embedding: {e}")
        return None
    

def search_products(
    query_embedding: List[float],
    collection_name: str,
    top_k: int = 5
) -> pd.DataFrame:
    """Search for similar products using vector similarity."""

    collection = Collection(collection_name)
    collection.load()

    search_params = {
        "metric_type": "L2",
        "params": {"nprobe": 15},
    }

    results = collection.search(
        data=[query_embedding],
        anns_field="embedding",
        param=search_params,
        limit=top_k,
        output_fields=["id_tovar", "oddelenie"]
    )

    matched_products = []
    for hits in results:
        for hit in hits:
            matched_products.append({
                'id_tovar': hit.entity.get('id_tovar'),
                'oddelenie': DEPARTMENT_MAPPING.get(hit.entity.get('oddelenie'), "Unknown"),
                'distance': hit.distance
            })

    return pd.DataFrame(matched_products)
