import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

# for local environment secrets
import os
from dotenv import load_dotenv 
load_dotenv()

def get_request(url, **kwargs):
    print('get_request kwargs: ' + str(kwargs))
    print("GET from {} ".format(url))

    try:
        if 'api_key' in kwargs:
           response = requests.get(url, headers={'Content-Type': 'application/json'},
                                        auth=HTTPBasicAuth('apikey', kwargs['api_key']), params=kwargs)
 
        else:
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
    url = os.environ['BASE_CLOUD_FUNCTIONS_URL']+"/dealership"
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,IAM_API_KEY=os.environ['IAM_API_KEY'])
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
    url = os.environ['BASE_CLOUD_FUNCTIONS_URL']+"/dealership"
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId = dealerId,IAM_API_KEY=os.environ['IAM_API_KEY'])
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
    url = os.environ['BASE_CLOUD_FUNCTIONS_URL']+"/dealership"
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, state = state,IAM_API_KEY=os.environ['IAM_API_KEY'])
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
    url = os.environ['BASE_CLOUD_FUNCTIONS_URL']+"/review"
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId = dealerId, IAM_API_KEY=os.environ['IAM_API_KEY'])
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
                                        

            dealer_review_obj.sentiment = analyze_review_sentiments(dealer_review_obj.review)
            print ('Text: '+ dealer_review_obj.review +'|Sentiment: ' + dealer_review_obj.sentiment)
            results.append(dealer_review_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview):
    url = os.environ['NLU_URL']

    json_result = get_request(url, text=dealerreview,version='2020-08-01',features='sentiment',
        api_key=os.environ['NLU_API_KEY'],return_analyzed_text=True)

    if 'sentiment' in json_result:
        sentiment = json_result['sentiment']['document']['label']
        return sentiment 

    return DealerReview.NEUTRAL

