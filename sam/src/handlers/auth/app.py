import json
from datetime import datetime
import jwt

def lambda_handler(event, context):
    print('Received:', event)

    # Extract and split the token from the event's authorization token
    token = event['authorizationToken'].split(' ')[1]
    try:
        # Decode and verify the JWT token
        decoded = jwt.decode(token, 'secretphrase', algorithms=['HS256'])
        print(f'Verified token: {decoded}')
        principal_id = decoded['sub']
        effect = 'Allow'
        resource = f"{event['methodArn'].split('/', 1)[0]}/*"
        policy = generate_policy(principal_id, effect, resource)
        print(f"Generated policy: {json.dumps(policy)}")
        return policy

    except jwt.exceptions.DecodeError as e:
        print(e)
        raise Exception('Error: Invalid token')

def generate_policy(principal_id, effect, resource):
    """Generate and return an AWS IAM policy.
    This function constructs an AWS IAM policy based on given criteria
    and returns it in a format suitable for use with AWS services.
    The returned policy can be attached to users, groups, or roles
    to grant permissions to AWS resources.
    """
    auth_response = {}
    auth_response['principalId'] = principal_id

    if effect and resource:
        policy_document = {}
        policy_document['Version'] = '2012-10-17'
        policy_document['Statement'] = []
        statement_one = {}
        statement_one['Action'] = 'execute-api:Invoke'
        statement_one['Effect'] = effect
        statement_one['Resource'] = resource
        policy_document['Statement'].append(statement_one)
        auth_response['policyDocument'] = policy_document

    auth_response['context'] = {
        'userId': 1,
        'createdAt': datetime.now().isoformat()
    }
    
    return auth_response
