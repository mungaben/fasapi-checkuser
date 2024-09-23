# # app/routes/user_routes.py

# from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
# from app.models.user import UserLogin, UserRegister, TokenResponse, UserInput
# from fastapi_jwt_auth import AuthJWT
# from app.services.user_service import create_user, get_user_by_username, verify_password
# from app.auth import authorize_user
# from app.utils.csrf import generate_csrf_token
# import csv
# from io import StringIO
# from typing import List, Dict
# import random
# import logging
# import os

# # Initialize the router
# router = APIRouter()

# # Set up logging
# logging.basicConfig(level=logging.INFO)

# log_file_path = os.path.join(os.getcwd(), 'data_processing.log')
# logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='w')

# # Route to get CSRF token
# @router.get("/csrf-token")
# async def get_csrf_token():
#     token = generate_csrf_token()
#     return {"csrf_token": token}


# # Register new user
# @router.post("/register", response_model=TokenResponse)
# async def register(user: UserRegister, Authorize: AuthJWT = Depends()):
#     # Check if user already exists
#     existing_user = await get_user_by_username(user.username)
#     if existing_user:
#         raise HTTPException(status_code=400, detail="User already exists")

#     # Create the new user
#     user_data = await create_user(user)
#     access_token = Authorize.create_access_token(subject=user.username)
    
#     # Log user registration
#     logging.info(f"User {user.username} registered successfully.")
    
#     return TokenResponse(access_token=access_token, user=user_data)


# # Login user
# @router.post("/login", response_model=TokenResponse)
# async def login(user: UserLogin, Authorize: AuthJWT = Depends()):
#     db_user = await get_user_by_username(user.username)
#     if not db_user or not await verify_password(user.password, db_user['password']):
#         raise HTTPException(status_code=401, detail="Invalid username or password")
    
#     access_token = Authorize.create_access_token(subject=user.username)
    
#     # Log login attempt
#     logging.info(f"User {user.username} logged in successfully.")
    
#     return TokenResponse(access_token=access_token, user=db_user)


# # Protected route example
# @router.get("/protected", dependencies=[Depends(authorize_user)])
# async def protected():
#     return {"message": "You are authorized to access this route"}


# # # Function to simulate user data processing based on SSN and other conditions
# # def process_user_data(first_name: str, last_name: str, ssn: str, city: str) -> Dict:
# #     # Simulating different conditions based on the SSN or username
# #     if ssn.endswith("747"):
# #         return {"status": "matched", "message": "SSN_ASSOCIATED_SSA_MATCHED", "data": f"{first_name} {last_name} SSN Matched"}
# #     elif ssn.endswith("982"):
# #         return {"status": "username_invalid", "message": "USERNAME_INVALID", "data": f"{first_name} {last_name} Needs New Username"}
# #     else:
# #         return {"status": "success", "message": "Successfully processed", "data": f"{first_name} {last_name} processed successfully"}


# # # Function to generate a new username if the current one is invalid
# # def generate_new_username(first_name: str, last_name: str) -> str:
# #     return f"{first_name}.{last_name}{random.randint(100, 999)}"


# # # Route to upload a CSV file and process records
# # @router.post("/upload")
# # async def upload_file(file: UploadFile = File(...)):
# #     # Ensure the file is a CSV file
# #     if not file.filename.endswith(".csv"):
# #         raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")

# #     # Read and process the CSV file
# #     results = []
# #     file_content = await file.read()
# #     file_stream = StringIO(file_content.decode("utf-8"))
# #     reader = csv.DictReader(file_stream)

# #     # Loop over each row in the CSV
# #     for row in reader:
# #         first_name = row.get("FirstName", "").strip()
# #         last_name = row.get("LastName", "").strip()
# #         ssn = row.get("SSN", "").strip()
# #         city = row.get("City", "").strip()

# #         # Log that the row is being processed
# #         logging.info(f"Processing data for {first_name} {last_name}, SSN: {ssn}")

# #         # Process each record
# #         result = process_user_data(first_name, last_name, ssn, city)

# #         # If the username is invalid, generate a new one and retry
# #         if result["status"] == "username_invalid":
# #             new_username = generate_new_username(first_name, last_name)
# #             logging.info(f"Retrying with new username: {new_username}")
# #             result["new_username"] = new_username
# #             result["message"] = "Retried with new username"

# #         # Append the result for this row
# #         results.append(result)

# #     return {"results": results}

# # Setup logging configuration

