import praw
from typing import List, Dict

class DataGatherer:

    def __init__(self, client_id: str, client_secret: str, subreddit_names_list: List[str], maximum_posts_per_subreddit: int, 
top_posts_time_filter: str):
        self.subreddit_names_list = subreddit_names_list
        self.maximum_posts_per_subreddit = maximum_posts_per_subreddit
        self.top_posts_time_filter = top_posts_time_filter
        self.reddit_client = praw.Reddit(client_id=client_id,
                                         client_secret=client_secret,
                                         user_agent="user_agent")
        self.comments_list_by_post = {}

    def get_comments_list_by_post(self, subreddit_name: str):
        retrieved_posts_count = 0

        for subreddit_name in self.subreddit_names_list:
            subreddit = self.reddit_client.subreddit(subreddit_name)
            top_posts = subreddit.top(time_filter=self.top_posts_time_filter)

            current_subreddit_retrieved_posts_count = 0

            for post in top_posts:
                post_id = post.id
                self.comments_list_by_post[post_id] = []

                post.comments.replace_more(limit=0)

                for comment in post.comments.list():
                    comment_author = comment.author
                    if comment_author and comment_author.name != "AutoModerator":
                        self.comments_list_by_post[post_id].append(comment.body)
                
                retrieved_posts_count += 1
                current_subreddit_retrieved_posts_count += 1
                print(f"Retrieved posts from r/{subreddit_name}: {retrieved_posts_count}")
                
                if current_subreddit_retrieved_posts_count == self.maximum_posts_per_subreddit:
                    break

        return self.comments_list_by_post
