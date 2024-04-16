import pandas as pd
from sklearn.cluster import DBSCAN
import folium
from matplotlib import pyplot as plt
from matplotlib.colors import to_hex
import re
from collections import Counter

data = pd.read_csv("yelp_gmaps_leftover_atleast_one_type.xlsx - Sheet1.csv")
coordinates = data[['gmaps_latitude', 'gmaps_longitude']]

"""dropping city and zip bc of borderlines (could be in the middle
of meaningful cluster)"""

data = data.drop(columns=['yelp_id', 'gmaps_id', 'gmaps_city','gmaps_zipcode', 'yelp_rating',
                    'yelp_rating_count', 'gmaps_rating', 'gmaps_rating_count',
                    'has at least one type (yelp/google)'])


"""
#Finding types for condensing data
unique = set()
for types in data['yelp_types']:
    if isinstance(types, str):
        unique.update(types.split(', '))
ptypes = sorted(list(unique))
print(ptypes)

file = 'yelptypes.txt'

item_counts = Counter(data['yelp_types'])
new = item_counts.most_common()[0:25]
print(new)
with open(file, 'w') as file:
    for item in new:
        file.write("%s\n" % item[0])
"""
"""
Results:
['art_gallery', 'atm', 'bakery', 'bank', 'bar', 'beauty_salon', 
'book_store', 'bowling_alley', 'cafe', 'car_rental', 'car_repair', 
'casino', 'clothing_store', 'convenience_store', 'department_store', 
'drugstore', 'electronics_store', 'finance', 'florist', 'food', 
'furniture_store', 'gas_station', 'general_contractor', 
'grocery_or_supermarket', 'gym', 'hair_care', 'hardware_store', 
'health', 'home_goods_store', 'jewelry_store', 'library', 'liquor_store', 
'local_government_office', 'locksmith', 'lodging', 'meal_delivery', 
'meal_takeaway', 'movie_theater', 'museum', 'night_club', 'park', 
'parking', 'pet_store', 'pharmacy', 'real_estate_agency', 'restaurant', 
'school', 'shoe_store', 'shopping_mall', 'spa', 'supermarket', 
'tourist_attraction', 'university']

Yelp results found in yelptypes.txt
"""

#sorted by relevance
food_types = ["restaurant",  "bar", "bakery", "cafe", "dessert"]
lifestyle_types = ["artgallery", "bowlingalley", "departmentstore", 
                   "movietheater", "museum", "nightclub", 
                    "spa", "beautysalon", "bookstore", 
                   "florist", "library", "park", "nightlife", "movietheater", "shoppingmall", "food", "clothingstore"]
specialized_food_types = ["restaurant", "bubbletea", "fastfood", "sandwiches",
                          "pizza", "sushi", "bars", "restaurants"]
specialized_lifestyle_types = ["axe_throwing", "yoga", "specialty food"]


def normalize_gmaps_types(types):
    if isinstance(types, str):
        # Remove non-alphanumeric characters
        normalized_types = re.sub(r'[^a-zA-Z0-9, ]+', '', types)
        # Convert to lowercase
        normalized_types = normalized_types.lower()
        # Strip leading and trailing spaces
        normalized_types = normalized_types.strip()
        # Replace remaining spaces with underscores
        return normalized_types
    else:
        return types
def gmapDescriptors(gtypes, ytypes):
    # Find a relevant single descriptor based on gmaps descriptions, 
    # if none exists, it sends the data to the yelp descriptors
    if isinstance(gtypes, str):
        type_collection = set(gtypes.split(', '))
        food_intersect = type_collection.intersection(food_types)
        lifestyle_intersect = type_collection.intersection(lifestyle_types)
        if lifestyle_intersect:
            return next(iter(lifestyle_intersect))
        elif food_intersect:
            return next(iter(food_intersect))
        else:
            if isinstance(ytypes, str):
                ytype_collection = set(ytypes.split(', '))
                yelp_intersect = ytype_collection.intersection(specialized_food_types)
                if yelp_intersect:
                    return next(iter(yelp_intersect))
                else:
                    return "other"
            else:
                return "other"
    else:
        if isinstance(ytypes, str):
            ytype_collection = set(ytypes.split(', '))
            yelp_intersect = ytype_collection.intersection(specialized_food_types)
            if yelp_intersect:
                return next(iter(yelp_intersect))
            else:
                return "other"
        else:
            return "other"
    
data['gmaps_types'] = data['gmaps_types'].apply(normalize_gmaps_types)
data['yelp_types'] = data['yelp_types'].apply(normalize_gmaps_types)
data['type'] = data.apply(lambda row: gmapDescriptors(row['gmaps_types'], row['yelp_types']), axis=1)

def unify(types):
    if isinstance(types, str):
        type_list = types.split(', ')
        if "restaurants" in type_list:
            type_list = ['restaurant' if t == 'restaurants' else t for t in type_list]
        if "bars" in type_list:
            type_list = ['bar' if t == 'bars' else t for t in type_list]
        unified_types = ', '.join(type_list)
        
        return unified_types
    else:
        return types
data['type'] = data['type'].apply(unify)
data = data[data['type'] != "other"]

data.to_csv("clean_data.csv")

#clustering test: 
"""dbscan = DBSCAN(eps=0.1, min_samples=10)
data['cluster'] = dbscan.fit_predict(coordinates)

data['composite_score'] = data['composite_score'].astype(float)
data = data[data['cluster'] != -1] #noise
clScores = data.groupby('cluster')['composite_score'].mean() #avg score for that area

center = [33.755711, -84.388372]
atl = folium.Map(location= center, zoom_start=12)

nClusters = len(clScores)
colors = plt.get_cmap('plasma', nClusters)

for idx, row in data.iterrows():
    if row['cluster'] != -1:
        cluster_color = colors(row['cluster'] % nClusters)
        folium.CircleMarker(
            location=[row['gmaps_latitude'], row['gmaps_longitude']],
            radius=5,
            popup=f"Cluster: {row['cluster']}, average score: {row['composite_score']:.2f}",
            color=to_hex(cluster_color[:3]),
            fill=True,
            fill_color=to_hex(cluster_color[:3])
        ).add_to(atl)

atl.save("atl.html")"""
