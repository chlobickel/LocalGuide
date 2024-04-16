import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt
from wordcloud import WordCloud

data = pd.read_csv("yelp_gmaps_leftover_atleast_one_type.xlsx - Sheet1.csv")
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
data2 = data.dropna(subset=['yelp_types', 'gmaps_types'], inplace=True)
uniqueTypes = set()
for index, row in data.iterrows():
    for column in ['yelp_types', 'gmaps_types']:
        if isinstance(row[column], str):
            uniqueTypes.update(row[column].split(', '))

txt = ' '.join(uniqueTypes)
wordcloud = WordCloud(width=800, height=400, 
                      colormap = 'winter', background_color='white').generate(txt)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()