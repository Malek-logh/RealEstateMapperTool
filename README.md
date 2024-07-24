```markdown
# Real Estate Data Processing and Visualization

This project involves scraping real estate data, cleaning and inserting it into a PostgreSQL database, and performing clustering analysis with visualization on a map. The main components of the project are:

1. **Data Scraping and Cleaning**
2. **Database Setup and Data Insertion**
3. **Clustering Analysis and Visualization**

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Scripts Overview](#scripts-overview)
- [Docker Setup](#docker-setup)

## Installation

To get started with this project, follow these steps:

### Prerequisites

- Python 3.7+
- Docker
- Docker Compose

### Clone the Repository

```bash
git clone https://github.com/Malek-logh/RealEstateMapperTool.git
RealEstateMapperTool
```

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Create `requirements.txt`

```text
pandas
beautifulsoup4
selenium
sqlalchemy
psycopg2
scikit-learn
folium
```

## Usage

### Step 1: Scrape Data

Run the scraping scripts to collect data from real estate websites. Make sure you have the necessary drivers for Selenium (e.g., ChromeDriver).

```bash
python scrapingTerrain.py
python scrapingMaison.py
python scrapingAppartement.py
```

### Step 2: Insert Data into PostgreSQL

Start the PostgreSQL database using Docker Compose and insert the scraped data.

```bash
docker-compose up -d
python insertdata.py
```

### Step 3: Perform Clustering and Visualization

Run the clustering analysis and generate the map with clustered data points.

```bash
python clustering.py
```

## Project Structure

```
real-estate-data/
├── scrapingTerrain.py
├── scrapingMaison.py
├── scrapingAppartement.py
├── MubawabTerrain.csv
├── MubawabMaison.csv
├── MubawabAppartement.csv
├── insertdata.py
├── clustering.py
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Scripts Overview

### `scrapingTerrain.py`, `scrapingMaison.py`, `scrapingAppartement.py`

These scripts scrape data from https://www.mubawab.tn/ and save it into CSV files. They use `BeautifulSoup` for parsing HTML and `selenium` for web interactions.

### `insertdata.py`

This script reads the data from the CSV files, cleans it, and inserts it into a PostgreSQL database. It uses `pandas` for data manipulation and `sqlalchemy` for database interactions.

### `clustering.py`

This script performs clustering analysis on the real estate data and visualizes the results on Tunisa map using `folium`. It uses `scikit-learn` for clustering and `folium` for map visualization.

### `docker-compose.yml`

This file sets up the PostgreSQL database and pgAdmin using Docker Compose.

## Docker Setup

Use Docker Compose to set up and run the PostgreSQL database and pgAdmin.

```bash
docker-compose up -d
```

- Access pgAdmin at `http://localhost:8081`
- PostgreSQL will be running on port `5432`

## Contributing

Feel free to fork this project, make your changes, and submit a pull request. Any contributions are highly appreciated!

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
```

This documentation provides a comprehensive guide to setting up, running, and understanding the project. Make sure to replace the placeholder `https://github.com/yourusername/real-estate-data.git` with the actual URL of your GitHub repository.
