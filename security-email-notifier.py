# Copyright (c) 2024 Maxwell Block
# This code is licensed under the MIT License.
# See the LICENSE file in the project root for license terms.

import json
import boto3
import os

def lambda_handler(event, context):
    # The event is a GuardDuty finding from EventBridge
    account_id = event.get('detail', {}).get('accountId', 'N/A')
    region = event.get('detail', {}).get('region', 'N/A')
    title = event.get('detail', {}).get('title', 'N/A')
    finding_type = event.get('detail', {}).get('type', 'N/A')
    event_time = event.get('detail', {}).get('updatedAt', 'N/A')
    
    # This is the message sent to emails
    message = (
        "GuardDuty Alert\n\n"
        "Account ID: " + account_id + "\n"
        "Region: " + region + "\n"
        "Title: " + title + "\n"
        "Type: " + finding_type + "\n"
        "Updated At: " + event_time + "\n"
    )
    
    sns_client = boto3.client('sns')

    sns_topic_arn = os.environ['SNS_TOPIC_ARN']
    
    response = sns_client.publish(
        TopicArn=sns_topic_arn,
        Message=message,
        Subject='GuardDuty Alert'
    )
    
    print("Message sent to SNS:")

    # Converts the AWS account ID to be read off as a string 
    account_id_words = convert_number_to_words(account_id)
    
    # This is the spoken message read off in the call
    message_spoken = (
        f"Hello, this is AWS notifying you of a critical GuardDuty alert impacting your AWS environment. "
        f"In {account_id_words} within the {region} region, we have detected {title}. "
        f"Please take action, thank you!"
    )
    
    connect_client = boto3.client('connect')

    # These are environment variables for Amazon Connect
    destination_phone_number = os.environ['DESTINATION_PHONE_NUMBER']
    contact_flow_id = os.environ['CONTACT_FLOW_ID']
    instance_id = os.environ['INSTANCE_ID']
    source_phone_number = os.environ['SOURCE_PHONE_NUMBER']
    
    # Initiate the outbound call
    response = connect_client.start_outbound_voice_contact(
        DestinationPhoneNumber=destination_phone_number, 
        ContactFlowId=contact_flow_id,  
        InstanceId=instance_id, 
        SourcePhoneNumber=source_phone_number,      
        Attributes={
            'messageToRead': message_spoken
        }
    )
    
    print(response)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Called')
    }

# Converts each number to a word
def convert_number_to_words(number):
    number_map = {
        '0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
        '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'
    }
    return ' '.join(number_map[digit] for digit in str(number))
