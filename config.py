
import os
import streamlit as st

OPENAI_API_KEY = st.secrets.OPENAI_API_KEY

MILVUS_HOST = st.secrets.MILVUS_HOST
MILVUS_PORT = st.secrets.MILVUS_PORT
MILVUS_COLLECTION_NAME = "ai_gift_recommender"

EMBEDDING_MODEL = "text-embedding-3-large"
EMBEDDING_DIM = 1024 

DEPARTMENT_MAPPING = {
    0: "Darčeky",
    1: "Drogéria",
    2: "Hry a hračky",
    3: "Knihy beletria",
    4: "Školské potreby"
}

SEARCH_PLACEHOLDER = "e.g., knihy pre ženu, vojenská literatúra"
MAX_QUERY_LENGTH = 200

PRODUCTS_CSV_PATH = "data/products.csv"
