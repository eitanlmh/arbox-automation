# arbox_client.py
# Contains the core logic to interact with Arbox.
# Implements functions like login, book lesson, etc.
# Can use browser automation or HTTP requests to perform these actions.
import requests
def login(email:str, password:str):
    """
    Logs in to the Arbox API and retrieves access and refresh tokens.

    :param email: User's email address
    :param password: User's password
    :return: Tuple containing access token and refresh token, or an error string
    """
    url = "https://apiappv2.arboxapp.com/api/v2/user/login"
    headers = {
        "accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Connection": "Keep-Alive",
        "referername": "app",
        "User-Agent": "okhttp/4.9.2",
        "version": "11",
        "whitelabel": "Arbox"
    }
    payload = {
        "email": email,
        "password": password
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        # Assuming the response contains tokens like this:
        access_token = data.get("accesstoken") or data.get("accessToken")
        refresh_token = data.get("refreshtoken") or data.get("refreshToken")
        return access_token, refresh_token
    else:
        return f"login failed: {response.status_code} {response.text}"

def get_profile(access_token: str, refresh_token: str):
    """
    Fetches the user profile information.

    :param access_token: JWT token obtained after login
    :param refresh_token: JWT refresh token obtained after login
    :return: JSON response containing user profile data or an error string
    """
    if not access_token:
        raise Exception("Not logged in or missing access token")
    url = "https://apiappv2.arboxapp.com/api/v2/user/profile"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accesstoken": access_token,
        "Connection": "Keep-Alive",
        "Host": "apiappv2.arboxapp.com",
        # "If-Modified-Since": "Mon, 07 Jul 2025 09:49:50 GMT",  # Optional: can be omitted or updated dynamically
        "referername": "app",
        "refreshtoken": refresh_token,
        "User-Agent": "okhttp/4.9.2",
        "version": "11",
        "whitelabel": "Arbox"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return f"get_profile failed: {response.status_code} {response.text}"
    
def get_schedule_between_dates(start_date: str, end_date: str, access_token: str, refresh_token: str, locations_box_id: int, boxes_id: int):
    """
    Fetches the available lessons and data about them between two datetime ranges.

    :param start_date: Start datetime in ISO 8601 format (e.g. '2025-07-07T13:23:13.430Z')
    :param end_date: End datetime in ISO 8601 format (e.g. '2025-07-10T20:00:00.000Z')
    :param access_token: JWT token obtained after login
    :param refresh_token: JWT refresh token obtained after login
    :param locations_box_id: ID of the location box (used to filter schedule)
    :param boxes_id: ID of the box (e.g., gym/studio) to fetch lessons for
    :return: JSON response containing lessons data or an error string
    """
    if not access_token or not refresh_token:
        raise Exception("Missing access or refresh token. Please login first.")

    url = "https://apiappv2.arboxapp.com/api/v2/schedule/betweenDates"
    headers = {
        "accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Connection": "Keep-Alive",
        "referername": "app",
        "User-Agent": "okhttp/4.9.2",
        "version": "11",
        "whitelabel": "Arbox",
        "accesstoken": access_token,
        "refreshtoken": refresh_token
    }

    """
    Example payload: (the time is weirddly set to the same value)
      {"from": "2025-07-07T13:23:13.430Z",
      "to": "2025-07-07T13:23:13.430Z",
      "locations_box_id": 100,
      "boxes_id": 101}
    """
    payload = {
        "from": start_date,
        "to": end_date,
        "locations_box_id": locations_box_id,
        "boxes_id": boxes_id
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()
    else:
        return f"get_schedule_between_dates failed: {response.status_code} {response.text}"

def schedule_lesson(schedule_id: int,membership_user_id:int, access_token: str, refresh_token: str, extras = None):
    """
    Booking a lesson.

    :param schedule_id: The ID of the scheduled class to check
    :param access_token: JWT token obtained after login
    :param refresh_token: Refresh token from login
    :return: JSON response with the late cancel status or an error message
    """
    url = "https://apiappv2.arboxapp.com/api/v2/scheduleUser/insert"

    headers = {
        "accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Connection": "Keep-Alive",
        "referername": "app",
        "User-Agent": "okhttp/4.9.2",
        "version": "11",
        "whitelabel": "Arbox",
        "accesstoken": access_token,
        "refreshtoken": refresh_token
    }

    payload = {
    "schedule_id": schedule_id,
    "membership_user_id": membership_user_id,
    "extras": extras or None
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()
    else:
        return f"check_late_cancel failed: {response.status_code} {response.text}"

def delete_schedule(schedule_id: int,schedule_user_id:int, access_token: str, refresh_token: str, late_cancel: bool = False):
    """
    Cancels (deletes) a scheduled lesson by schedule ID.

    :param schedule_id: The ID of the schedule to delete/cancel
    :param access_token: JWT access token from login
    :param refresh_token: JWT refresh token from login
    :return: JSON response from the API or error string
    """
    url = "https://apiappv2.arboxapp.com/api/v2/scheduleUser/delete"
    
    headers = {
        "accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Connection": "Keep-Alive",
        "referername": "app",
        "User-Agent": "okhttp/4.9.2",
        "version": "11",
        "whitelabel": "Arbox",
        "accesstoken": access_token,
        "refreshtoken": refresh_token
    }
    
    payload = {
    "schedule_user_id": schedule_user_id,
    "schedule_id": schedule_id,
    "late_cancel": late_cancel
    }
    
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        return f"delete_schedule failed: {response.status_code} {response.text}"