import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt

data = pd.read_csv("clean_data.csv")
"""
Heatmap: 
plt.figure(figsize=(10, 8))
sns.heatmap(data.pivot_table(index=pd.cut(data['gmaps_latitude'], 25),
                             columns=pd.cut(data['gmaps_longitude'], 25),
                             values='composite_score', aggfunc='mean'),
            cmap='plasma', annot=True, fmt=".2f", cbar_kws={'label': 'Average Composite Score'})

plt.title('Heatmap of Average Composite Scores')
plt.xlabel('Longitude Bins')
plt.ylabel('Latitude Bins')
plt.show()
"""

average_scores_by_type = data.groupby('gmaps_type')['composite_score'].mean().sort_values(ascending=False)

# Create a bar chart
plt.figure(figsize=(10, 6))
average_scores_by_type.plot(kind='bar', color='skyblue')

# Set the title and labels
plt.title('Average Composite Scores by Establishment Type')
plt.xlabel('Establishment Type')
plt.ylabel('Average Composite Score')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability

# Show the plot
plt.tight_layout()
plt.show()
