import re
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from config import SPACY_MODEL

# Load spaCy model gracefully with automatic download fallback
try:
    nlp = spacy.load(SPACY_MODEL)
except OSError:
    try:
        import spacy.cli
        spacy.cli.download(SPACY_MODEL)
        nlp = spacy.load(SPACY_MODEL)
    except Exception:
        # Minimal fallback in case spaCy or internet connection fails during test
        nlp = None

def clean_text_basic(text: str) -> str:
    """
    Cleans raw text by removing emails, URLs, phone numbers, and special characters.
    """
    if not text:
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
    
    # Remove Email addresses
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', ' ', text)
    
    # Remove Phone Numbers (standard formats)
    text = re.sub(r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b', ' ', text)
    
    # Remove extra spaces/newlines
    text = re.sub(r'\s+', ' ', text)
    
    # Keep alphanumeric characters and basic punctuation for parsing
    text = re.sub(r'[^\w\s\-\.\,\/\+]', ' ', text)
    
    return text.strip()

def preprocess_text(text: str) -> list:
    """
    Cleans text, tokenizes, removes stopwords and punctuation, and lemmatizes tokens.
    Returns a list of lemmatized word tokens.
    """
    cleaned = clean_text_basic(text)
    if not cleaned:
        return []
    
    if nlp is not None:
        doc = nlp(cleaned)
        tokens = [
            token.lemma_ for token in doc 
            if not token.is_stop and not token.is_punct and token.text.strip()
        ]
        return tokens
    else:
        # Fallback split-based cleaning if spaCy is not available
        words = cleaned.split()
        return [
            re.sub(r'[^\w]', '', w) for w in words 
            if w not in STOP_WORDS and re.sub(r'[^\w]', '', w)
        ]

def get_cleaned_string(text: str) -> str:
    """
    Cleans, lemmatizes and returns a single unified string of processed text.
    """
    return " ".join(preprocess_text(text))
