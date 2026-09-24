import json
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

PRODUCTS_PATH = 'C:/Users/Yam/Documents/Work Related/Website-Project/Products.csv'
PRODUCTS_EMBEDDINGS_PATH = 'embeddings.csv'


def create_embedding_text(df: pd.DataFrame):
    texts = []
    for index, row in df.iterrows():
        text = (f"Name: {row['name']}\n"
                f"Short Description: {row['short_description']}\n"
                f"Full Description: {row['full_description']}\n")
        texts.append(text)
    return texts


def embed_products():
    df = pd.read_csv(PRODUCTS_PATH)
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    texts_to_embed = create_embedding_text(df)
    embeddings = model.encode(texts_to_embed, normalize_embeddings=True)
    embeddings_df = pd.DataFrame.from_dict({'id': df['id'].to_list(), 'embeddings': embeddings.tolist()})
    embeddings_df.to_csv(PRODUCTS_EMBEDDINGS_PATH, index=False)


def request_based_recommendation(query: str):
    df = pd.read_csv(PRODUCTS_EMBEDDINGS_PATH, converters={"embeddings": json.loads})
    products_embeddings = np.vstack(df['embeddings'].to_numpy())
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    embedding = model.encode(query, normalize_embeddings=True)
    scores = cosine_similarity([embedding], products_embeddings)[0]
    recommendations_ranks = df[["id"]].copy()
    recommendations_ranks["score"] = scores
    recommendations_ranks = recommendations_ranks.sort_values("score", ascending=False)
    return recommendations_ranks


if __name__ == '__main__':
    #embed_products()
    print(request_based_recommendation('I want to go on an adventure'))