# #  -------------------------
# # Utility Functions
# # -------------------------
# def get_new_session_and_csrf(retries=3):
#     url = 'https://studentaid.gov/app/keepSessionAlive.action'
#     headers = {
#         'Accept': 'application/json',
#         'Content-Type': 'application/json;charset=UTF-8',
#         'Referer': 'https://studentaid.gov/fsa-id/create-account/launch',
#         'User-Agent': 'Mozilla/5.0'
#     }
#     for attempt in range(retries):
#         try:
#             response = requests.get(url, headers=headers)
#             if response.status_code == 200:
#                 session_id = response.cookies.get('SESSION', None)
#                 csrf_token = response.cookies.get('XSRF-TOKEN', None)
#                 return session_id, csrf_token
#             else:
#                 logging.error(f"Failed to fetch session and CSRF token: {response.status_code} {response.text}")
#         except requests.RequestException as e:
#             logging.error(f"Network error during session fetch: {e}")
#     return None, None

# def create_request_headers(session_id, csrf_token, route_id):
#     headers = {
#         'Accept': 'application/json',
#         'Content-Type': 'application/json;charset=UTF-UTF-8',
#         'X-XSRF-TOKEN': csrf_token,
#         'User-Agent': 'Mozilla/5.0',
#         'Referer': 'https://studentaid.gov/fsa-id/create-account/confirm-verify',
#         'Origin': 'https://studentaid.gov'
#     }
#     cookies = {
#         'SESSION': session_id,
#         'XSRF-TOKEN': csrf_token,
#         'ROUTEID': route_id
#     }
#     return headers, cookies

# def post_check_user_data(headers, cookies, user_data):
#     url = 'https://studentaid.gov/app/api/auth/registration/checkUserData'
#     response = requests.post(url, headers=headers, cookies=cookies, json=user_data)
#     return response.json()

# def format_date(dob):
#     try:
#         date_obj = datetime.strptime(dob, '%Y-%m-%d')
#         return date_obj.strftime('%Y-%m-%d')
#     except ValueError:
#         logging.warning(f"Date format error for: {dob}")
#         return None

# def generate_hypothetical_email(first_name, last_name, ssn):
#     return f"{first_name}{last_name}{ssn}@gmail.com"

# def generate_hypothetical_username(first_name, last_name, city, ssn):
#     return f"{first_name}{last_name}{city}{ssn[:3]}".lower()

# def create_user_data(first_name, last_name, dob, ssn, city):
#     email = generate_hypothetical_email(first_name, last_name, ssn)
#     username = generate_hypothetical_username(first_name, last_name, city, ssn)

#     return {
#         "user": {
#             "streetAddress": "",
#             "city": city,
#             "state": "",
#             "zipCode": "",
#             "cellPhone": "",
#             "smsOptIn": False,
#             "homePhone": "",
#             "email": email,
#             "username": username,
#             "password": "ExamplePassword123!",
#             "firstName": first_name,
#             "middleName": "",
#             "lastName": last_name,
#             "dob": dob,
#             "ssn": ssn,
#             "upgradeAccount": None,
#             "cqas": [
#                 {"question": "Who was your first boss?", "answer": "myself"},
#                 {"question": "What color was your first car?", "answer": "black"},
#                 {"question": "What was your childhood nickname?", "answer": "chief"},
#                 {"question": "What city were you born in?", "answer": "kenol"}
#             ],
#             "language": "ENG"
#         },
#         "checkRequired": True
#     }

# # -------------------------
# # Data Models for Pydantic
# # -------------------------



# # -------------------------
# # Routes
# # -------------------------

# # Single record processing for JSON requests (POST)
# @router.post("/process_single_record", response_class=JSONResponse)
# async def process_single_record(data: UserInput):
#     first_name = data.first_name
#     last_name = data.last_name
#     dob = format_date(data.dob)
#     ssn = data.ssn
#     city = data.city

#     session_id, csrf_token = get_new_session_and_csrf()
#     route_id = '.1'

#     if session_id and csrf_token:
#         headers, cookies = create_request_headers(session_id, csrf_token, route_id)
#         user_data = create_user_data(first_name, last_name, dob, ssn, city)
#         response = post_check_user_data(headers, cookies, user_data)

