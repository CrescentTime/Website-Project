import pandas as pd
import pickle
from sentence_transformers import SentenceTransformer

PRODUCTS_PATH = 'C:/Users/Yam/Documents/Work Related/Website-Project/Products.csv'


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
    embeddings = model.encode(texts_to_embed)
    embeddings_df = pd.DataFrame.from_dict({'id': df['id'].to_list(), 'embeddings': embeddings.tolist()})
    embeddings_df.to_csv('embeddings.csv', index=False)



if __name__ == '__main__':
    embed_products()