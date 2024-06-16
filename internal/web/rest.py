import requests

def fetch_image(query):
    access_key = 'Fs-lBU_aSvMzN0cwWcpHWu3Y7w_a3W6fCIQaPf2jvoE'  # Replace 'YOUR_ACCESS_KEY' with your Unsplash access key
    url = 'https://api.unsplash.com/search/photos'
    headers = {
        'Authorization': f'Client-ID {access_key}'
    }
    params = {
        'query': query,
        'page': 1,
        'per_page': 1
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        results = response.json()['results']
        if results:
            # Return the URL of the first image in the results
            return results[0]['urls']['regular']
        else:
            return 'No images found.'
    else:
        return f'Failed to fetch images: {response.status_code}'

# Example usage
print(fetch_image('real-life car BMW 420 Gran Coupé M Paket LCi'))
