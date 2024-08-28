import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
# Ensure stopwords are downloaded
nltk.download('stopwords')
nltk.download('punkt')

class Preprocessing:
        
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))

    def preprocess_list_of_comments(self, comments_list: List[str]):
        
        list_of_cleanded_comment = []
        
        for comment in comments_list:
            
            cleaned_comment = self.preprocess_single_text(comment)
            list_of_cleanded_comment.append(cleaned_comment)
        
        return list_of_cleanded_comment
    
    def preprocess_single_text(self, text):
        # Remove new lines and extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove special characters (keep only alphanumeric and punctuation)
        text = re.sub(r'[^\w\s]', '', text)
        
        # Tokenize the text
        tokens = word_tokenize(text.lower())
        
        # Remove stop words and non-alphabetic tokens
        tokens = [word for word in tokens if word.isalpha() and word not in self.stop_words]
        
        return tokens
