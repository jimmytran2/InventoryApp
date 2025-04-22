import boto3
import json
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = 'Inventory'
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    # Validate required parameters
    if 'pathParameters' not in event or 'id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps({"error": "Missing required path parameter: 'id'"})
        }

    key_value = event['pathParameters']['id']  # Partition Key (PK)

    try:
        # Query for items with the given Partition Key (PK)
        response = table.query(
            KeyConditionExpression=Key('id').eq(key_value)
        )

        items = response.get('Items', [])

        if not items:
            return {
                'statusCode': 404,
                'body': json.dumps({"error": "Item not found"})
            }

        # Pick the first item (or loop through all to delete all)
        for item in items:
            sort_key_value = item['location']  # Extract Sort Key dynamically

            # Delete the item
            table.delete_item(Key={'id': key_value, 'location': sort_key_value})

        return {
            'statusCode': 200,  
            'body': "Successfully deleted item"  
        }

    except ClientError as e:
        print(f"Failed to delete item: {e.response['Error']['Message']}")
        return {
            'statusCode': 500,
            'body': json.dumps({"error": f"Error deleting item: {e.response['Error']['Message']}"})
        }

# Comment to check if lambda deploy worked