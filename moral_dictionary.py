import gensim.downloader as api
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


moral_dict = {
    'care': ['support', 'compassion', 'empathy'],
    'harm': ['damage', 'injury', 'suffer'],
    'fairness': ['justice', 'equality', 'impartiality'],
    'cheating': ['fraud', 'deceit', 'dishonesty'],
    'loyalty': ['patriot', 'allegiance', 'faithful'],
    'betrayal': ['traitor', 'betray', 'deceit'],
    'authority': ['leadership', 'obedience', 'respect'],
    'subversion': ['rebel', 'resist', 'dissent'],
    'sanctity': ['sacred', 'holy', 'reverence'],
    'degradation': ['corrupt', 'pollute', 'defile']
}

# Load the pre-trained Word2Vec model
word2vec_model = api.load("word2vec-google-news-300")

class MoralCentroids:
    
    def __init__(self, moral_dict, word2vec_model):
        self.moral_dict = moral_dict
        self.word2vec_model = word2vec_model
        self.centroids = self.calculate_centroids()

    def calculate_centroids(self):
        centroids = {}
        
        for dimension, words in self.moral_dict.items():
            word_vectors = []
            
            for word in words:
                if word in self.word2vec_model.key_to_index:
                    word_vectors.append(self.word2vec_model[word])
            
            if word_vectors:
                # Calculate the mean vector (centroid)
                centroid = np.mean(word_vectors, axis=0)
                # Normalize the centroid so it has a unit length
                centroids[dimension] = centroid / np.linalg.norm(centroid)
            else:
                centroids[dimension] = None  # Handle cases where no word vector was found
                
        return centroids

    def calculate_moral_scores(self, text_tokens, model):
        try:   
            text_vector = sum([model[word] for word in text_tokens if word in model]) / len(text_tokens)
            moral_scores = {}
            for moral, moral_vector in self.centroids.items():
                moral_scores[moral] = cosine_similarity([text_vector], [moral_vector])[0][0]
        except:
            moral_scores = {}
            for moral, moral_vector in self.centroids.items():
                moral_scores[moral] = None
            
        return moral_scores

