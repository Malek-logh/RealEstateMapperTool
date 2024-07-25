import pandas as pd
from sqlalchemy import create_engine
from sklearn.cluster import KMeans
import numpy as np
import folium
from folium.plugins import MarkerCluster

# Database credentials
db_host = 'localhost'
db_name = 'postgres'
db_user = 'replace_with_your_username'
db_pass = 'replace_with_your_password'
db_port = '5432'

# Create the connection string
db_url = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'

# Create SQLAlchemy engine
engine = create_engine(db_url)

# Load data from database tables into DataFrames
appartement_df = pd.read_sql('SELECT * FROM appartement', engine)
maison_df = pd.read_sql('SELECT * FROM maison', engine)
terrain_df = pd.read_sql('SELECT * FROM terrain', engine)

# Combine data into one DataFrame
combined_df = pd.concat([appartement_df, maison_df, terrain_df], ignore_index=True)


# Select relevant features for clustering
features = combined_df[['price(TND)', 'area(m²)']].dropna()

# Perform KMeans clustering
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(features)

# Add cluster labels to the original DataFrame
combined_df['cluster'] = np.nan
combined_df.loc[features.index, 'cluster'] = clusters

# Remove rows with NaN values in latitude or longitude
cleaned_df = combined_df.dropna(subset=['latitude', 'longitude'])

# Create a base map
m = folium.Map(location=[34.0, 9.0], zoom_start=7)

# Define a color map for clusters
colors = ['red', 'blue', 'green']

# Create a marker cluster
marker_cluster = MarkerCluster().add_to(m)

# Add markers to the map
for idx, row in cleaned_df.iterrows():
    if not pd.isna(row['cluster']):
        popup_text = f"""
        Type: {row['property']} <br>
        Prix: {row['price(TND)']} TND<br>
        Surface: {row['area(m²)']} m²<br>
        <a href="{row['link']}" target="_blank">Property Link</a>
        """
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=popup_text,
            icon=folium.Icon(color=colors[int(row['cluster'])])
        ).add_to(marker_cluster)

# Save the map to an HTML file
m.save('real_estate_clusters.html')

print("Map has been saved as real_estate_clusters.html")
