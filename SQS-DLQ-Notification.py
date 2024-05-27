import json
import requests
import base64

def send_slack_message(queue_name, aws_region, message_content):
    slack_webhook_url = 'https://hooks.slack.com/services/123456789'

    payload = {
        'text': f"New message in Dead Letter Queue\n Queue Name: {queue_name}\n AWS Region: {aws_region}\n Message Content:\n{json.dumps(message_content, indent=2)}\n"
    }

    try:
        print("Sending payload to Slack:", json.dumps(payload, indent=2))
        response = requests.post(slack_webhook_url, json=payload)
        response.raise_for_status()

        print("Slack API Response:", response.text)  # Debug statement

        if response.status_code == 200:
            print("Message sent successfully!")
        else:
            print(f"Failed to send message. Status code: {response.status_code}")
            print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Slack: {e}")

def lambda_handler(event, context):
    try:
        received_event = json.dumps(event, indent=2) 
        print("Received event:", received_event)
        if 'Records' in event and event['Records']:
            for record in event['Records']:
                arn_parts = record.get('eventSourceARN', '').split(':')
                aws_region = arn_parts[3]
                queue_name = arn_parts[-1]
                message_id = record.get('messageId', '')  
                timestamp = record.get('attributes', {}).get('SentTimestamp', '') 
                message_body = record.get('body', '')  
                message_content = {
                    'eventSourceARN': record.get('eventSourceARN', ''),
                    'messageId': message_id,
                    'timestamp': timestamp,
                    'body': message_body
                }
                print("SQS Record:", json.dumps(message_content, indent=2))  
                send_slack_message(queue_name, aws_region, message_content)
        else:
            print("No SQS records found in the event.")
    except Exception as e:
        print(f"Error processing SQS event: {e}")
