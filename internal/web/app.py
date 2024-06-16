from flask import Flask, render_template, request, jsonify
from llama_index.llms.groq import Groq
import requests
import nltk
from nltk.tokenize import sent_tokenize
from bs4 import BeautifulSoup
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/comparative', methods=['POST'])
def api_comparative():
    data = request.get_json()
    url1 = data.get('url1')
    url2 = data.get('url2')
    if not url1 or not url2:
        return jsonify({'error': 'Missing URL parameters'}), 400

    try:
        post_data = {'url1': url1, 'url2': url2}
        # Ensure you are making the request to the correct port and address
        response = requests.post('http://localhost:8080/api/comparative', json=post_data)

        if response.status_code == 200:
            # Extract data from response
            res1 = response.json().get('response1')
            res2 = response.json().get('response2')

            nltk.download('punkt')
            sentences = sent_tokenize(res1)
            # sentences2 = sent_tokenize(res2)

             # Remove the first and last sentence, adjusting punctuation
            if len(sentences) > 2:
                # Prepare sentences by stripping trailing punctuation and re-adding it uniformly
                sentences = [s.strip('.!?') for s in sentences[1:-1]]
                res1 = ". ".join(sentences) + "." if sentences else ""
            else:
                res1 = ""
            
            start = res2.find('{') + 1  # Add 1 to start after the '{'
            end = res2.rfind('}')
            # Extract the text between
            if start > 0 and end > 0 and end > start:
                res2 = res2[start:end]
                res2 = "{" + res2 + "}"
            else:
                res2 = "No valid brackets found"

            return jsonify({'1': res1, '2':res2})  # Directly pass on the JSON response
        else:
            return jsonify({'error': 'API request failed', 'status_code': response.status_code}), 502

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/auto-submit', methods=['POST'])
def auto_submit():
    data = request.get_json()
    link = data.get('link', 'No link provided')
    task = f"Give me the name of the product on the link without any comments: {link}"
    llm = Groq(model="mixtral-8x7b-32768", api_key="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")
    response = llm.complete(task)
    string_request = str(response)
    url = 'https://www.google.com/search?q=' + string_request + '&sca_esv=1a90f3acf3a57e4e&sxsrf=ADLYWIIAd03qzWG33VhqkU2QkZ5bxtriKQ:1718517096517&source=hp&biw=1536&bih=730&ei=aH1uZpeoHZ_ixc8PyoGsgAk&iflsig=AL9hbdgAAAAAZm6LeNmpqIvsUmD3LWgZyONUuGwDiGcy&oq=&gs_lp=EgNpbWciACoCCAAyBxAjGCcY6gIyBxAjGCcY6gIyBxAjGCcY6gJI-wpQAFgAcAF4AJABAJgBAKABAKoBALgBAcgBAIoCC2d3cy13aXotaW1nmAIBoAIKqAIDmAMKkgcBMaAHAA&sclient=img&udm=2'  # Replace with your target URL
    images = fetch_images(url)

    if images:
        # Convert image to base64
        # image_bytes = BytesIO(images[1])
        # encoded_string = base64.b64encode(image_bytes.getvalue()).decode('utf-8')
        # base64_image = f"data:image/jpeg;base64,{encoded_string}"
        return jsonify({'image': images[1], 'message': 'Images fetched successfully'})
    else:
        return jsonify({'error': 'No images found'}), 404


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


if __name__ == '__main__':
    app.run(port=5000, debug=True)
