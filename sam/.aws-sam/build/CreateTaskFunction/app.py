import boto3
from uuid import uuid4
from datetime import datetime
import json
import os

# Load environment variable for table name. This is done outside the handler
# to reuse the variable across multiple invocations of the lambda function.
TABLE_NAME = os.getenv('TASKS_TABLE')

# Set up DynamoDB resource outside the handler to reuse the resource
# across multiple invocations.
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    print('received:', event)

    body = json.loads(event['body'])
    user = event['requestContext']['authorizer']['principalId']
    id = str(uuid4())

    title = body['title']
    body_text = body['body']

    due_date = datetime.now().isoformat()
    created_at = due_date

    if 'dueDate' in body:
        due_date = body['dueDate']
    
    # Construct the item that we want to store in DynamoDB
    item = {
        'user': f'user#{user}',
        'id': f'task#{id}',
        'title': title,
        'body': body_text,
        'dueDate': due_date,
        'createdAt': created_at
    }

    print(f'Writing data to table {table.name}')
    # Add the item to the DynamoDB table
    table.put_item(Item=item)
    print('Success - item added')

    # Build and return the HTTP response
    response = {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(item)
    }
    return response
