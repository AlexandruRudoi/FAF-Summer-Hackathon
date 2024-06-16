from llama_index.llms.groq import Groq
import requests
import json
import re
from flask import Flask, request, jsonify

# Function to get data from a URL
def getData(url_req):
    response = requests.get(
        url='https://app.scrapingbee.com/api/v1/',
        params={
            'api_key': '8KGX7HWF6F7K7V74S99RYJW22Z8EIE8GU68SNBTIGMD9P51PSGAWWYI79VTMHZZNGVW8Q9LS6BKXB6N6',
            'url': url_req,
        },
        
    )
    car_structure = {
        "manufacturer_name", "model_name", "transmission", "color", "odometer_value", "year_produced", "engine_fuel", "engine_has_gas", "engine_type", "engine_capacity", "body_type", "has_warranty", "state", "price_usd"
    }
    
    task = f"Get me the details using the following structure: {car_structure}, from the following: {url_req}. If you didn't find the details, please find it by yourself and fill it and don't add any other comment also if it is need to make any conversion do it."
    llm = Groq(model="mixtral-8x7b-32768", api_key="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")
    response = llm.complete(task)
    return response


# Function to calculate the fitness score of a car based on its attributes
def calculate_max_price(car):
    current_year = 2024
    try:
        age_score = (20 - current_year - int(car["year_produced"])) / 20
        odometer_value = int(car["odometer_value"])
        engine_capacity = float(car["engine_capacity"])
        price = float(car["price_usd"])
    except:
        return 0
    # Age score
    if (age_score < 0):
        age_score = 0
    
    # Mileage score
    mileage_score = max(0, 1 - (odometer_value / 300000))
    
    # Engine capacity score
    engine_capacity_score = max(0, min(1, (engine_capacity - 1) / 5.0))
    
    # Compute the total fitness score for maximum price computation
    total_score = (age_score * 0.5) + (mileage_score * 0.3) + (engine_capacity_score * 0.2)
    
    
    return price / total_score


# Function to calculate the fitness score of a car based on its attributes
def calculate_fitness(car, mean_max):
    current_year = 2024
    try:
        age_score = (20 - current_year - int(car["year_produced"])) / 20
        odometer_value = int(car["odometer_value"])
        engine_capacity = float(car["engine_capacity"])
        price = float(car["price_usd"])
    except:
        return [0.0, 0.0]
    # Age score
    if (age_score < 0):
        age_score = 0
    
    # Mileage score
    mileage_score = max(0, 1 - (odometer_value / 300000))
    
    # Engine capacity score
    engine_capacity_score = max(0, min(1, (engine_capacity - 1) / 5.0))
    
    # Compute the total fitness score
    total_score = (age_score * 0.65) + (mileage_score * 0.2) + (engine_capacity_score * 0.15)
    
    # Normalize the score by the price factor
    price_ratio = mean_max / price
    adjusted_score = total_score * price_ratio
    
    return [total_score, adjusted_score]


# Function to process cars from a JSON file and calculate their fitness scores
def process_cars_from_json(json_filepath):
    
    with open(json_filepath, 'r', encoding='utf-8') as file:  # Specify encoding here
        cars = json.load(file)
    scores = []
    mean_max = 0
    # Compute mean max
    for car in cars:
        try:
            # If an error occurs like division by zero, then skip this data
            max_price = calculate_max_price(car)
        except:
            pass
        mean_max += max_price
    mean_max /= len(cars)
    print(mean_max)
    for car in cars:
        score = calculate_fitness(car, mean_max)
        scores.append([car, score])
    
    return (scores, mean_max)


