"""
Text preprocessing module for news articles
"""
import re
import nltk
import ssl
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Fix SSL certificate issue
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))


def preprocess_text(text):
    """
    Preprocess text by:
    1. Converting to lowercase
    2. Removing special characters and numbers
    3. Removing extra whitespace
    4. Removing stopwords
    5. Lemmatizing words
    
    Args:
        text (str): Raw text to preprocess
    
    Returns:
        str: Preprocessed text
    """
    if not isinstance(text, str):
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # Remove stopwords and lemmatize
    tokens = [lemmatizer.lemmatize(token) for token in tokens 
              if token not in stop_words and len(token) > 2]
    
    # Join back to string
    processed_text = ' '.join(tokens)
    
    return processed_text


def validate_input(text):
    """
    Validate input text
    
    Args:
        text (str): Text to validate
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if not text or not isinstance(text, str):
        return False, "Please provide valid text input"
    
    text = text.strip()
    
    if len(text) < 10:
        return False, "Text must be at least 10 characters long"
    
    if len(text) > 5000:
        return False, "Text must not exceed 5000 characters"
    
    # Check if text has enough words after preprocessing
    processed = preprocess_text(text)
    words = processed.split()
    
    if len(words) < 3:
        return False, "Text must contain at least 3 meaningful words"
    
    return True, ""
