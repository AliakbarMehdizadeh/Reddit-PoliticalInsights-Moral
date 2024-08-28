from credentials import CLIENT_ID, CLIENT_SECRET
from config import TOP_POSTS_TIME_FILTER, MAXIMUM_POSTS_PER_SUBREDDIT, SUBREDDIT_NAMES_LIST
from data_gatherer import DataGatherer
from analyzer import MoralScoreAnalyzer
from preprocessing import Preprocessing
from moral_dictionary import MoralCentroid

if __name__ == "__main__":
    # Initialize DataGatherer and Preprocessing classes
    data_gatherer = DataGatherer(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        subreddit_names_list=SUBREDDIT_NAMES_LIST,
        top_posts_time_filter=TOP_POSTS_TIME_FILTER,
        maximum_posts_per_subreddit=MAXIMUM_POSTS_PER_SUBREDDIT
    )
    
    comments_list_by_post = data_gatherer.get_comments_list_by_post(subreddit_name="all")
    
    cleaned_comments_list_by_post = {}
    moral_scores = {}
    
    preprocessor = Preprocessing()
    moral_centroids = MoralCentroids(moral_dict, word2vec_model)
    
    for post_id in comments_list_by_post:
        # Preprocess comments for the current post
        cleaned_comments_list_by_post[post_id] = preprocessor.preprocess_list_of_comments(comments_list_by_post[post_id])
        moral_scores_by_post = []
        
        for i, comment_tokens in enumerate(cleaned_comments_list_by_post[post_id]):
            
            score = moral_centroids.calculate_moral_scores(comment_tokens, word2vec_model)
            
            moral_scores_by_post.append(score)
        
        moral_scores[post_id] = moral_scores_by_post
    
    analyzer = MoralScoreAnalyzer(moral_dict)
    analyzer.collect_scores(moral_scores)
    analyzer.calculate_statistics()
    analyzer.plot_violin_plot()
    analyzer.plot_radar_chart()

    # Print out average values for each dimension
    print("Average values for each moral dimension:")
    for dimension, avg_value in analyzer.average_scores.items():
        print(f"{dimension}: {avg_value:.4f}")
