import requests
from bs4 import BeautifulSoup

def fetch_images(url):
    # Send a GET request to the webpage
    response = requests.get(url)
    # Raise an error for bad requests
    response.raise_for_status()

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all <img> tags
    images = soup.find_all('img')

    # Extract the source URLs for the images
    image_urls = [img['src'] for img in images if 'src' in img.attrs]

    return image_urls
string_request = 'BMW 420 Gran Coupé M Paket LCi Facelift*Head-Up*1 Ha'
url = 'https://www.google.com/search?q=' + string_request + '&sca_esv=1a90f3acf3a57e4e&sxsrf=ADLYWIIAd03qzWG33VhqkU2QkZ5bxtriKQ:1718517096517&source=hp&biw=1536&bih=730&ei=aH1uZpeoHZ_ixc8PyoGsgAk&iflsig=AL9hbdgAAAAAZm6LeNmpqIvsUmD3LWgZyONUuGwDiGcy&oq=&gs_lp=EgNpbWciACoCCAAyBxAjGCcY6gIyBxAjGCcY6gIyBxAjGCcY6gJI-wpQAFgAcAF4AJABAJgBAKABAKoBALgBAcgBAIoCC2d3cy13aXotaW1nmAIBoAIKqAIDmAMKkgcBMaAHAA&sclient=img&udm=2'  # Replace with your target URL
images = fetch_images(url)

print(images[1])