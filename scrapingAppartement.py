import re
import csv
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver

# Setting up Chrome options for the Selenium WebDriver
options = webdriver.ChromeOptions()
# Uncomment the next line to run Chrome in headless mode (without opening a window)
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

# Function to scrape data from a given URL
def scrape_page(url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extracting the longitude from the page, if available
    try:
        longitude = soup.find('div', class_='blockProp mapBlockProp').find('div', class_='prop-map-holder')['lon']
    except (AttributeError, KeyError):
        longitude = ''

    # Extracting the latitude from the page, if available
    try:
        latitude = soup.find('div', class_='blockProp mapBlockProp').find('div', class_='prop-map-holder')['lat']
    except (AttributeError, KeyError):
        latitude = ''

    # Extracting the title of the property
    try:
        title = soup.find('div', class_='blockProp').h1.text.strip()
    except AttributeError:
        title = ''

    # Extracting the city information
    try:
        city = soup.find('div', class_='mainInfoProp').find('h3', class_='greyTit').text.replace('\n', '').replace('\t', ' ')
    except AttributeError:
        city = ''

    # Extracting the price, handling special cases
    try:
        price_h3 = soup.find('div', class_='mainInfoProp').find('h3', class_='orangeTit')
        if price_h3:
            price_h3_text = price_h3.text.replace('\n', '').replace('\t', '').strip()
            if price_h3_text == "Prix à consulter" or "Baisse du prix" in price_h3_text:
                price = None  # If the price is not available or if there's a price drop indication, set it to None
            else:
                # Extracting numerical value of the price, removing spaces
                match = re.search(r'(\d[\d\s]*)\s*TND', price_h3_text)
                if match:
                    price = match.group(1).replace(' ', '')
                else:
                    price = None
        else:
            price = None
    except AttributeError:
        price = ''

    # Extracting the area information
    try:
        area_span = soup.find('span', string=lambda x: x and 'm²' in x)
        area = area_span.text.strip().replace('m²', '').strip() if area_span else ''
    except AttributeError:
        area = ''

    # Extracting the number of rooms
    try:
        rooms_span = soup.find('span', string=lambda x: x and 'Chambres' in x)
        rooms = rooms_span.text.strip().replace('Chambres', '').strip() if rooms_span else ''
    except AttributeError:
        rooms = ''

    # Extracting the property type
    try:
        property = soup.find('p', class_='adMainFeatureContentValue').text
    except AttributeError:
        property = ''

    # Returning the extracted information as a tuple
    results = (title, city, property, area, rooms, price, longitude, latitude, url)
    return results

# Function to generate the URL for a specific page number
def get_url(NbPage):
    template = 'https://www.mubawab.tn/fr/sc/appartements-a-vendre:p:{}'
    url = template.format(NbPage)
    return url

# Function to get links to individual property listings from a search results page
def get_links(url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # Extracting the 'linkref' attribute from each listing item
    links = [item.get('linkref') for item in soup.find_all('li', class_='listingBox w100')]
    return links

# Main function to control the scraping process
def main(Nbpage):
    links = []
    data = []

    # Looping through the specified number of pages
    for i in range(1, Nbpage + 1):
        page_url = get_url(i)
        page_links = get_links(page_url)
        for link in page_links:
            data.append(scrape_page(link))

    driver.quit()  # Closing the Selenium WebDriver

    # Creating a DataFrame to store the scraped data
    df = pd.DataFrame(data, columns=['title', 'city', 'property', 'area(m²)', 'rooms', 'price(TND)', 'longitude', 'latitude', 'link'])

    # Clean 'area(m²)' column to keep only numerical values
    df['area(m²)'] = df['area(m²)'].apply(lambda x: re.findall(r'\d+', x)[-1] if re.findall(r'\d+', x) else '')

    # Dropping rows where 'price(TND)' is None or empty
    df = df.dropna(subset=['price(TND)'])
    df = df[df['price(TND)'] != '']

    # Dropping rows where 'rooms' is None or empty
    df = df.dropna(subset=['rooms'])
    df = df[df['rooms'] != '']

    # Inserting an 'id' column with incremental numbers
    df.insert(0, 'id', range(1, len(df) + 1))


    # Saving the cleaned DataFrame to a CSV file
    df.to_csv('MubawabAppartement.csv', index=False)

# Running the main function with 140 pages to scrape
main(140)