# Function to fix file encoding
def fix_file_encoding(source_filepath, target_filepath, source_encoding='ISO-8859-1'):
    try:
        # Read the file with the suspected source encoding
        with open(source_filepath, 'r', encoding=source_encoding) as file:
            content = file.read()
        
        # Write the content to a new file with utf-8 encoding
        with open(target_filepath, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print("File re-encoded successfully and saved as:", target_filepath)
    except UnicodeDecodeError as e:
        print("Failed to decode the file with", source_encoding, "encoding.")
        print("Error:", e)
    except Exception as e:
        print("An error occurred:", e)


# Car recommandation
def recommend_car(car, car_scores, mean_max):
    current_year = 2024
    # Consider a relative price range +- 20%
    relative_price_range = 0.2
    price = float(car["price_usd"])
    min_price = price * (1 - relative_price_range)
    max_price = price * (1 + relative_price_range)
    
    # Collecting fitness scores of similar but better cars
    similar_better_cars = []
    car_fitness = calculate_fitness(car, mean_max)
    for candidate in car_scores:
        candidate_car = candidate[0]
        candidate_score = candidate[1]
        try:
            # Filtering criteria: similar age, mileage, engine capacity, and within price range
            if abs(int(candidate_car["year_produced"]) - int(car["year_produced"])) <= 2 and \
            abs(float(candidate_car["engine_capacity"]) - float(car["engine_capacity"])) <= 0.5 and \
            abs(int(candidate_car["odometer_value"]) - int(car["odometer_value"])) <= 50000 and \
            min_price <= float(candidate_car["price_usd"]) <= max_price:
                
                # We want to recommend only cars with a better fitness score
                if candidate_score[0] > car_fitness[0]:
                    similar_better_cars.append([candidate_car, candidate_score])
        except:
            pass

    # Sorting the list by fitness score in descending order to recommend the best match first
    similar_better_cars.sort(key=lambda x: x[1], reverse=True)

    # Return the best match or None if no suitable car is found
    return similar_better_cars[0] if similar_better_cars else None

# 
def car_comparative_analysis(url1, url2):
    # Example usage
    source_filepath = 'cars.json'  # Path to the problematic file
    target_filepath = 'cars.json'  # Path where the fixed file will be saved

    # You might need to adjust the source_encoding if you suspect a different encoding
    fix_file_encoding(source_filepath, target_filepath, source_encoding='ISO-8859-1')
    # Function to calculate and print fitness scores for all cars in a JSON file
    json_filepath = 'cars.json'  # Path to the JSON file with car data
    car_scores, mean_max = process_cars_from_json(json_filepath)
    # Sort by fitness score
    print(car_scores[0][1][0])
    car_scores.sort(key=lambda element: element[1][0], reverse=True)  # Sort by the fitness score
    for i in range(len(car_scores)):
        print(f"Manufacturer: {car_scores[i][0]['manufacturer_name']}, Model: {car_scores[i][0]['model_name']}, Fitness Score: {car_scores[i][1]}")


    # Read and get the user inserted car data:
    car_data = {
    'year_produced': 2018,
    'transmission': 'Automatic',
    'model_name': 'Gran Coupé 420d M Paket Facelift',
    'engine_type': 'Diesel',
    'state': 'Used',
    'color': 'Black',
    'engine_capacity': 2.0,
    'has_warranty': True,
    'price_usd': 32635.0,
    'engine_has_gas': False,
    'odometer_value': 3500.0,
    'manufacturer_name': 'BMW',
    'body_type': 'Coupé',
    'engine_fuel': 'Diesel'
    }

    recommended_car = recommend_car(car_data, car_scores, mean_max)
    if recommended_car:
        print(f"Recommended Car: {recommended_car}, Fitness Score: {recommended_car[1]}")
    else:
        print("No suitable recommendation found.") 

# Compare two products and suggest alternatives
def comparative(url1, url2):
    llm = Groq(model="mixtral-8x7b-32768", api_key="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")

    task = f"Compare the following two products: {url1} and {url2}. Provide a simple and clear description suitable for someone with no technical background. Also suggest alternative similar products that might be a better option."
    task2 = f"Show a comparison table with the main features of the two products, but make the products in json format, if there are `not specified fields` search and fill it: {url1} and {url2}."

    response = llm.complete(task)
    response2 = llm.complete(task2)
    response = str(response)
    response2 = str(response2)

    return response, response2

# def main():
#     url1 = 'https://www.mobile.de/ro/Automobil/BMW-Gran-Coup%C3%A9-420d-M-Paket-Facelift/vhc:car,ms1:3500__/pg:vipcar/394150676.html'
#     url2 = 'https://www.mobile.de/ro/Automobil/Peugeot-Peugeot-308/vhc:car/pg:vipcar/395213526.html'
#     # url1 = 'https://www.t-mobile.com/cell-phone/samsung-galaxy-s24'
#     # url2 = 'https://enter.online/telefoane/smartphone-uri/ulefone-note-13p-4-gb-64-gb-dual-sim-black'
#     res1, res2 = comparative(url1, url2)

#     print(res1)
#     print(res2)
    

# if __name__ == "__main__":
#     main()


app = Flask(__name__)

# Example of a GET request: Fetch data or perform action based on URL
# http://127.0.0.1:8080/api/getData?url={"https://www.mobile.de/ro/Automobil/BMW-Gran-Coup%C3%A9-420d-M-Paket-Facelift/vhc:car,ms1:3500__/pg:vipcar/394150676.html"}
@app.route('/api/getData', methods=['GET'])
def api_get_data():
    url_req = request.args.get('url')
    if not url_req:
        return jsonify({'error': 'Missing URL parameter'}), 400
    try:
        data = getData(url_req)
        return jsonify(str(data))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Example of a POST request: Receive data, process it, and return a response
@app.route('/api/comparative', methods=['POST'])
def api_comparative():
    data = request.json
    url1 = data.get('url1')
    url2 = data.get('url2')
    if not url1 or not url2:
        return jsonify({'error': 'Missing URL parameters'}), 400
    try:
        res1, res2 = comparative(url1, url2)
        return jsonify({'response1': res1, 'response2': res2})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=8080, debug=True)

