from pathlib import Path
from bertopic import BERTopic
from umap import UMAP
from sklearn.feature_extraction.text import CountVectorizer
from bertopic.representation import KeyBERTInspired
from sentence_transformers import SentenceTransformer
from hdbscan import HDBSCAN
from bertopic.vectorizers import ClassTfidfTransformer
import os

def load_posts(folder_path):
    posts = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                posts.append(f.read())

    print(f"Loaded documents: {len(posts)}")
    print(f"Empty documents: {sum(1 for p in posts if not p.strip())}")
    return posts

reddit_text_files = Path(__file__).parent.parent / "data" / "post_txt" / "reddit_txt"

reddit_posts = load_posts(reddit_text_files)

#platform_stopwords = ["don"]

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)
umap_model = UMAP(
    n_neighbors=5, 
    n_components=5, 
    min_dist=0.0, 
    metric='cosine', 
    random_state=42
)
hdbscan_model = HDBSCAN(
    min_cluster_size=5, 
    min_samples=4, 
    metric='euclidean', 
    cluster_selection_method='leaf', 
    prediction_data=True
)
vectorizer_model = CountVectorizer(
    #stop_words=list(
    #set(CountVectorizer(stop_words="english").get_stop_words()).union(platform_stopwords)), 
    stop_words="english", 
    ngram_range=(1, 1), 
    min_df=3, 
    max_df=0.8 
) 
ctfidf_model = ClassTfidfTransformer(
    reduce_frequent_words=True
) 
representation_model = KeyBERTInspired(
)

topic_model = BERTopic(
    embedding_model=embedding_model,
    umap_model=umap_model,
    hdbscan_model=hdbscan_model,
    vectorizer_model=vectorizer_model,
    ctfidf_model=ctfidf_model,
)

topics, probabilities = topic_model.fit_transform(reddit_posts)
hierarchical_topics = topic_model.hierarchical_topics(reddit_posts)

# storing topic-word representations
topic_info = topic_model.get_topic_info()
topic_info.to_csv(Path(__file__).parent.parent / "output" / "topics" / "reddit_topics.csv", index=False)

# visualization documents
topic_model.visualize_documents(reddit_posts).write_html(Path(__file__).parent.parent / "output" / "figures" / "reddit_documents.html")
topic_model.visualize_documents(reddit_posts).write_image(Path(__file__).parent.parent / "output" / "figures" / "reddit_documents.png")

# visualization hierarchy
topic_model.visualize_hierarchy(hierarchical_topics=hierarchical_topics).write_html(Path(__file__).parent.parent / "output" / "figures" / "reddit_hierarchy.html")

print("**********")
print(" Reddit ")
print("**********")

print("Number of topics:", len(set(topics)))
print(topic_model.get_topic_info())

print(f"\nTopic words -1 (outliers/noise): {topic_model.get_topic(-1)}")
print(f"\nTopic words 0: {topic_model.get_topic(0)}")
print(f"\nTopic words 1: {topic_model.get_topic(1)}")
print(f"\nTopic words 2: {topic_model.get_topic(2)}")
print(f"\nTopic words 3: {topic_model.get_topic(3)}")
print(f"\nTopic words 4: {topic_model.get_topic(4)}")
print(f"\nTopic words 5: {topic_model.get_topic(5)}")
print(f"\nTopic words 6: {topic_model.get_topic(6)}")
print(f"\nTopic words 7: {topic_model.get_topic(7)}")
print(f"\nTopic words 8: {topic_model.get_topic(8)}")
print(f"\nTopic words 9: {topic_model.get_topic(9)}")
print(f"\nTopic words 10: {topic_model.get_topic(10)}")
print(f"\nTopic words 11: {topic_model.get_topic(11)}")
print(f"\nTopic words 12: {topic_model.get_topic(12)}")
print(f"\nTopic words 13: {topic_model.get_topic(13)}")
print(f"\nTopic words 14: {topic_model.get_topic(14)}")
print(f"\nTopic words 15: {topic_model.get_topic(15)}")
print(f"\nTopic words 16: {topic_model.get_topic(16)}")
# this is messy, change it