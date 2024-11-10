import re

def clean_text(text):
    """
    Basic text cleaning: lowercase, remove special characters, extra spaces,
    keep diacritics, and retain numbers.
    """
    text = text.lower()
    
    text = re.sub(r'http\S+|www.\S+', '', text)
    
    text = re.sub(r'\S+@\S+', '', text)
    
    text = re.sub(r'[^a-záäčďéěíľĺňóôřšťúůýž0-9\s]', ' ', text)
    
    text = ' '.join(text.split())
    
    return text