#         if response.get('status') == 'ERROR_WARNING':
#             error_codes = response.get('errorCodes', [])
#             warning_codes = response.get('warningCodes', [])
#             logging.warning(f"Warnings or Errors for {first_name} {last_name}: {error_codes}, {warning_codes}")
#             return {"status": "Error", "errors": error_codes, "warnings": warning_codes}
#         else:
#             logging.info(f"Successfully processed user {first_name} {last_name}")
#             return {"status": "Success", "message": f"Successfully processed {first_name} {last_name}"}
#     else:
#         return {"status": "Error", "message": "Failed to get session or CSRF token"}


# # CSV File Upload for multiple records
# @router.post("/upload", response_class=JSONResponse)
# async def upload_file(file: UploadFile = File(...)):
#     if not file.filename.endswith(".csv"):
#         raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")

#     results = []
#     file_content = await file.read()
#     file_stream = StringIO(file_content.decode("utf-8"))
#     reader = csv.DictReader(file_stream)

#     for row in reader:
#         first_name = row.get("FirstName", "").strip()
#         last_name = row.get("LastName", "").strip()
#         dob = format_date(row.get("DateOfBirth", "").strip())
#         ssn = row.get("SSN", "").strip()
#         city = row.get("City", "").strip()

#         logging.info(f"Processing data for {first_name} {last_name}, SSN: {ssn}")

#         session_id, csrf_token = get_new_session_and_csrf()
#         route_id = '.1'

#         if session_id and csrf_token:
#             headers, cookies = create_request_headers(session_id, csrf_token, route_id)
#             user_data = create_user_data(first_name, last_name, dob, ssn, city)
#             response = post_check_user_data(headers, cookies, user_data)

#             if response.get('status') == 'ERROR_WARNING':
#                 error_codes = response.get('errorCodes', [])
#                 warning_codes = response.get('warningCodes', [])
#                 logging.warning(f"Warnings or Errors for {first_name} {last_name}: {error_codes}, {warning_codes}")
#                 results.append({"status": "Error", "first_name": first_name, "last_name": last_name, "errors": error_codes, "warnings": warning_codes})
#             else:
#                 logging.info(f"Successfully processed user {first_name} {last_name}")
#                 results.append({"status": "Success", "first_name": first_name, "last_name": last_name})

#         else:
#             logging.error(f"Failed to get session or CSRF token for {first_name} {last_name}")
#             results.append({"status": "Error", "first_name": first_name, "last_name": last_name, "message": "Failed to get session or CSRF token"})

#     return {"results": results}



# app/routes/user_routes.py

import os
import csv
import logging
import random
import requests
from io import StringIO
from datetime import datetime
from typing import List, Dict

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from app.models.user import UserLogin, UserRegister, TokenResponse, UserInput
from app.services.user_service import create_user, get_user_by_username, verify_password
from app.auth import authorize_user
from app.utils.csrf import generate_csrf_token


# Initialize the router
router = APIRouter()

# Set up logging configuration
log_file_path = os.path.join(os.getcwd(), 'data_processing.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='w')

# -------------------------
# Utility Functions

def get_new_session_and_csrf(retries=3):
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
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=UTF-8',
        'X-XSRF-TOKEN': csrf_token,
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://studentaid.gov/fsa-id/create-account/confirm-verify',
        'Origin': 'https://studentaid.gov'
    }
    cookies = {
        'SESSION': session_id,
        'XSRF-TOKEN': csrf_token,
        'ROUTEID': route_id
    }
    return headers, cookies

def post_check_user_data(headers, cookies, user_data):
    url = 'https://studentaid.gov/app/api/auth/registration/checkUserData'
    response = requests.post(url, headers=headers, cookies=cookies, json=user_data)
    
    # Log the raw response data for debugging
    logging.info(f"API Response: {response.json()}")
    
    if response.status_code != 200:
        logging.error(f"Failed request: {response.status_code}, {response.text}")
        return {"status": "error", "message": "Failed to process request", "response": response.text}
    
    return response.json()

def format_date(dob):
    try:
        date_obj = datetime.strptime(dob, '%Y-%m-%d')
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        logging.warning(f"Date format error for: {dob}")
        return None

def generate_hypothetical_email(first_name, last_name, ssn):
    return f"{first_name}{last_name}{ssn}@gmail.com"

def generate_hypothetical_username(first_name, last_name, city, ssn):
    return f"{first_name}{last_name}{city}{ssn[:3]}".lower()

