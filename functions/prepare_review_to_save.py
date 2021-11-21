import requests

"""
    Action function to validate and prepare request params 

    :param dict: Dictionary of request parameters
    :returns: Formatted JSON for review entry to save to DB, or error and error code 
    when form validation fails

"""   
def main(dict):
    validation_results = validate_params(dict)
    
    if not validation_results['code'] == 200:
        return validation_results
        
    return prepare_doc_to_save(dict['review'])
    
    
"""
    Performs server-side form validation of review

    :param dict: Dictionary of request parameters
    :returns: error code and error message when a particular scenario fails, else returns code 200

"""       
def validate_params(dict):
    if 'review' not in dict:
        return {"error": "Input is not formatted correctly", "code": 500}
    elif 'review' not in dict['review']:
        return format_error('review')
    elif 'purchase' not in dict['review']:
        return format_error('purchase field')
    elif dict['review']['purchase']:
        if 'purchase_date' not in dict['review']: 
            return format_error('purchase date')
        elif 'car_make' not in dict['review']: 
            return format_error('car make')
        elif 'car_model' not in dict['review']:
            return format_error('car model')
        elif 'car_year' not in dict['review']:
            return format_error('car year')
            
    return {"code": 200}
    
"""
    Wrapper function for formatting error messages wheen validate_params(dict) fails

    :param field: String representing field that is blank
    :returns: Formatted JSON containing error message and status code 500

"""      
def format_error(field):
    return {"error": field + " is blank", "code": 500}
    
"""
    Formats review entry to save 

    :param review: Dictionary representing Review JSON object
    :returns: Formatted JSON for review entry to save to DB

"""       
def prepare_doc_to_save(review):
    return {
        'doc': {
            'id':review['id'],
            'name': review['name'],
            'dealership': review['dealership'],
            'review': review['review'],
            'purchase': review['purchase'],
            'purchase_date': review['purchase_date'],
            'car_make': review['car_make'],
            'car_model': review['car_model'],
            'car_year': review['car_year'],
        }
    }