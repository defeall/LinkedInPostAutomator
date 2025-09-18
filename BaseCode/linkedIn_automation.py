import requests
from dotenv import load_dotenv
import os
import logging
from DevOpsContentGenerator import DevOpsContentWorkflow
import asyncio


class LinkedInAutomator:
    def __init__(self):
        self.author_urn = f'urn:li:person:{os.getenv("author_sub")}'
        self.access_token = os.getenv('access_token')
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }
        self._setup_logging()
        if self.access_token:
            logging.info("LinkedIn access_token exists")
        else:
            logging.error("LinkedIn access_token not set")

    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def get_user_info(self):
        url = "https://api.linkedin.com/v2/userinfo"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            logging.info("Fetched user info successfully.")
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Failed to fetch user info: {e}")
            return None

    def post_on_linkedin(self, text_to_post: str):
        url = 'https://api.linkedin.com/v2/ugcPosts'
        post_data = {
            "author": self.author_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text_to_post
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        try:
            response = requests.post(url, headers=self.headers, json=post_data)
            if response.status_code == 201:
                logging.info("Post shared successfully on LinkedIn!")
                return True
            else:
                logging.error(f"Error: {response.status_code} - {response.text}")
                return False
        except requests.RequestException as e:
            logging.error(f"Failed to post on LinkedIn: {e}")
            return False

    def run(self, text_to_post=""):
        # Optionally fetch user info
        # user_info = self.get_user_info()
        # logging.info(f"User Info: {user_info}")
        self.post_on_linkedin(text_to_post)

if __name__ == "__main__":
    load_dotenv(override=True)
    automator = LinkedInAutomator()

    openai_api_key = os.getenv('OPENAI_API_KEY')
    if openai_api_key:
        logging.info(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
    else:
        logging.error("OpenAI API Key not set")
        
    workflow = DevOpsContentWorkflow(api_key=openai_api_key, model="gpt-4o-mini")
    text_to_post = asyncio.run(workflow.run())
    
    if text_to_post:
        automator.run(text_to_post=text_to_post)
    else:
        logging.error("No text generated to post on LinkedIn.")