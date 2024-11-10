import streamlit as st
import pandas as pd
import time
from preprocessor import clean_text
from database import (
    initialize_embeddings,
    initialize_milvus,
    get_embedding,
    search_products
)
from config import (
    PRODUCTS_CSV_PATH,
    MILVUS_COLLECTION_NAME,
    SEARCH_PLACEHOLDER,
    MAX_QUERY_LENGTH
)

st.set_page_config(page_title="🎁 AI Gift Guide", layout="wide")

try:
    embed_model = initialize_embeddings()
    initialize_milvus()
    st.session_state['initialized'] = True
except Exception as e:
    st.error(f"Failed to initialize connections: {e}")
    st.session_state['initialized'] = False

st.title("🎁 AI Gift Guide")
st.markdown("Find the perfect gift based on your interests!")

@st.cache_data(ttl=3600)
def load_product_data():
    return pd.read_csv(PRODUCTS_CSV_PATH)

try:
    products_df = load_product_data()
except Exception as e:
    st.error(f"Failed to load product data: {e}")
    st.stop()

search_query = st.text_input(
    "Enter your search:",
    placeholder=SEARCH_PLACEHOLDER
)

st.subheader("Quick Categories")

col1, col2, col3, col4, col5, col6 = st.columns(6)

categories = [
    ("Milovníci Harryho Pottera", "harry_potter"),
    ("Pre malé princezné", "princess"),
    ("Krížovky pre starších", "crosswords"),
    ("Milovníci puzzle", "puzzle"),
    ("Pre ženy po štyridsiatke", "women_over40"),
    ("Pre malých staviteľov", "builders")
]

for idx, (category, key) in enumerate(categories):
    with [col1, col2, col3, col4, col5, col6][idx]:
        if st.button(category, key=key):
            search_query = category

if search_query and len(search_query) > MAX_QUERY_LENGTH:
    st.warning(f"Search query is too long. Please limit to {MAX_QUERY_LENGTH} characters.")
    search_query = '' 

if search_query and st.session_state.get('initialized', False):
    start_time = time.time()
    cleaned_query = clean_text(search_query)

    with st.spinner("Searching for products..."):
        query_embedding = get_embedding(search_query, embed_model)

        if query_embedding:
            results_df = search_products(
                query_embedding=query_embedding,
                collection_name=MILVUS_COLLECTION_NAME,
                top_k=20
            )

            results = results_df.merge(products_df, on='id_tovar', how='left')
            elapsed_time = time.time() - start_time

            if not results.empty:
                st.subheader("Recommended Products")

                st.caption(f"Search completed in {elapsed_time:.2f} seconds")

                st.dataframe(
                    results[['id_tovar', 'name', 'cleaned_description', 'oddelenie', 'distance']],
                    column_config={
                        "id_tovar": "Product ID",
                        "name": "Title",
                        "cleaned_description": "Description",
                        "oddelenie": "Department",
                        "distance": "Distance"
                    },
                    hide_index=True,
                    use_container_width=True
                )
            else:
                st.info("No products found matching your search.")
        else:
            st.error("Failed to process your search query. Please try again.")
else:
    st.info("Enter a search term or select one of the quick categories above to get started!")
