import boto3
import json
import os

# Load environment variable for table name
TABLE_NAME = os.getenv('TASKS_TABLE')

# Set up DynamoDB resource outside the handler to reuse the resource
# across multiple invocations.
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    print('received:', event)
    
    user = event['requestContext']['authorizer']['principalId']
    
    # Query the DynamoDB table for tasks related to the user
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('user').eq(f'user#{user}')
    )
    
    items = response.get('Items', [])

    # Build and return the HTTP response
    response = {
        'statusCode': 200,
        'headers': {
        'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(items)
    }
    return response
