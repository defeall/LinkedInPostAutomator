import json
import logging
import os
import boto3
import urllib3
from datetime import datetime

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class LinkedInAutomator:
    def __init__(self):
        # Get credentials from Parameter Store
        self.author_sub = os.environ.get('author_sub')
        self.access_token = os.environ.get('access_token')
        self.author_urn = f'urn:li:person:{self.author_sub}'
        
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }
        
        if self.access_token:
            logger.info("LinkedIn access token loaded successfully")
        else:
            logger.error("LinkedIn access token not found")
            raise ValueError("LinkedIn access token is required")

    def get_user_info(self):
        """Fetch LinkedIn user information"""
        url = "https://api.linkedin.com/v2/userinfo"
        http = urllib3.PoolManager()
        
        try:
            response = http.request('GET', url, headers=self.headers)
            if response.status == 200:
                user_info = json.loads(response.data.decode('utf-8'))
                logger.info("Fetched user info successfully")
                return user_info
            else:
                logger.error(f"Failed to fetch user info: {response.status}")
                return None
        except Exception as e:
            logger.error(f"Error fetching user info: {e}")
            return None

    def post_on_linkedin(self, text_to_post: str):
        """Post content to LinkedIn"""
        url = 'https://api.linkedin.com/v2/ugcPosts'
        http = urllib3.PoolManager()
        
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
            response = http.request(
                'POST',
                url,
                body=json.dumps(post_data).encode('utf-8'),
                headers=self.headers
            )
            
            if response.status == 201:
                logger.info("Post shared successfully on LinkedIn!")
                response_data = json.loads(response.data.decode('utf-8'))
                return True, response_data.get('id', 'unknown')
            else:
                logger.error(f"Error posting to LinkedIn: {response.status} - {response.data}")
                return False, None
                
        except Exception as e:
            logger.error(f"Failed to post on LinkedIn: {e}")
            return False, None

def send_notification(success: bool, result: str, msg: str = None):
    """Send SNS notification about posting status"""
    sns = boto3.client("sns")

    TOPIC_ARN = os.environ.get('NOTIFICATION_SNS_TOPIC')

    if not TOPIC_ARN:
        return
    
    try:
        message = {
            "Post": result,
            "status": "success" if success else "failed",
            "timestamp": datetime.now().isoformat()
        }
        
        if msg:
            message["status"] = msg
        
        sns.publish(
            TopicArn=TOPIC_ARN,
            Message=json.dumps(message),
            Subject=f"LinkedIn Post {'Successful' if success else 'Failed'}"
        )
        logger.info(f"Notification sent for post")
    except Exception as e:
        logger.error(f"Error sending notification: {e}")

def lambda_handler(event, context):
    """
    Lambda handler for posting to LinkedIn
    Expects event from SNS with content and post_id
    """
    logger.info(f"Event received: {json.dumps(event)}")
    
    try:
        
        lambda_client = boto3.client('lambda')

        # Initialize LinkedIn automator
        automator = LinkedInAutomator()
        
        response = lambda_client.invoke(
            FunctionName='DevOpsContentGenerator',  # ARN or name
            InvocationType='RequestResponse',        # sync call
            Payload=json.dumps(event),
        )
        logger.info(f"Response received from DevOpsContentGenerator: {response}")
        # Get response payload
        content = json.loads(response['Payload'].read())
        logger.info(f"type: {type(content['body'])}")
        logger.info(f"Content received from DevOpsContentGenerator: {content}")
        # Post to LinkedIn
        result = automator.post_on_linkedin(content["body"])
        
        if result:
            # Send success notification
            send_notification(True, result, "Posted successfully to LinkedIn")
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Successfully posted to LinkedIn',
                    'LinkedIn_post': result
                })
            }
        else:
            # Send failure notification
            send_notification(False, result, "Failed to post to LinkedIn")
            
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'message': 'Failed to post to LinkedIn'
                })
            }
            
    except Exception as e:
        logger.error(f"Error in lambda_handler: {str(e)}")
        
        # Send error notification
        send_notification(False, str(e), "Error occurred in LinkedInPostAutomator")
        
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }