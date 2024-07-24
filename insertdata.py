import pandas as pd
from sqlalchemy import create_engine

# Load CSV files
appartement_df = pd.read_csv('MubawabAppartement.csv')
maison_df = pd.read_csv('MubawabMaison.csv')
terrain_df = pd.read_csv('MubawabTerrain.csv')

# Clean price columns
def clean_price(price):
    return int(price.replace('\u00a0', '').replace(' ', ''))

for df in [appartement_df, maison_df, terrain_df]:
    df['price(TND)'] = df['price(TND)'].apply(clean_price)

# Database credentials
db_host = 'localhost'
db_name = 'postgres'
db_user = 'malek'
db_pass = 'mallouka80*'
db_port = '5432'

# Create the connection string
db_url = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'

# Create SQLAlchemy engine
engine = create_engine(db_url)

# Define table names
table_names = {
    'appartement': appartement_df,
    'maison': maison_df,
    'terrain': terrain_df
}

# Create tables and insert data
for table_name, df in table_names.items():
    df.to_sql(table_name, engine, if_exists='replace', index=False)

print("Data has been successfully inserted into the PostgreSQL database.")
