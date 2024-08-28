import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

class MoralScoreAnalyzer:
    def __init__(self, moral_dict):
        self.moral_dict = moral_dict
        self.scores = {key: [] for key in moral_dict.keys()}
        self.df_scores = None
        self.average_scores = None
        self.std_dev_scores = None
        self.activation_threshold = 0.0

    def collect_scores(self, moral_scores):
        for post_id, comments_score in moral_scores.items():
            for comment_score in comments_score:
                for dim in comment_score:
                    try: 
                        self.scores[dim].append(comment_score[dim])
                    except KeyError:
                        print(f"Dimension not found: {dim}")
                        print(comment_score)
                        print(comments_score)

    def calculate_statistics(self):
        self.df_scores = pd.DataFrame(self.scores)
        self.df_scores.dropna()
        self.df_scores = self.df_scores[(self.df_scores >= self.activation_threshold).all(axis=1)]
        self.average_scores = self.df_scores.mean()
        self.std_dev_scores = self.df_scores.std()


    def plot_violin_plot(self):
        sns.set_style('darkgrid')
        # Convert DataFrame from wide to long format for Seaborn
        df_long = self.df_scores.melt(var_name='Dimension', value_name='Score')

        plt.figure(figsize=(14, 7))
        sns.violinplot(x='Dimension', y='Score', data=df_long, palette='Set2', inner='quartile')

        # Set the y-axis limit to ensure the minimum is zero
        plt.ylim(bottom=0)

        # Save the figure
        if not os.path.exists('result'):
            os.makedirs('result')
        plt.savefig('result/violin.png')
        plt.show()
        plt.close()

    def plot_radar_chart(self):
        def plot_radar(data, std_dev, labels, title):
            num_vars = len(labels)
            angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
            data += data[:1]
            std_dev += std_dev[:1]
            angles += angles[:1]

            fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
            ax.fill(angles, data, color='red', alpha=0.25, label='Average Score')
            ax.plot(angles, data, color='red', linewidth=2)

            # Add shaded area for standard deviation
            ax.fill_between(angles, [d - sd for d, sd in zip(data, std_dev)], [d + sd for d, sd in zip(data, std_dev)], color='red', 
alpha=0.1, label='Standard Deviation')

            ax.set_yticklabels([])
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(labels, rotation=45)

            plt.title(title, size=15, color='red', y=1.1)
            plt.legend(loc='upper right', bbox_to_anchor=(0.5, -0.05), ncol=2, frameon=False)
            plt.tight_layout(rect=[0, 0, 1, 0.95])

            # Save the figure
            if not os.path.exists('result'):
                os.makedirs('result')
            plt.savefig('result/radar_chart.png')
            plt.show()
            plt.close()

        labels = self.average_scores.index
        data = self.average_scores.tolist()
        std_dev = self.std_dev_scores.tolist()
        plot_radar(data, std_dev, labels, 'Average Moral Scores For Reddit Comments')