def create_user_data(first_name, last_name, dob, ssn, city):
    email = generate_hypothetical_email(first_name, last_name, ssn)
    username = generate_hypothetical_username(first_name, last_name, city, ssn)
    logging.info(email,username,ssn ,dob,  first_name,last_name)

    return {
        "user": {
            "streetAddress": "",
            "city":"BROOKLYN",
            "state": "",
            "zipCode": "",
            "cellPhone": "",
            "smsOptIn": False,
            "homePhone": "",
            "email": email,
            "username": username,
            "password": "BenKiko@21",
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

# -------------------------
# Routes
# -------------------------

# Single record processing for JSON requests (POST)
@router.post("/process_single_record", response_class=JSONResponse)
async def process_single_record(data: UserInput):
    first_name = data.first_name
    last_name = data.last_name
    dob = format_date(data.dob)
    ssn = data.ssn
    city = data.city

    logging.info(f"Processing data for {first_name} {last_name}, SSN: {ssn}")

    session_id, csrf_token = get_new_session_and_csrf()
    route_id = '.1'

    if session_id and csrf_token:
        headers, cookies = create_request_headers(session_id, csrf_token, route_id)
        user_data = create_user_data(first_name, last_name, dob, ssn, city)
        response = post_check_user_data(headers, cookies, user_data)

        logging.info(f"Response for {first_name} {last_name}: {response}")

        # If there are warnings or errors, log both properly
        if 'status' in response and response['status'] in ['ERROR_WARNING', 'SUCCESS_WARNING']:
            error_codes = response.get('errorCodes', [])
            warning_codes = response.get('warningCodes', [])

            # Improved logging format to match expectations
            if error_codes or warning_codes:
                logging.warning(f"Warnings or Errors for {first_name} {last_name}: Errors - {error_codes}, Warnings - {warning_codes}")
            
            return {"status": "Warning/Error", "errors": error_codes, "warnings": warning_codes}

        elif response.get('status') == 'success':
            logging.info(f"Successfully processed user {first_name} {last_name}")
            return {"status": "Success", "message": f"Successfully processed {first_name} {last_name}"}
        
        else:
            logging.error(f"Unexpected response for {first_name} {last_name}: {response}")
            return {"status": "Error", "message": "Unexpected response from the API"}
    else:
        logging.error(f"Failed to get session or CSRF token for {first_name} {last_name}")
        return {"status": "Error", "message": "Failed to get session or CSRF token"}

# CSV File Upload for multiple records
@router.post("/upload", response_class=JSONResponse)
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")

    results = []
    file_content = await file.read()
    file_stream = StringIO(file_content.decode("utf-8"))
    reader = csv.DictReader(file_stream)

    for row in reader:
        first_name = row.get("FirstName", "").strip()
        last_name = row.get("LastName", "").strip()
        dob = format_date(row.get("DateOfBirth", "").strip())
        ssn = row.get("SSN", "").strip()
        city = row.get("City", "").strip()

        logging.info(f"Processing data for {first_name} {last_name}, SSN: {ssn}")

        session_id, csrf_token = get_new_session_and_csrf()
        route_id = '.1'

        if session_id and csrf_token:
            headers, cookies = create_request_headers(session_id, csrf_token, route_id)
            user_data = create_user_data(first_name, last_name, dob, ssn, city)
            response = post_check_user_data(headers, cookies, user_data)

            # Handle errors and warnings
            if response.get('status') in ['ERROR_WARNING', 'SUCCESS_WARNING']:
                error_codes = response.get('errorCodes', [])
                warning_codes = response.get('warningCodes', [])
                logging.warning(f"Warnings or Errors for {first_name} {last_name}: Errors - {error_codes}, Warnings - {warning_codes}")
                results.append({
                    "status": "Warning/Error",
                    "first_name": first_name,
                    "last_name": last_name,
                    "errors": error_codes,
                    "warnings": warning_codes
                })
            elif response.get('status') == 'success':
                logging.info(f"Successfully processed user {first_name} {last_name}")
                results.append({
                    "status": "Success",
                    "first_name": first_name,
                    "last_name": last_name
                })
            else:
                logging.error(f"Unexpected response for {first_name} {last_name}: {response}")
                results.append({
                    "status": "Error",
                    "first_name": first_name,
                    "last_name": last_name,
                    "message": "Unexpected response from the API"
                })
        else:
            logging.error(f"Failed to get session or CSRF token for {first_name} {last_name}")
            results.append({
                "status": "Error",
                "first_name": first_name,
                "last_name": last_name,
                "message": "Failed to get session or CSRF token"
            })

    return {"results": results}