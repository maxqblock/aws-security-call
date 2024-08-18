# Copyright (c) 2024 Maxwell Block
# This code is licensed under the MIT License.
# See the LICENSE file in the project root for license terms.

import json
import boto3
import time
import os

def lambda_handler(event, context):
    # The event is a GuardDuty finding from EventBridge
    account_id = event.get('detail', {}).get('accountId', 'N/A')
    region = event.get('detail', {}).get('region', 'N/A')
    title = event.get('detail', {}).get('title', 'N/A')
    finding_type = event.get('detail', {}).get('type', 'N/A')
    time = event.get('detail', {}).get('updatedAt', 'N/A')
    
    # This is the message sent to emails
    message = (
        "GuardDuty Alert\n\n"
        "Account ID: " + account_id + "\n"
        "Region: " + region + "\n"
        "Title: " + title + "\n"
        "Type: " + finding_type + "\n"
        "Updated At: " + time + "\n"
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
    
    polly_client = boto3.client('polly')
    
    response = polly_client.synthesize_speech(
        Text=message_spoken,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )
    
    mp3_file_path = '/tmp/output.mp3'
    with open('/tmp/output.mp3', 'wb') as file:
        file.write(response['AudioStream'].read())
    
    # Upload the mp3 file to a S3 bucket
    s3_client = boto3.client('s3')
    bucket_name = os.environ['S3_BUCKET_NAME']
    s3_key = 'output.mp3'
    s3_client.upload_file(mp3_file_path, bucket_name, s3_key)

    time.sleep(30)  
    
    connect_client = boto3.client('connect')
    
    s3_url = f"https://s3.amazonaws.com/{bucket_name}/{s3_key}"

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
            's3AudioUrl': s3_url
        }
    )
    
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

