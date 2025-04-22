import boto3
import json
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = 'Inventory'
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    # Check if 'id' is in the request
    if 'pathParameters' not in event or 'id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'id' path parameter")
        }

    key_value = event['pathParameters']['id']

    try:
        # Query DynamoDB to get all records with the given id
        response = table.query(
            KeyConditionExpression=Key('id').eq(key_value)
        )

        items = response.get('Items', [])

        if not items:
            return {
                'statusCode': 404,
                'body': json.dumps('Item not found')
            }
 
        return {
            'statusCode': 200,
            'body': json.dumps(items, default=str)  # Convert to JSON-friendly format
        }

    except ClientError as e:
        print(f"Failed to fetch item: {e.response['Error']['Message']}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error fetching item: {e.response['Error']['Message']}")
        }

# Comment to check if lambda deploy worked