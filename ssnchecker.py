import csv
import os
import logging
import requests
from datetime import datetime

# Setup logging configuration
log_file_path = os.path.join(os.getcwd(), 'data_processing.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='w')

def get_new_session_and_csrf(retries=3):
    """Fetches new session ID and CSRF token from a defined URL with retries."""
    url = 'https://studentaid.gov/app/keepSessionAlive.action'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=UTF-8',
        'Referer': 'https://studentaid.gov/fsa-id/create-account/launch',
        'User-Agent': 'Mozilla/5.0'
    }
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                session_id = response.cookies.get('SESSION', None)
                csrf_token = response.cookies.get('XSRF-TOKEN', None)
                return session_id, csrf_token
            else:
                logging.error(f"Failed to fetch session and CSRF token: {response.status_code} {response.text}")
        except requests.RequestException as e:
            logging.error(f"Network error during session fetch: {e}")
    return None, None

def create_request_headers(session_id, csrf_token, route_id):
    """Creates headers and cookies for API requests."""
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.62 Safari/537.36',
        'X-XSRF-TOKEN': csrf_token,
        'Referer': 'https://studentaid.gov/fsa-id/create-account/confirm-verify',
        'Origin': 'https://studentaid.gov',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Ch-Ua': '"Not;A=Brand";v="99", "Chromium";v="106"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'X-Dtreferer': 'https://studentaid.gov/fsa-id/create-account/challenge-questions',
        'X-Dtpc': '5$117047117_413h31vKNHHRKOAUHFDRKSOKKGGQPDRMRFHEVDD-0e0'
    }
    cookies = {
        'SESSION': session_id,
        'XSRF-TOKEN': csrf_token,
        'ROUTEID': route_id
    }
    return headers, cookies

def post_check_user_data(headers, cookies, user_data):
    """Submits the user data via POST request to the checkUserData API endpoint."""
    url = 'https://studentaid.gov/app/api/auth/registration/checkUserData'
    response = requests.post(url, headers=headers, cookies=cookies, json=user_data)
    return response.json()

def format_date(dob):
    """Formats date to YYYY-MM-DD if it is not already in that format."""
    try:
        date_obj = datetime.strptime(dob, '%Y-%m-%d')
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        logging.warning(f"Date format error for: {dob}")
        return None

def generate_hypothetical_email(first_name, last_name, ssn):
    """Generates a hypothetical email based on first name, last name, and SSN."""
    return f"{first_name}{last_name}{ssn}@gmail.com"

def generate_hypothetical_username(first_name, last_name, city, ssn):
    """Generates a hypothetical username based on first name, last name, city, and SSN."""
    return f"{first_name}{last_name}{city}{ssn[:3]}".lower()

def create_user_data(first_name, last_name, dob, ssn, city):
    """Creates the payload data for the POST request."""
    email = generate_hypothetical_email(first_name, last_name, ssn)
    username = generate_hypothetical_username(first_name, last_name, city, ssn)

    return {
        "user": {
            "streetAddress": "",
            "city": city,
            "state": "",
            "zipCode": "",
            "cellPhone": "",
            "smsOptIn": False,
            "homePhone": "",
            "email": email,
            "username": username,
            "password": "ExamplePassword123!",  # A placeholder password
            "firstName": first_name,
            "middleName": "",
            "lastName": last_name,
            "dob": dob,
            "ssn": ssn,
            "upgradeAccount": None,
            "cqas": [
                {"question": "Who was your first boss?", "answer": "myself"},
                {"question": "What color was your first car?", "answer": "black"},
                {"question": "What was your childhood nickname?", "answer": "chief"},
                {"question": "What city were you born in?", "answer": "kenol"}
            ],
            "language": "ENG"
        },
        "checkRequired": True
    }

def save_successful_user_data(file_path, user_data):
    """Saves the successful user data to a CSV file."""
    file_exists = os.path.isfile(file_path)
    
    with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['firstName', 'lastName', 'email', 'username', 'dob', 'ssn', 'city']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header if the file does not exist
        if not file_exists:
            writer.writeheader()

        writer.writerow({
            'firstName': user_data['user']['firstName'],
            'lastName': user_data['user']['lastName'],
            'email': user_data['user']['email'],
            'username': user_data['user']['username'],
            'dob': user_data['user']['dob'],
            'ssn': user_data['user']['ssn'],
            'city': user_data['user']['city']
        })

def process_data(file_path, success_file):
    """Processes the data for each user and sends a POST request."""
    if not os.path.exists(file_path):
        logging.error(f"File does not exist: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        
        for entry in reader:
            first_name = entry.get("FirstName", "").strip()
            last_name = entry.get("LastName", "").strip()
            dob = format_date(entry.get("DateOfBirth", "").strip())
            ssn = entry.get("SSN", "").strip()
            city = entry.get("City", "").strip()

            logging.info(f"Processing data for {first_name} {last_name}, SSN: {ssn}")

            session_id, csrf_token = get_new_session_and_csrf()
            route_id = '.1'  # Example route ID (you can retrieve it dynamically if needed)
            
            if session_id and csrf_token:
                headers, cookies = create_request_headers(session_id, csrf_token, route_id)
                user_data = create_user_data(first_name, last_name, dob, ssn, city)

                # Perform POST request
                response = post_check_user_data(headers, cookies, user_data)

                if response.get('status') == 'ERROR_WARNING':
                    error_codes = response.get('errorCodes', [])
                    warning_codes = response.get('warningCodes', [])
                    logging.warning(f"Warnings or Errors for {first_name} {last_name}: {error_codes}, {warning_codes}")
                else:
                    logging.info(f"Successfully processed user {first_name} {last_name}")
                    save_successful_user_data(success_file, user_data)
            else:
                logging.error(f"Failed to get session or CSRF token for {first_name} {last_name}")

def main():
    input_file = input("Enter the input CSV file path: ").strip()
    success_file = "successful_users.csv"
    
    if not os.path.exists(input_file):
        print(f"File does not exist: {input_file}")
        return

    print(f"Processing file: {input_file}")
    process_data(input_file, success_file)
    logging.info("All entries have been processed.")
    print("All entries have been processed.")

if __name__ == "__main__":
    main()
