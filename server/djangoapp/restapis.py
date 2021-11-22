import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)

    except:
        # If any error occurs
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data    

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf():
    url = "https://fcfec9e2.us-south.apigw.appdomain.cloud/api/dealership"
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result['docs']
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results

def get_dealer_by_id_from_cf(dealerId):
    url = "https://fcfec9e2.us-south.apigw.appdomain.cloud/api/dealership"
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId = dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result['docs']
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    
    return results[0] if (len(results)>0) else results

def get_dealer_by_state_from_cf(state):
    url = "https://fcfec9e2.us-south.apigw.appdomain.cloud/api/dealership"
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, state = state)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result['docs']
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_reviews_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(dealerId):
    url = "https://fcfec9e2.us-south.apigw.appdomain.cloud/api/review"
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId = dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result['reviews']
        # For each dealer object
        for review in reviews:
            # Get its content in `reviews` object
            # Create a DealerReview object with values in `reviews` object
            dealer_review_obj = DealerReview(id=id, dealership=review['dealership'], name=review['name'], 
                                        purchase=review['purchase'], review=review['review'], 
                                        purchase_date=review['purchase_date'], car_make=review['car_make'], 
                                        car_model=review['car_model'], car_year=review['car_year'])                           
            results.append(dealer_review_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



