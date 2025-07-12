# arbox_client.py
# Contains the core logic to interact with Arbox.
# Implements functions like login, book lesson, etc.
# Can use browser automation or HTTP requests to perform these actions.
import requests

class ArboxClient:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.access_token = None
        self.refresh_token = None

    def login(self):
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
            "email": self.email,
            "password": self.password
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            # Assuming the response contains tokens like this:
            self.access_token = data.get("accesstoken") or data.get("accessToken")
            self.refresh_token = data.get("refreshtoken") or data.get("refreshToken")
            return "success"
        else:
            return f"login failed: {response.status_code} {response.text}"
   
    def get_profile(self):
        if not self.access_token:
            raise Exception("Not logged in or missing access token")

        url = "https://apiappv2.arboxapp.com/api/v2/user/profile"
        headers = {
            "accept": "application/json, text/plain, */*",
            "accesstoken": self.access_token,
            "Connection": "Keep-Alive",
            "Host": "apiappv2.arboxapp.com",
            # "If-Modified-Since": "Mon, 07 Jul 2025 09:49:50 GMT",  # Optional: can be omitted or updated dynamically
            "referername": "app",
            "refreshtoken": self.refresh_token or "",
            "User-Agent": "okhttp/4.9.2",
            "version": "11",
            "whitelabel": "Arbox"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return f"get_profile failed: {response.status_code} {response.text}"
        
    