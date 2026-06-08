import re
import nltk

# Download required NLTK data on Streamlit Cloud
for resource in ["stopwords", "punkt", "punkt_tab"]:
    try:
        nltk.data.find(
            f"corpora/{resource}" if resource == "stopwords"
            else f"tokenizers/{resource}"
        )
    except LookupError:
        nltk.download(resource)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stop_words = set(stopwords.words('english'))

def clean_text(text):

    text = text.lower()

    text = re.sub(r'[^a-zA-Z ]', '', text)

    words = word_tokenize(text)

    filtered_words = [
        word for word in words
        if word not in stop_words
    ]

    return " ".join(filtered_words)